"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import json
import os
import time
from pathlib import Path

from langchain_core.tools import tool


@tool
def get_available_collections() -> str:
    """
    获取所有可用的集合信息。
    返回所有可用的集合名称和描述，帮助选择合适的集合来查询知识。

    Returns:
        str: 包含所有集合信息的JSON字符串，每个集合包含name和description字段
    """
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
    import nest_asyncio
    import asyncio
    
    # 允许在已有事件循环中嵌套运行
    nest_asyncio.apply()
    
    # 从环境变量获取 MCP URL，默认使用 Docker 容器名
    mcp_url = os.environ.get("MCP_URL", "http://mcp:8001/sse")
    print(f"🔗 Connecting to MCP Server at: {mcp_url}")
    
    async def _fetch_tools():
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        client = MultiServerMCPClient(
            {
                "mcp-server-rag": {
                    "url": mcp_url,
                    "transport": "sse",
                }
            }
        )
        try:
            return await client.get_tools()
        except Exception as e:
            print(f"Error fetching tools: {e}")
            return []

    # 重试机制：最多尝试 5 次，每次间隔 2 秒
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # 使用 nest_asyncio 后可以安全调用 asyncio.run()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                tools = loop.run_until_complete(_fetch_tools())
            finally:
                loop.close()
            
            if tools:
                print(f"✅ Successfully loaded {len(tools)} MCP RAG tools:")
                for t in tools:
                    tool_desc = t.description[:50] + "..." if len(t.description) > 50 else t.description
                    print(f"   - {t.name}: {tool_desc}")
                return tools
            else:
                print(f"⚠️ MCP tools fetch attempt {attempt + 1}/{max_retries}: got empty list")
        except Exception as e:
            print(f"⚠️ MCP tools fetch attempt {attempt + 1}/{max_retries} failed: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2)
    
    print("❌ Failed to fetch MCP tools after all retries. RAG functionality will be unavailable!")
    return []
