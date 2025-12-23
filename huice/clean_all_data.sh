#!/bin/bash

# 清理所有历史数据脚本
# Copyright (c) 2025 Dean Wu. All rights reserved.

echo "🧹 清理所有历史数据..."
echo "================================"

# 1. 停止 RAG Core（避免文件占用）
echo "⏹️  停止 RAG Core..."
pkill -f "lightrag_server"
sleep 2

# 2. 清理 RAG Core 存储
echo "🗑️  清理 RAG Core 存储..."
rm -f rag-core/rag_storage/*.json
rm -f rag-core/rag_storage/*.graphml
echo "  ✓ 已清理 rag_storage"

# 3. 清理输入目录
echo "🗑️  清理输入目录..."
rm -rf rag-core/inputs/*
echo "  ✓ 已清理 inputs"

# 4. 清理 MCP Server 存储
echo "🗑️  清理 MCP Server 存储..."
rm -rf mcp-server/rag_storage/*
echo "  ✓ 已清理 mcp-server/rag_storage"

# 5. 重启 RAG Core
echo "🚀 重启 RAG Core..."
cd rag-core
python -m lightrag.api.lightrag_server --host 0.0.0.0 --port 9621 > /dev/null 2>&1 &
cd ..
sleep 3

echo ""
echo "✅ 清理完成！"
echo ""
echo "📊 验证："
echo "  curl http://localhost:9621/health"
echo ""
echo "🎯 下一步："
echo "  1. 访问 Admin UI: http://localhost:5173/webui/"
echo "  2. 上传新文档"
echo "  3. 测试 RAG 查询"
