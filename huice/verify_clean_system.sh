#!/bin/bash

# 验证系统清理完成
echo "🔍 验证系统状态..."
echo "================================"
echo ""

# 1. 检查 RAG Core
echo "1️⃣  RAG Core 健康检查"
if curl -s http://localhost:9621/health > /dev/null; then
    echo "   ✅ RAG Core 运行正常"
else
    echo "   ❌ RAG Core 未运行"
    exit 1
fi

# 2. 检查文档数量
echo ""
echo "2️⃣  文档数量检查"
doc_count=$(curl -s -X POST http://localhost:9621/documents/paginated -H "Content-Type: application/json" -d '{"page":1,"page_size":10}' | python3 -c "import sys, json; print(json.load(sys.stdin)['pagination']['total_count'])" 2>/dev/null)
if [ "$doc_count" = "0" ]; then
    echo "   ✅ 文档数量: 0 (已清空)"
else
    echo "   ⚠️  文档数量: $doc_count (未完全清空)"
fi

# 3. 检查存储文件
echo ""
echo "3️⃣  存储文件检查"
storage_files=$(ls rag-core/rag_storage/*.json 2>/dev/null | wc -l)
if [ "$storage_files" -eq 0 ]; then
    echo "   ✅ 存储文件已清空"
else
    echo "   ℹ️  存储文件: $storage_files 个 (新建的空文件)"
fi

# 4. 检查所有服务
echo ""
echo "4️⃣  服务状态检查"
services=("RAG Core:9621" "MCP Server:8001" "Agent Service:2025" "Chat UI:3000" "Admin UI:5173")
for service in "${services[@]}"; do
    name="${service%:*}"
    port="${service#*:}"
    if lsof -i :$port > /dev/null 2>&1; then
        echo "   ✅ $name (:$port)"
    else
        echo "   ❌ $name (:$port) 未运行"
    fi
done

echo ""
echo "================================"
echo "✨ 系统验证完成！"
echo ""
echo "🎯 现在可以开始测试："
echo "   1. 访问 Admin UI: http://localhost:5173/webui/"
echo "   2. 上传 PDF 文档"
echo "   3. 访问 Chat UI: http://localhost:3000"
echo "   4. 测试 RAG 查询"
