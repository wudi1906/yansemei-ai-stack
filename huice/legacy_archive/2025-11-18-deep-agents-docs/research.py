import asyncio
import os
from typing import Literal

from deepagents.backends import StateBackend, CompositeBackend, StoreBackend
from langchain.chat_models import init_chat_model
from langchain_core.stores import InMemoryStore
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Checkpointer
from tavily import TavilyClient
from deepagents import create_deep_agent
os.environ["TAVILY_API_KEY"] = "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"
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def web_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""
os.environ["DEEPSEEK_API_KEY"] = "sk-12fe20a839dc4a8f8f995c92cce35215"
model = init_chat_model("deepseek:deepseek-chat")
composite_backend = lambda rt: CompositeBackend(
    default=StateBackend(rt),
    routes={
        "/memories/": StoreBackend(rt),
    }
)
client = MultiServerMCPClient(
    {
        "chrome-devtools": {
            "transport": "stdio",  # Local subprocess communication
            "command": "npx",
            # Absolute path to your math_server.py file
            "args": ["-y", "@antv/mcp-server-chart"],
        }
    }
)


tools = asyncio.run(client.get_tools())

# check = InMemorySaver()
agent = create_deep_agent(
    model=model,
    tools=[web_search] + tools,
    system_prompt=research_instructions,
    # backend=composite_backend
)