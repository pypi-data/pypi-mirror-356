import typing
from collections.abc import Callable
from typing import Unpack

from loguru import logger
from notte_browser.session import NotteSession
from notte_browser.vault import VaultSecretsScreenshotMask
from notte_browser.window import BrowserWindow
from notte_core.actions import CompletionAction
from notte_core.common.config import NotteConfig
from notte_core.common.tracer import LlmUsageDictTracer
from notte_core.credentials.base import BaseVault
from notte_core.llms.engine import LLMEngine
from notte_sdk.types import AgentCreateRequestDict, AgentRunRequestDict
from pydantic import field_validator
from typing_extensions import override

from notte_agent.common.base import BaseAgent
from notte_agent.common.conversation import Conversation
from notte_agent.common.parser import NotteStepAgentOutput
from notte_agent.common.types import AgentResponse
from notte_agent.falco.agent import FalcoAgent
from notte_agent.gufo.parser import GufoParser
from notte_agent.gufo.perception import GufoPerception
from notte_agent.gufo.prompt import GufoPrompt


class GufoConfig(NotteConfig):
    enable_perception: bool = True
    auto_scrape: bool = True

    @field_validator("enable_perception")
    def check_perception(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Perception should be enabled for gufo. Don't set this argument to `False`.")
        return value

    @field_validator("auto_scrape")
    def check_auto_scrape(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Auto scrape should be enabled for gufo. Don't set this argument to `False`.")
        return value


class GufoAgent(BaseAgent):
    """
    A base agent implementation that coordinates between an LLM and the Notte environment.

    This class demonstrates how to build an agent that can:
    1. Maintain a conversation with an LLM
    2. Execute actions in the Notte environment
    3. Parse and format responses between the LLM and Notte

    To customize this agent:
    1. Implement your own Parser class to format observations and actions
    2. Modify the conversation flow in the run() method
    3. Adjust the think() method to handle LLM interactions
    4. Customize the ask_notte() method for your specific needs

    Args:
        task (str): The task description for the agent
        model (str): The LLM model identifier
        max_steps (int): Maximum number of steps before terminating
        headless (bool): Whether to run browser in headless mode
        parser (Parser | None): Custom parser for formatting interactions
    """

    def __init__(
        self,
        window: BrowserWindow,
        vault: BaseVault | None = None,
        step_callback: Callable[[str, NotteStepAgentOutput], None] | None = None,
        **data: Unpack[AgentCreateRequestDict],
    ) -> None:
        self.config: GufoConfig = GufoConfig.from_toml(**data)
        session = NotteSession(window=window, enable_perception=True)
        super().__init__(session=session)

        self.step_callback: Callable[[str, NotteStepAgentOutput], None] | None = step_callback
        self.tracer: LlmUsageDictTracer = LlmUsageDictTracer()
        self.vault: BaseVault | None = vault
        self.llm: LLMEngine = LLMEngine(model=self.config.reasoning_model, tracer=self.tracer)
        # Users should implement their own parser to customize how observations
        # and actions are formatted for their specific LLM and use case
        self.parser: GufoParser = GufoParser()
        self.prompt: GufoPrompt = GufoPrompt(self.parser)
        self.perception: GufoPerception = GufoPerception()
        self.conv: Conversation = Conversation()

        if self.vault is not None:
            # hide vault leaked credentials within llm inputs
            self.llm.structured_completion = self.vault.patch_structured_completion(0, self.vault.get_replacement_map)(  # pyright: ignore [reportAttributeAccessIssue]
                self.llm.structured_completion
            )

    async def reset(self):
        await self.session.areset()
        self.conv.reset()

    def output(self, answer: str, success: bool) -> AgentResponse:
        return AgentResponse(
            answer=answer,
            success=success,
            session_trajectory=self.session.trajectory,
            agent_trajectory=[],
            llm_usage=self.tracer.usage,
        )

    async def step(self, task: str) -> CompletionAction | None:
        # Processes the conversation history through the LLM to decide the next action.
        # logger.info(f"🤖 LLM prompt:\n{self.conv.messages()}")
        response: str = await self.llm.single_completion(self.conv.messages())
        self.conv.add_assistant_message(content=response)
        logger.info(f"🤖 LLM response:\n{response}")
        # Ask Notte to perform the selected action
        parsed_response = self.parser.parse(response)

        if parsed_response is None or parsed_response.action is None:
            self.conv.add_user_message(content=self.prompt.env_rules())
            return None

        if self.step_callback is not None:
            self.step_callback(task, parsed_response)

        if parsed_response.completion is not None:
            return parsed_response.completion
        action = parsed_response.action
        # Replace credentials if needed using the vault
        if self.vault is not None and self.vault.contains_credentials(action):
            locator = await self.session.locate(action)
            if locator is not None:
                action = self.vault.replace_credentials(
                    action,
                    await FalcoAgent.compute_locator_attributes(locator),
                    self.session.snapshot,
                )
        # Execute the action
        _ = await self.session.astep(action)
        obs = await self.session.aobserve()
        text_obs = self.perception.perceive(obs)
        self.conv.add_user_message(
            content=f"""
{text_obs}
{self.prompt.select_action_rules()}
{self.prompt.completion_rules()}
""",
            image=obs.screenshot if self.config.use_vision else None,
        )
        logger.info(f"🌌 Action successfully executed:\n{text_obs}")
        return None

    @override
    async def run(self, **kwargs: typing.Unpack[AgentRunRequestDict]) -> AgentResponse:
        """
        Main execution loop that coordinates between the LLM and Notte environment.

        This method shows a basic conversation flow. Consider customizing:
        1. The initial system prompt
        2. How observations are added to the conversation
        3. When and how to determine task completion
        4. Error handling and recovery strategies
        """
        task = kwargs.get("task")
        url = kwargs.get("url")
        logger.info(f"🚀 starting agent with task: {task} and url: {url}")
        system_msg = self.prompt.system(task, url)
        if self.vault is not None:
            system_msg += "\n" + self.vault.instructions()
        self.conv.add_system_message(content=system_msg)
        self.conv.add_user_message(self.prompt.env_rules())

        if self.vault is not None:
            self.session.window.screenshot_mask = VaultSecretsScreenshotMask(vault=self.vault)
        for i in range(self.config.max_steps):
            logger.info(f"> step {i}: looping in")
            output = await self.step(task=task)
            if output is not None:
                status = "😎 task completed sucessfully" if output.success else "👿 task failed"
                logger.info(f"{status} with answer: {output.answer}")
                return self.output(output.answer, output.success)
        # If the task is not done, raise an error
        error_msg = f"Failed to solve task in {self.config.max_steps} steps"
        logger.info(f"🚨 {error_msg}")
        return self.output(error_msg, False)
