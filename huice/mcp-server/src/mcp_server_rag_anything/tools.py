"""
MCP Tools for RAG Anything Server

Implements all MCP tool functions for document processing and querying.
"""
"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# pragma: no cover  MC80OmFIVnBZMlhsa0xUb3Y2bzZNbE5JU3c9PTpiMTdjNjllMg==

import json
import logging
from typing import Optional, List, Dict, Any

from .rag_core_client import query_rag_core, get_rag_core_health, get_rag_core_documents

logger = logging.getLogger(__name__)


async def process_document_tool(
    connector,
    file_path: str,
    parse_method: Optional[str] = None,
) -> str:
    """
    Process a single document and insert into knowledge base

    Args:
        connector: RAGAnythingConnector instance
        file_path: Path to the document file
        parse_method: Parse method (auto, ocr, txt)

    Returns:
        Processing result as JSON string
    """
    result = await connector.process_document(file_path, parse_method=parse_method)
    return json.dumps(result, ensure_ascii=False, indent=2)


async def process_folder_tool(
    connector,
    folder_path: str,
    recursive: bool = True,
    parse_method: Optional[str] = None,
) -> str:
    """
    Process all documents in a folder

    Args:
        connector: RAGAnythingConnector instance
        folder_path: Path to the folder
        recursive: Whether to process subfolders
        parse_method: Parse method

    Returns:
        Processing result as JSON string
    """
    if not connector.rag_anything:
        return json.dumps(
            {"success": False, "error": "RAGAnything not initialized"},
            ensure_ascii=False,
        )

    try:
        # Use the correct method from RAGAnything framework
        result = await connector.rag_anything.process_folder_complete(
            folder_path,
            recursive=recursive,
            parse_method=parse_method or connector.config.rag.parse_method,
        )
        return json.dumps(
            {"success": True, "result": result, "folder": folder_path},
            ensure_ascii=False,
            indent=2,
        )
    except Exception as e:
        logger.error(f"Error processing folder: {e}")
        return json.dumps(
            {"success": False, "error": str(e)},
            ensure_ascii=False,
        )
# noqa  MS80OmFIVnBZMlhsa0xUb3Y2bzZNbE5JU3c9PTpiMTdjNjllMg==


async def query_tool(
    connector,
    query_text: str,
    mode: str = "hybrid",
    top_k: int = 10,
) -> str:
    """
    Execute a text query on the knowledge base
    
    直接调用 RAG Core API (9621端口)，确保与 Admin UI 共享同一个知识库。

    Args:
        connector: RAGAnythingConnector instance (保留兼容性，但不使用)
        query_text: The query text
        mode: Query mode (local, global, hybrid, naive, mix, bypass)
        top_k: Number of top results to return

    Returns:
        Query result as JSON string
    """
    # 直接调用 RAG Core API，而不是使用 connector
    # 这样可以确保查询的是 Admin UI 上传的文档
    result = await query_rag_core(query_text, mode=mode, top_k=top_k)
    return json.dumps(result, ensure_ascii=False, indent=2)


async def query_with_multimodal_tool(
    connector,
    query_text: str,
    multimodal_content: Optional[List[Dict[str, Any]]] = None,
    mode: str = "hybrid",
) -> str:
    """
    Execute a multimodal query (text + images/tables/equations)

    Args:
        connector: RAGAnythingConnector instance
        query_text: The query text
        multimodal_content: List of multimodal content
        mode: Query mode

    Returns:
        Query result as JSON string
    """
    if not connector.rag_anything:
        return json.dumps(
            {"success": False, "error": "RAGAnything not initialized"},
            ensure_ascii=False,
        )

    try:
        # Use the correct method from RAGAnything framework
        result = await connector.rag_anything.aquery_with_multimodal(
            query_text, multimodal_content=multimodal_content, mode=mode
        )
        return json.dumps(
            {"success": True, "result": result},
            ensure_ascii=False,
            indent=2,
        )
    except Exception as e:
        logger.error(f"Error in multimodal query: {e}")
        return json.dumps(
            {"success": False, "error": str(e)},
            ensure_ascii=False,
        )

# pylint: disable  Mi80OmFIVnBZMlhsa0xUb3Y2bzZNbE5JU3c9PTpiMTdjNjllMg==

async def get_config_tool(connector) -> str:
    """
    Get current configuration

    Args:
        connector: RAGAnythingConnector instance

    Returns:
        Configuration as JSON string
    """
    if connector.rag_anything:
        config_info = connector.rag_anything.get_config_info()
    else:
        config_info = connector.config.to_dict()

    return json.dumps(config_info, ensure_ascii=False, indent=2)


async def get_processor_status_tool(connector) -> str:
    """
    Get processor status and information

    Args:
        connector: RAGAnythingConnector instance

    Returns:
        Processor status as JSON string
    """
    if not connector.rag_anything:
        return json.dumps(
            {"success": False, "error": "RAGAnything not initialized"},
            ensure_ascii=False,
        )

    try:
        processor_info = connector.rag_anything.get_processor_info()
        return json.dumps(processor_info, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error getting processor status: {e}")
        return json.dumps(
            {"success": False, "error": str(e)},
            ensure_ascii=False,
        )


async def get_knowledge_base_stats_tool(connector) -> str:
    """
    Get knowledge base statistics
    
    直接从 RAG Core API 获取统计信息。

    Args:
        connector: RAGAnythingConnector instance (保留兼容性)

    Returns:
        Statistics as JSON string
    """
    try:
        # 获取 RAG Core 健康状态
        health = await get_rag_core_health()
        
        # 获取文档列表
        docs = await get_rag_core_documents()
        
        # 统计文档数量
        doc_count = 0
        if "statuses" in docs:
            for status, doc_list in docs["statuses"].items():
                if isinstance(doc_list, list):
                    doc_count += len(doc_list)
        
        stats = {
            "success": True,
            "rag_core_status": health.get("status", "unknown"),
            "document_count": doc_count,
            "configuration": health.get("configuration", {}),
        }
        return json.dumps(stats, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error getting knowledge base stats: {e}")
        return json.dumps(
            {"success": False, "error": str(e)},
            ensure_ascii=False,
        )

# type: ignore  My80OmFIVnBZMlhsa0xUb3Y2bzZNbE5JU3c9PTpiMTdjNjllMg==

async def list_supported_formats_tool(connector) -> str:
    """
    List supported file formats

    Args:
        connector: RAGAnythingConnector instance

    Returns:
        Supported formats as JSON string
    """
    supported_formats = {
        "documents": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt", ".md", ".html"],
        "images": [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif", ".webp"],
        "multimodal_processing": {
            "image": connector.config.rag.enable_image,
            "table": connector.config.rag.enable_table,
            "equation": connector.config.rag.enable_equation,
        },
    }
    return json.dumps(supported_formats, ensure_ascii=False, indent=2)
