# Multi-Agent Conversation: Platon and Kant discussing how the world would look like if an AI govern a country

## Setup

from utils import get_openai_api_key
OPENAI_API_KEY = get_openai_api_key()
llm_config = {"model": "gpt-3.5-turbo"}

## Define an AutoGen agent

from autogen import ConversableAgent

agent = ConversableAgent(
    name="chatbot",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

reply = agent.generate_reply(
    messages=[{"content": "Ask me a question about what would happen if an AI was governing a country.", "role": "user"}]
)
print(reply)

reply = agent.generate_reply(
    messages=[{"content": "Repeat the question.", "role": "user"}]
)
print(reply)

## Conversation

Setting up a conversation between two agents, Platon and Kant, where the memory of their interactions is retained.

platon = ConversableAgent(
    name="platon",
    system_message=
    "Your name is Platon and you are Platon, the phylosopher."
    "Ask questions about what would happen if an AI would govern a country",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

kant = ConversableAgent(
    name="kant",
    system_message=
    "Your name is Kant and you are Kant, the phylosopher "
    "Give answer to the questions you receive.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)


chat_result = platon.initiate_chat(
    recipient=kant, 
    message="I'm Platon. Kant, let's explore how the world would like if an AI will govern a country",
    max_turns=2,
)

## Print some results

You can print out:

1. Chat history
2. Cost
3. Summary of the conversation

import pprint

pprint.pprint(chat_result.chat_history)

pprint.pprint(chat_result.cost)

pprint.pprint(chat_result.summary)

## Get a better summary of the conversation

chat_result = platon.initiate_chat(
    kant, 
    message="I'm Platon. Kant, let's explore how the world would like if an AI will govern a country",
    max_turns=2, 
    summary_method="reflection_with_llm",
    summary_prompt="Summarize the conversation",
)

pprint.pprint(chat_result.summary)

## Chat Termination

Chat can be terminated using a termination conditions.

kant = ConversableAgent(
    name="kant",
    system_message=
    "Your name is Kant and you are Kant, the phylosopher. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
)

platon = ConversableAgent(
    name="platon",
    system_message=
    "Your name is Platon and you are Platon, the phylosopher "
    "When you're ready to end the conversation, say 'I gotta go'.",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"] or "Goodbye" in msg["content"],
)

chat_result = platon.initiate_chat(
    recipient=kant,
    message="I'm Platon. Kant, let's explore whow the world look like if an AI govern a country."
)

kant.send(message="What's last question we talked about?", recipient=platon)
