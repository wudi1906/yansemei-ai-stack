#!/bin/bash
# ============================================
# VPS 系统备份脚本
# 项目: Yansemei AI Stack (双轨制架构)
# 创建: 2025-12-26
# ============================================

set -e

# 配置
BACKUP_DIR="/home/ai-stack/backups"
PROJECT_DIR="/home/ai-stack/yansemei-ai-stack"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="yansemei_backup_${DATE}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Yansemei AI Stack 系统备份${NC}"
echo -e "${GREEN}  时间: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo -e "${GREEN}========================================${NC}"

# 创建备份目录
mkdir -p "${BACKUP_PATH}"
echo -e "${YELLOW}[1/8] 创建备份目录: ${BACKUP_PATH}${NC}"

# 1. 备份配置文件
echo -e "${YELLOW}[2/8] 备份配置文件...${NC}"
mkdir -p "${BACKUP_PATH}/configs"
cp "${PROJECT_DIR}/huice/docker-compose.yml" "${BACKUP_PATH}/configs/"
cp "${PROJECT_DIR}/huice/fastgpt.env" "${BACKUP_PATH}/configs/"
cp "${PROJECT_DIR}/huice/fastgpt-config.json" "${BACKUP_PATH}/configs/"
cp "${PROJECT_DIR}/huice/.env" "${BACKUP_PATH}/configs/" 2>/dev/null || true
cp -r "${PROJECT_DIR}/huice/rag-core/.env" "${BACKUP_PATH}/configs/rag-core.env" 2>/dev/null || true
cp -r "${PROJECT_DIR}/huice/agent-service/.env" "${BACKUP_PATH}/configs/agent-service.env" 2>/dev/null || true
echo "  ✓ 配置文件已备份"

# 2. 备份 MongoDB
echo -e "${YELLOW}[3/8] 备份 MongoDB 数据库...${NC}"
mkdir -p "${BACKUP_PATH}/mongodb"
docker exec mongo mongodump \
  -u root -p 'FastGPT2025Secure!' \
  --authenticationDatabase admin \
  --out /dump
docker cp mongo:/dump "${BACKUP_PATH}/mongodb/"
docker exec mongo rm -rf /dump
echo "  ✓ MongoDB 已备份"

# 3. 备份 PostgreSQL
echo -e "${YELLOW}[4/8] 备份 PostgreSQL 数据库...${NC}"
mkdir -p "${BACKUP_PATH}/postgresql"
docker exec pg pg_dumpall -U postgres > "${BACKUP_PATH}/postgresql/all_databases.sql"
echo "  ✓ PostgreSQL 已备份"

# 4. 备份 Redis (可选，通常不需要)
echo -e "${YELLOW}[5/8] 备份 Redis 数据...${NC}"
mkdir -p "${BACKUP_PATH}/redis"
docker exec redis redis-cli -a 'FastGPT2025Secure!' BGSAVE 2>/dev/null || true
sleep 2
docker cp redis:/data/dump.rdb "${BACKUP_PATH}/redis/" 2>/dev/null || echo "  ⚠ Redis 无持久化数据"
echo "  ✓ Redis 已备份"

# 5. 备份 NPM (Nginx Proxy Manager) 配置
echo -e "${YELLOW}[6/8] 备份 NPM 代理配置...${NC}"
mkdir -p "${BACKUP_PATH}/npm"
# NPM 数据通常在这些位置
if docker ps | grep -q npm; then
    docker cp npm:/data "${BACKUP_PATH}/npm/data" 2>/dev/null || true
    docker cp npm:/etc/letsencrypt "${BACKUP_PATH}/npm/letsencrypt" 2>/dev/null || true
    echo "  ✓ NPM 配置已备份"
else
    echo "  ⚠ NPM 容器未运行，跳过"
fi

# 6. 备份 RAG 存储数据
echo -e "${YELLOW}[7/8] 备份 RAG 存储数据...${NC}"
mkdir -p "${BACKUP_PATH}/rag"
cp -r "${PROJECT_DIR}/huice/rag_storage" "${BACKUP_PATH}/rag/" 2>/dev/null || true
cp -r "${PROJECT_DIR}/huice/inputs" "${BACKUP_PATH}/rag/" 2>/dev/null || true
echo "  ✓ RAG 数据已备份"

# 7. 记录系统状态
echo -e "${YELLOW}[8/8] 记录系统状态...${NC}"
cat > "${BACKUP_PATH}/system_info.txt" << EOF
========================================
系统备份信息
备份时间: $(date '+%Y-%m-%d %H:%M:%S')
========================================

【Docker 容器状态】
$(docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}")

【Docker 数据卷】
$(docker volume ls)

【磁盘使用】
$(df -h | grep -E "^/dev|Filesystem")

【Docker 镜像】
$(docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}")

【网络配置】
$(docker network ls)
EOF
echo "  ✓ 系统状态已记录"

# 压缩备份
echo -e "${YELLOW}正在压缩备份文件...${NC}"
cd "${BACKUP_DIR}"
tar -czf "${BACKUP_NAME}.tar.gz" "${BACKUP_NAME}"
rm -rf "${BACKUP_NAME}"

# 显示结果
BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" | cut -f1)
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ 备份完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "  备份文件: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
echo -e "  文件大小: ${BACKUP_SIZE}"
echo ""

# 列出所有备份
echo "【现有备份列表】"
ls -lh "${BACKUP_DIR}"/*.tar.gz 2>/dev/null || echo "  无备份文件"
echo ""

# 清理提示
BACKUP_COUNT=$(ls -1 "${BACKUP_DIR}"/*.tar.gz 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 5 ]; then
    echo -e "${YELLOW}⚠ 提示: 已有 ${BACKUP_COUNT} 个备份，建议清理旧备份${NC}"
    echo "  删除最旧备份: rm \$(ls -t ${BACKUP_DIR}/*.tar.gz | tail -1)"
fi
