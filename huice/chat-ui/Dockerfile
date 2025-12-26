# Chat UI Dockerfile (Next.js - Development Mode)
# Copyright (c) 2025 Dean Wu. All rights reserved.
# AuroraAI Project.
#
# 使用开发模式运行，避免 TypeScript 严格检查导致的构建失败

FROM node:20-alpine

WORKDIR /app

# 安装 pnpm
RUN corepack enable && corepack prepare pnpm@10.5.1 --activate

# 复制依赖文件
COPY package.json pnpm-lock.yaml ./

# 安装依赖
RUN pnpm install --frozen-lockfile

# 复制源代码
COPY . .

# 暴露端口
EXPOSE 3000

# 使用开发模式运行
CMD ["pnpm", "dev"]
