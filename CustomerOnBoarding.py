import asyncio
import sys
import traceback
from pydantic import BaseModel, Field, InstanceOf
from beeai_framework import (
    AssistantMessage,
    BaseAgent,
    BaseMemory,
    Message,
    SystemMessage,
    UnconstrainedMemory,
    UserMessage,
)
from beeai_framework.adapters.ollama.backend.chat import OllamaChatModel
from beeai_framework.agents.react.types import ReActAgentRunInput, ReActAgentRunOptions
from beeai_framework.agents.types import AgentMeta
from beeai_framework.backend.chat import ChatModel
from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter
from beeai_framework.errors import FrameworkError
from beeai_framework.utils.models import ModelLike, to_model, to_model_optional


class State(BaseModel):
    thought: str
    final_answer: str


class RunOutput(BaseModel):
    message: InstanceOf[Message]
    state: State


class OnboardingAgent(BaseAgent[ReActAgentRunInput, ReActAgentRunOptions, RunOutput]):
    memory: BaseMemory | None = None

    def __init__(self, name: str, system_message: str, llm: ChatModel, memory: BaseMemory) -> None:
        self.model = llm
        self.memory = memory
        self.name = name
        self.system_message = system_message
        self.emitter = Emitter.root().child(namespace=["agent", name], creator=self)

    async def _run(self, run_input: ModelLike[ReActAgentRunInput], options: ModelLike[ReActAgentRunOptions] | None, context: RunContext) -> RunOutput:
        run_input = to_model(ReActAgentRunInput, run_input)
        options = to_model_optional(ReActAgentRunOptions, options)

        class CustomSchema(BaseModel):
            thought: str = Field(description="Describe your thought process before coming up with a final answer")
            final_answer: str = Field(description="Provide a concise answer to the original question.")

        response = await self.model.create_structure(
            schema=CustomSchema,
            messages=[
                SystemMessage(self.system_message),
                *(self.memory.messages if self.memory is not None else []),
                UserMessage(run_input.prompt or ""),
            ],
            max_retries=options.execution.total_max_retries if options and options.execution else None,
            abort_signal=context.signal,
        )

        result = AssistantMessage(response.object["final_answer"])
        await self.memory.add(result) if self.memory else None

        return RunOutput(
            message=result,
            state=State(thought=response.object["thought"], final_answer=response.object["final_answer"]),
        )

    @property
    def meta(self) -> AgentMeta:
        return AgentMeta(
            name=self.name,
            description=f"{self.name} is responsible for customer onboarding steps.",
            tools=[],
        )


async def main() -> None:
    llm = OllamaChatModel("granite3.1-dense:8b")
    memory = UnconstrainedMemory()

    personal_info_agent = OnboardingAgent(
        "Onboarding Personal Information Agent",
        "You are a helpful customer onboarding agent. Gather customer's name and location. Return 'TERMINATE' when done.",
        llm,
        memory,
    )
    topic_preference_agent = OnboardingAgent(
        "Onboarding Topic Preference Agent",
        "You are a helpful customer onboarding agent. Gather customer's preferences on news topics. Return 'TERMINATE' when done.",
        llm,
        memory,
    )
    engagement_agent = OnboardingAgent(
        "Customer Engagement Agent",
        "You are a customer service agent providing fun based on user data. Share fun facts, jokes, or interesting stories. Return 'TERMINATE' when done.",
        llm,
        memory,
    )

    user_input = "Hello, I'm here to help you get started with our product. Could you tell me your name and location?"
    response1 = await personal_info_agent.run(user_input)
    print(response1.state)

    user_input = "Great! Could you tell me what topics you are interested in reading about?"
    response2 = await topic_preference_agent.run(user_input)
    print(response2.state)

    user_input = "Let's find something fun to read."
    response3 = await engagement_agent.run(user_input)
    print(response3.state)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
