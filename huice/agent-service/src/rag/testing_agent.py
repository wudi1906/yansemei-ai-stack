"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import asyncio
# noqa  MC8yOmFIVnBZMlhsa0xUb3Y2bzZUWEJ5ZEE9PTpkYWQ4NDBiMA==

from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from rag.chat.llms import deepseek_model
# pylint: disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZUWEJ5ZEE9PTpkYWQ4NDBiMA==

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
#
# client = MultiServerMCPClient(
#     {
#         "mcp-server-rag": {
#             "url": "http://127.0.0.1:8000/sse",
#             "transport": "sse",
#         }
#     }
# )
# tools = asyncio.run(client.get_tools())
# print(tools)
#
agent = create_react_agent(model=deepseek_model(),
                     tools=[add]
                     )