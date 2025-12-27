"""
RAG Core API Client

直接调用 RAG Core API (9621端口) 进行查询，
而不是使用独立的 RAGAnything 实例。

这样可以确保 MCP Server 和 Admin UI 共享同一个知识库。
"""
"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import os
import logging
import aiohttp
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# RAG Core API 地址和认证
RAG_CORE_API_URL = os.getenv("RAG_CORE_API_URL", "http://127.0.0.1:9621")
RAG_CORE_API_KEY = os.getenv("RAG_CORE_API_KEY", "")


async def query_rag_core(
    query_text: str,
    mode: str = "mix",
    top_k: int = 10,
    timeout: int = 120,
) -> Dict[str, Any]:
    """
    通过 HTTP 调用 RAG Core API 进行查询
    
    Args:
        query_text: 查询文本
        mode: 查询模式 (local, global, hybrid, naive, mix, bypass)
        top_k: 返回结果数量
        timeout: 超时时间（秒）
    
    Returns:
        查询结果字典
    """
    url = f"{RAG_CORE_API_URL}/query"
    
    payload = {
        "query": query_text,
        "mode": mode,
        "top_k": top_k,
    }
    
    # 构建请求头，包含 API Key 认证
    headers = {}
    if RAG_CORE_API_KEY:
        headers["X-API-Key"] = RAG_CORE_API_KEY
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "response": result.get("response", ""),
                        "references": result.get("references", []),
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"RAG Core API error: {response.status} - {error_text}")
                    return {
                        "success": False,
                        "error": f"RAG Core API returned {response.status}: {error_text}",
                    }
    except aiohttp.ClientError as e:
        logger.error(f"RAG Core API connection error: {e}")
        return {
            "success": False,
            "error": f"无法连接到 RAG Core API: {str(e)}",
        }
    except Exception as e:
        logger.error(f"RAG Core API query error: {e}")
        return {
            "success": False,
            "error": str(e),
        }


async def get_rag_core_health() -> Dict[str, Any]:
    """
    检查 RAG Core API 健康状态
    
    Returns:
        健康状态信息
    """
    url = f"{RAG_CORE_API_URL}/health"
    
    # 构建请求头，包含 API Key 认证
    headers = {}
    if RAG_CORE_API_KEY:
        headers["X-API-Key"] = RAG_CORE_API_KEY
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"status": "unhealthy", "error": f"HTTP {response.status}"}
    except Exception as e:
        return {"status": "unreachable", "error": str(e)}


async def get_rag_core_documents() -> Dict[str, Any]:
    """
    获取 RAG Core 中的文档列表
    
    Returns:
        文档列表信息
    """
    url = f"{RAG_CORE_API_URL}/documents"
    
    # 构建请求头，包含 API Key 认证
    headers = {}
    if RAG_CORE_API_KEY:
        headers["X-API-Key"] = RAG_CORE_API_KEY
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"HTTP {response.status}"}
    except Exception as e:
        return {"error": str(e)}
