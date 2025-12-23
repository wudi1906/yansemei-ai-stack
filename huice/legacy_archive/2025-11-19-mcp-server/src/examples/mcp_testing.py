"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# server.py
from fastmcp import FastMCP
# type: ignore  MC8yOmFIVnBZMlhsa0xUb3Y2bzZOSGhYVFE9PTo5NmE2ZmUwYQ==

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
# fmt: off  MS8yOmFIVnBZMlhsa0xUb3Y2bzZOSGhYVFE9PTo5NmE2ZmUwYQ==

if __name__ == "__main__":
    mcp.run(transport="sse", port=8000, host="0.0.0.0")