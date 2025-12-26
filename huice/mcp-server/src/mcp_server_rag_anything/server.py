"""
AuroraAI MCP RAG Server - Lightweight Version

通过 HTTP API 调用 RAG Core，而不是直接导入 raganything。
这样可以大大简化依赖，加快构建速度。

Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import argparse
import json
import logging
import os

from fastmcp import FastMCP
from dotenv import load_dotenv

from mcp_server_rag_anything.rag_core_client import (
    query_rag_core,
    get_rag_core_health,
    get_rag_core_documents,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# MCP Server
mcp = FastMCP(name="AuroraAI企业级RAG")


@mcp.tool()
async def query(
    query_text: str,
    mode: str = "mix",
    top_k: int = 10,
) -> str:
    """
    在知识库中查询信息。

    Args:
        query_text: 查询文本，描述你想要查找的信息
        mode: 查询模式 (local=局部, global=全局, hybrid=混合, naive=朴素, mix=综合, bypass=直通)
        top_k: 返回结果数量

    Returns:
        查询结果，包含答案和相关引用
    """
    logger.info(f"Executing query: {query_text[:100]}... (mode: {mode})")
    
    result = await query_rag_core(query_text, mode=mode, top_k=top_k)
    
    if result.get("success"):
        return json.dumps({
            "answer": result.get("response", ""),
            "references": result.get("references", []),
        }, ensure_ascii=False, indent=2)
    else:
        return json.dumps({
            "error": result.get("error", "查询失败"),
        }, ensure_ascii=False)


@mcp.tool()
async def get_knowledge_base_status() -> str:
    """
    获取知识库状态信息。

    Returns:
        知识库健康状态和统计信息
    """
    health = await get_rag_core_health()
    docs = await get_rag_core_documents()
    
    return json.dumps({
        "health": health,
        "documents": docs,
    }, ensure_ascii=False, indent=2)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="AuroraAI MCP RAG Server")
    parser.add_argument("--sse", action="store_true", default=True, help="Enable SSE mode")
    parser.add_argument("--port", type=int, default=8001, help="Server port")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host")
    return parser.parse_args()


def main():
    """Main entry point"""
    load_dotenv()
    args = parse_arguments()

    logger.info(f"Starting AuroraAI MCP RAG Server on {args.host}:{args.port}")
    logger.info(f"RAG Core API: {os.getenv('RAG_CORE_API_URL', 'http://127.0.0.1:9621')}")

    if args.sse:
        mcp.run(transport="sse", port=args.port, host=args.host)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
