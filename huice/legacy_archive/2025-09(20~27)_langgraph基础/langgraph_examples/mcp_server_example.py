import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient(
    {
        "mcp-chart-http": {
            # Ensure you start your weather server on port 8000
            "url": "http://localhost:1122/mcp",
            "transport": "streamable_http",
        }
    }
)
client2 = MultiServerMCPClient(
    {
        "mcp-chart-sse": {
            # Ensure you start your weather server on port 8000
            "url": "http://localhost:1122/sse",
            "transport": "sse",
        }
    }
)

client3 = MultiServerMCPClient(
    {
        "mcp-server-chart": {
            "command": "npx",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["-y", "@antv/mcp-server-chart"],
            "transport": "stdio",
        }
    }
)

async def main():
    tools = await client3.get_tools()
    print(tools)


# ss = asyncio.run(client.get_tools())
# print(ss)
asyncio.run(main())