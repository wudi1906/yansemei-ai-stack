import os
from typing import Any, TypedDict

from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage
from langchain_core.messages.utils import count_tokens_approximately
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langmem.short_term import SummarizationNode, RunningSummary

os.environ["DEEPSEEK_API_KEY"] = "sk-b68ccb70b0934c4c80cb58a95f9cee00"
model = init_chat_model("deepseek:deepseek-chat")
summarization_model = model.bind(max_tokens=128)

class State(MessagesState):
    context: dict[str, RunningSummary]

class LLMInputState(TypedDict):
    summarized_messages: list[AnyMessage]
    context: dict[str, RunningSummary]

# max_tokens：控制最终输出的大小，确保输出不会超过这个限制。
# max_tokens_before_summary：控制何时触发总结，避免一次性处理过多消息。
# max_summary_tokens：控制总结消息的长度，确保总结不会过于冗长。
# 这三个参数共同作用，确保在处理大量消息时，既能有效地进行总结，又能保证最终输出的大小在可控范围内。
summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=summarization_model,
    max_tokens=256,
    max_tokens_before_summary=256,
    max_summary_tokens=128,
)

def call_model(state: LLMInputState):
    response = model.invoke(state["summarized_messages"])
    return {"messages": [response]}

checkpointer = InMemorySaver()
builder = StateGraph(State)
builder.add_node(call_model)
builder.add_node("summarize", summarization_node)
builder.add_edge(START, "summarize")
builder.add_edge("summarize", "call_model")
graph = builder.compile(checkpointer=checkpointer)

# Invoke the graph
config = {"configurable": {"thread_id": "1"}}
graph.invoke({"messages": "我的名字是AuroraAI"}, config)
graph.invoke({"messages": "写一首关于猫的短诗"}, config)
graph.invoke({"messages": "对狗也做同样的操作"}, config)
final_response = graph.invoke({"messages": "我的名字是什么？"}, config)

final_response["messages"][-1].pretty_print()
print("\nSummary:", final_response["context"]["running_summary"].summary)