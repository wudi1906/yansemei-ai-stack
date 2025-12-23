#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 开始初始化项目环境...${NC}"

# 1. 安装 Python 依赖
echo -e "\n${GREEN}📦 安装核心 Python 依赖...${NC}"
# 优先使用 uv (如果已安装)，否则使用 pip
if command -v uv &> /dev/null; then
    echo "检测到 uv，使用 uv pip install..."
    uv pip install -e rag-core
    uv pip install -e mcp-server
    # Force reinstall agent-service to pick up new langchain version constraints
    uv pip install --force-reinstall -e agent-service
    uv pip install -U "mineru[core]" docling
else
    echo "使用标准 pip install..."
    pip install -e rag-core
    pip install -e mcp-server
    # Force reinstall agent-service to pick up new langchain version constraints
    pip install --force-reinstall -e agent-service
    pip install -U "mineru[core]" docling
fi

# 2. 安装前端依赖
echo -e "\n${GREEN}📦 安装前端依赖...${NC}"

echo "正在安装 Chat UI (用户前台) 依赖..."
cd chat-ui
if [ ! -f "package.json" ]; then
    echo "⚠️  Chat UI 目录似乎不完整，跳过..."
else
    # 优先使用 pnpm 或 bun，最后 npm
    if command -v bun &> /dev/null; then
        bun install
    elif command -v pnpm &> /dev/null; then
        pnpm install
    else
        npm install
    fi
fi
cd ..

echo "正在安装 Admin UI (管理后台) 依赖..."
cd admin-ui
if [ ! -f "package.json" ]; then
    echo "⚠️  Admin UI 目录似乎不完整，跳过..."
else
    if command -v bun &> /dev/null; then
        bun install
    elif command -v pnpm &> /dev/null; then
        pnpm install
    else
        npm install
    fi
fi
cd ..

# 3. 环境配置检查
echo -e "\n${GREEN}🔧 检查环境配置...${NC}"
if [ ! -f ".env" ]; then
    if [ -f "rag-core/.env.example" ]; then
        echo "生成根目录 .env (来源于 rag-core 模板)"
        cp rag-core/.env.example .env
    else
        echo "⚠️  未找到 .env 模板"
    fi
fi

echo -e "\n${BLUE}✨ 项目初始化完成! 请运行 python start_all.py 启动服务${NC}"
