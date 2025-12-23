import os

from langchain.chat_models import init_chat_model
from langchain_core.messages import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph

os.environ["DEEPSEEK_API_KEY"] = "sk-95a7b5cd98e34ba2ab07f00ca757b051"
model = init_chat_model("deepseek:deepseek-chat")
def delete_messages(state):
    messages = state["messages"]
    if len(messages) > 2:
        # remove the earliest two messages
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}

def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}

builder = StateGraph(MessagesState)
builder.add_sequence([call_model, delete_messages])
builder.add_edge(START, "call_model")

checkpointer = InMemorySaver()
app = builder.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "1"}}
for event in app.stream(
    {"messages": [{"role": "user", "content": "我是AuroraAI"}]},
    config,
    stream_mode="values"
):
    print([(message.type, message.content) for message in event["messages"]])

for event in app.stream(
    {"messages": [{"role": "user", "content": "我是谁?"}]},
    config,
    stream_mode="values"
):
    print([(message.type, message.content) for message in event["messages"]])