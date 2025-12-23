import asyncio
import os

from langchain.chat_models import init_chat_model
from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately
)
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
os.environ["DEEPSEEK_API_KEY"] = "sk-b68ccb70b0934c4c80cb58a95f9cee00"
model = init_chat_model("deepseek:deepseek-chat")

# This function will be called every time before the node that calls LLM
def pre_model_hook(state):
    # token = count_tokens_approximately(messages=state["messages"])
    trimmed_messages = trim_messages(
        state["messages"],
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=384,
        start_on="human",
        end_on=("human", "tool"),
    )
    return {"llm_input_messages": trimmed_messages}

checkpointer = InMemorySaver()
agent = create_react_agent(
    model,
    [],
    pre_model_hook=pre_model_hook,
    checkpointer=checkpointer,
)

config = {"configurable": {"thread_id": "1"}}
async def main():
    # Stream the agent
    async for chunk in agent.astream(
            {"messages": [{"role": "user", "content": "写一首关于冬天的文言文"}]},
            stream_mode="values",
            config=config
    ):
        if "messages" in chunk:
            chunk["messages"][-1].pretty_print()
    async for chunk in agent.astream(
            {"messages": [{"role": "user", "content": "再一首夏天的"}]},
            stream_mode="values",
            config=config
    ):
        if "messages" in chunk:
            chunk["messages"][-1].pretty_print()
if __name__ == "__main__":
    asyncio.run(main())