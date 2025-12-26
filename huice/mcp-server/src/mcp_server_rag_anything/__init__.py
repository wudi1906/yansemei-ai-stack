"""
AuroraAI MCP RAG Server - Lightweight Version

通过 HTTP API 调用 RAG Core，提供 MCP 工具接口。

Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

__version__ = "0.2.0"
__author__ = "AuroraAI Team"

# 只导出需要的模块
from . import server
from . import rag_core_client

__all__ = ["server", "rag_core_client"]
