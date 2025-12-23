import os

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.postgres import PostgresSaver

os.environ["DEEPSEEK_API_KEY"] = "sk-95a7b5cd98e34ba2ab07f00ca757b051"
model = init_chat_model("deepseek:deepseek-chat")
DB_URI = "postgresql://postgres:postgres@localhost:5432/langgraph_db?sslmode=disable"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # 创建初始化表
    # checkpointer.setup()

    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])
        return {"messages": response}

    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_edge(START, "call_model")

    graph = builder.compile(checkpointer=checkpointer)

    config = {
        "configurable": {
            "thread_id": "2"
        }
    }

    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": "你好，我是AuroraAI"}]},
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()

    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": "我是谁？"}]},
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()