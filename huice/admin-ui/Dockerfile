# Admin UI Dockerfile (Vite + React - Development Mode)
# Copyright (c) 2025 Dean Wu. All rights reserved.
# AuroraAI Project.
#
# 注意：Admin UI 使用开发模式运行，因为它需要代理到 RAG Core

FROM node:20-alpine

WORKDIR /app

# 复制依赖文件
COPY package.json package-lock.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

EXPOSE 5173

# 使用开发模式运行（支持代理功能）
CMD ["npm", "run", "dev-no-bun", "--", "--host", "0.0.0.0"]
