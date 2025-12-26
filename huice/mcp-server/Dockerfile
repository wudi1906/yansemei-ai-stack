# MCP Server Dockerfile
# Copyright (c) 2025 Dean Wu. All rights reserved.
# AuroraAI Project.

FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY huice/mcp-server/pyproject.toml ./
COPY huice/mcp-server/uv.lock ./

# 安装 uv 并安装依赖
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache -r pyproject.toml

# 复制源代码
COPY huice/mcp-server/src ./src

# 设置 PYTHONPATH
ENV PYTHONPATH=/app/src

# 暴露端口
EXPOSE 8001

# 启动服务
CMD ["python", "-m", "mcp_server_rag_anything.server", "--sse", "--port", "8001"]
