import os
from typing import Optional
# pip install langchain_ollama
from langchain.embeddings import init_embeddings
from langchain.chat_models import init_chat_model
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore
from langgraph.graph import START, MessagesState, StateGraph

os.environ["DEEPSEEK_API_KEY"] = "sk-b68ccb70b0934c4c80cb58a95f9cee00"
os.environ["OLLAMA_HOST"] = "http://155.138.220.75:11434"
model = init_chat_model("deepseek:deepseek-chat")

# Create store with semantic search enabled
# embeddings = init_embeddings("ollama:nomic-embed-text", base_url=os.environ["OLLAMA_HOST"])
embeddings = init_embeddings("ollama:qwen3-embedding:0.6b", base_url=os.environ["OLLAMA_HOST"])
# DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres_db?sslmode=disable"
# store_postgres = PostgresStore.from_conn_string(DB_URI, index={
#     "embed": embeddings,
#     "dims": 1024,
# })

store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1024,
    }
)

store.put(("user_123", "memories"), "1", {"text": "我喜欢吃肉夹馍"})
store.put(("user_123", "memories"), "2", {"text": "我是一名软件工程师"})

def chat(state, *, store: BaseStore):
    # Search based on user's last message
    items = store.search(
        ("user_123", "memories"), query=state["messages"][-1].content, limit=1
    )
    memories = "\n".join(item.value["text"] for item in items)
    memories = f"## Memories of user\n{memories}" if memories else ""
    response = model.invoke(
        [
            {"role": "system", "content": f"You are a helpful assistant.\n{memories}"},
            *state["messages"],
        ]
    )
    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node(chat)
builder.add_edge(START, "chat")
graph = builder.compile(store=store)

for message, metadata in graph.stream(
    input={"messages": [{"role": "user", "content": "我是一名python开发工程师，我该学习什么语言呢？"}]},
    stream_mode="messages",
):
    print(message.content, end="")