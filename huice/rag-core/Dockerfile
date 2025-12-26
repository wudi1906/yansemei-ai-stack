FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# 基础依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    poppler-utils \
    tesseract-ocr \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 先复制源码（动态版本 attr 需要模块可导入）
COPY lightrag ./lightrag
COPY raganything ./raganything
COPY pyproject.toml setup.py ./

# 装 CPU 版 torch/torchvision，再装本地包
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple torch==2.2.2 torchvision==0.17.2 && \
    pip install --no-cache-dir --no-build-isolation ".[api]"

# 对外端口（默认 9621）
EXPOSE 9621

# 正确的启动命令
CMD ["python", "-m", "lightrag.api.lightrag_server"]
