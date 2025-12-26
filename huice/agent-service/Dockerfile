# Agent Service Dockerfile
# Copyright (c) 2025 Dean Wu. All rights reserved.
# AuroraAI Project.

FROM python:3.11-slim

WORKDIR /app

# 安装依赖（直接用 pip，不需要 uv）
RUN pip install --no-cache-dir \
    langchain>=0.3.0 \
    langchain-community>=0.3.0 \
    langchain-core>=0.3.0 \
    langchain-text-splitters>=0.3.0 \
    langchain-mcp-adapters>=0.1.0 \
    langgraph>=0.2.0 \
    langchain-openai>=0.1.0 \
    nest-asyncio>=1.6.0 \
    fastapi>=0.115.0 \
    uvicorn>=0.32.0 \
    python-dotenv>=1.0.0 \
    pydantic>=2.0.0

# 复制源代码
COPY . .

# 暴露端口
EXPOSE 2025

# 启动服务
CMD ["python", "start_server.py"]
