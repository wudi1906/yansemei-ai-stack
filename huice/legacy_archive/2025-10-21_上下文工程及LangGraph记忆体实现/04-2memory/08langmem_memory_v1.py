import os

from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore

from langmem import create_manage_memory_tool, create_search_memory_tool
os.environ["DEEPSEEK_API_KEY"] = "sk-b68ccb70b0934c4c80cb58a95f9cee00"
os.environ["OLLAMA_HOST"] = "http://155.138.220.75:11434"
model = init_chat_model("deepseek:deepseek-chat")
embeddings = init_embeddings("ollama:qwen3-embedding:0.6b", base_url=os.environ["OLLAMA_HOST"])
store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1024,
    }
)

agent_a_tools = [
    # Write to agent-specific namespace
    create_manage_memory_tool(namespace=("memories", "team_a", "agent_a")),
    # Read from shared team namespace
    create_search_memory_tool(namespace=("memories", "team_a"))
]


# Agents with different prompts sharing read access
agent_a = create_react_agent(
    model,
    tools=agent_a_tools,
    store=store,
    prompt="You are a research assistant"
)

# Create tools for agent B with different write space
agent_b_tools = [
    create_manage_memory_tool(namespace=("memories", "team_a")),
    create_search_memory_tool(namespace=("memories", "team_a"))
]
agent_b = create_react_agent(
    model,
    tools=agent_b_tools,
    store=store,
    prompt="You are a report writer."
)

s = agent_b.invoke({"messages": [{"role": "user", "content": "我是AuroraAI，请记住我的名字"}]})
print(s)
s = agent_b.invoke({"messages": [{"role": "user", "content": "我是谁？"}]})
print(s)