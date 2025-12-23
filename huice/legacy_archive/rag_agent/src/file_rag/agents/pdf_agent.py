"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import os

from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from langchain.agents import create_agent
from langgraph.store.memory import InMemoryStore

from file_rag.core.llms import deepseek_model

from langmem import create_manage_memory_tool, create_search_memory_tool
os.environ["DEEPSEEK_API_KEY"] = "sk-a9a724c109ed499a8f375a6fe46b3937"
os.environ["OLLAMA_HOST"] = "http://35.235.113.151:11434"
model = init_chat_model("deepseek:deepseek-chat")
embeddings = init_embeddings("ollama:qwen3-embedding:0.6b", base_url=os.environ["OLLAMA_HOST"])
store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1024,
    }
)

memory_tools = [
    # Write to agent-specific namespace
    create_manage_memory_tool(namespace=("memories", "user001")),
    # Read from shared team namespace
    create_search_memory_tool(namespace=("memories", "user001"))
]


def pre(state):
    print("pdf 文件内容：",state)

agent = create_agent(
    model=deepseek_model,
    tools=memory_tools,
    # store=store,
    system_prompt="你擅长基于用户提供的上下文信息回答用户问题。",
    name="pdf_chat_agent",
    # pre_model_hook=pre
)