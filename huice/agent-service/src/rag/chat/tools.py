"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import json
import os
import time
import threading
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
    """获取 MCP RAG 工具，使用独立线程运行事件循环"""
    import asyncio
    
    # 从环境变量获取 MCP URL，默认使用 Docker 容器名
    mcp_base = os.environ.get("MCP_URL", "http://mcp:8001")
    # 确保 URL 以 /sse 结尾
    if not mcp_base.endswith("/sse"):
        mcp_url = mcp_base.rstrip("/") + "/sse"
    else:
        mcp_url = mcp_base
    print(f"🔗 Connecting to MCP Server at: {mcp_url}")
    
    tools_result = []
    error_result = [None]
    
    def run_in_thread():
        """在独立线程中运行异步代码"""
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
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(_fetch_tools())
            tools_result.extend(result)
        except Exception as e:
            error_result[0] = e
        finally:
            loop.close()
    
    # 重试机制：最多尝试 5 次，每次间隔 2 秒
    max_retries = 5
    for attempt in range(max_retries):
        try:
            tools_result.clear()
            error_result[0] = None
            
            # 在独立线程中运行，避免事件循环冲突
            thread = threading.Thread(target=run_in_thread)
            thread.start()
            thread.join(timeout=30)  # 30秒超时
            
            if thread.is_alive():
                print(f"⚠️ MCP tools fetch attempt {attempt + 1}/{max_retries}: timeout")
                continue
            
            if error_result[0]:
                print(f"⚠️ MCP tools fetch attempt {attempt + 1}/{max_retries} failed: {error_result[0]}")
            elif tools_result:
                print(f"✅ Successfully loaded {len(tools_result)} MCP RAG tools:")
                for t in tools_result:
                    tool_desc = t.description[:50] + "..." if len(t.description) > 50 else t.description
                    print(f"   - {t.name}: {tool_desc}")
                return list(tools_result)
            else:
                print(f"⚠️ MCP tools fetch attempt {attempt + 1}/{max_retries}: got empty list")
        except Exception as e:
            print(f"⚠️ MCP tools fetch attempt {attempt + 1}/{max_retries} failed: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2)
    
    print("❌ Failed to fetch MCP tools after all retries. RAG functionality will be unavailable!")
    return []
