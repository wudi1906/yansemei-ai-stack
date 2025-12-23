import os

from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately
)
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, MessagesState
os.environ["DEEPSEEK_API_KEY"] = "sk-b68ccb70b0934c4c80cb58a95f9cee00"
model = init_chat_model("deepseek:deepseek-chat")
summarization_model = model.bind(max_tokens=128)

def call_model(state: MessagesState):
    messages = trim_messages(
        state["messages"],
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=128,
        start_on="human",
        end_on=("human", "tool"),
    )
    response = model.invoke(messages)
    return {"messages": [response]}

checkpointer = InMemorySaver()
builder = StateGraph(MessagesState)
builder.add_node(call_model)
builder.add_edge(START, "call_model")
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}
graph.invoke({"messages": "我的名字是AuroraAI"}, config)
graph.invoke({"messages": "写一首关于猫的短诗"}, config)
graph.invoke({"messages": "对狗也做同样的操作"}, config)
final_response = graph.invoke({"messages": "我的名字是什么？"}, config)

final_response["messages"][-1].pretty_print()