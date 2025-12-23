"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# server.py
from fastmcp import FastMCP
# pylint: disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZNems1TlE9PTpiNjEzOTcxZg==

mcp = FastMCP("Demo 🚀")
# fmt: off  MS8yOmFIVnBZMlhsa0xUb3Y2bzZNems1TlE9PTpiNjEzOTcxZg==

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="sse", port=8000, host="0.0.0.0")