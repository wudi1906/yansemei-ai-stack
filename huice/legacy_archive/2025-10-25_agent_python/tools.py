"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"{city}，今天是晴天，温度为 25 摄氏度。!"

def get_zhipu_search_mcp_tools():
    client = MultiServerMCPClient(
        {
            "search": {
                "url": "https://open.bigmodel.cn/api/mcp/web_search/sse?Authorization=0d3c7b3d55c84d6682663dbdbdb3d614.cpoJIoZ3NFaqXARQ",
                "transport": "sse",
            }
        }
    )
    tools = asyncio.run(client.get_tools())
    return tools



# tools = get_zhipu_search_mcp_tools()
# print(tools)