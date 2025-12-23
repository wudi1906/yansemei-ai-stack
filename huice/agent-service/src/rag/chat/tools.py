"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from langchain_core.tools import tool
# type: ignore  MC8yOmFIVnBZMlhsa0xUb3Y2bzZiWEZJWmc9PTowYTVkNTIzOQ==

import asyncio
import json
import os
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import tool
# pylint: disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZiWEZJWmc9PTowYTVkNTIzOQ==

@tool
def get_available_collections() -> str:
    """
    获取所有可用的集合信息。
    返回所有可用的集合名称和描述，帮助选择合适的集合来查询知识。

    Returns:
        str: 包含所有集合信息的JSON字符串，每个集合包含name和description字段
    """
    # 获取当前文件所在目录
    current_dir = Path(__file__).parent
    collections_file = current_dir / "collections.json"

    try:
        with open(collections_file, 'r', encoding='utf-8') as f:
            collections = json.load(f)
        return json.dumps(collections, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        return json.dumps({"error": "collections.json文件不存在"}, ensure_ascii=False)
    except json.JSONDecodeError:
        return json.dumps({"error": "collections.json文件格式错误"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"读取集合信息失败: {str(e)}"}, ensure_ascii=False)

def get_mcp_rag_tools():
    """获取 MCP RAG 工具，带重试机制"""
    import time
    
    async def _fetch_tools():
        # langchain-mcp-adapters 0.1.0+ 新 API：不再使用 async with
        client = MultiServerMCPClient(
            {
                "mcp-server-rag": {
                    "url": "http://127.0.0.1:8001/sse",
                    "transport": "sse",
                }
            }
        )
        try:
            # 直接调用 get_tools()，不使用上下文管理器
            return await client.get_tools()
        except Exception as e:
            print(f"Error fetching tools: {e}")
            return []

    # 重试机制：最多尝试 5 次，每次间隔 2 秒
    max_retries = 5
    for attempt in range(max_retries):
        try:
            tools = asyncio.run(_fetch_tools())
            if tools:
                print(f"✅ Successfully loaded {len(tools)} MCP RAG tools:")
                for tool in tools:
                    tool_desc = tool.description[:50] + "..." if len(tool.description) > 50 else tool.description
                    print(f"   - {tool.name}: {tool_desc}")
                return tools
            else:
                print(f"⚠️ MCP tools fetch attempt {attempt + 1}/{max_retries}: got empty list")
        except Exception as e:
            print(f"⚠️ MCP tools fetch attempt {attempt + 1}/{max_retries} failed: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2)
    
    print("❌ Failed to fetch MCP tools after all retries. RAG functionality will be unavailable!")
    return []