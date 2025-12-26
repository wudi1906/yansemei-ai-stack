# MCP Server Dockerfile - Lightweight Version
# Copyright (c) 2025 Dean Wu. All rights reserved.
# AuroraAI Project.

FROM python:3.11-slim

WORKDIR /app

# 安装依赖（不需要 build-essential，因为没有需要编译的包）
RUN pip install --no-cache-dir \
    aiohttp>=3.9.0 \
    fastmcp>=2.0.0 \
    python-dotenv>=1.0.0 \
    httpx>=0.27.0

# 复制源代码
COPY huice/mcp-server/src ./src

# 设置 PYTHONPATH
ENV PYTHONPATH=/app/src

# 暴露端口
EXPOSE 8001

# 启动服务
CMD ["python", "-m", "mcp_server_rag_anything.server", "--sse", "--port", "8001"]
