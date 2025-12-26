#!/bin/bash
# ============================================
# VPS 系统恢复脚本
# 项目: Yansemei AI Stack (双轨制架构)
# 创建: 2025-12-26
# ============================================

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

BACKUP_DIR="/home/ai-stack/backups"
PROJECT_DIR="/home/ai-stack/yansemei-ai-stack"

# 检查参数
if [ -z "$1" ]; then
    echo -e "${YELLOW}用法: $0 <备份文件名>${NC}"
    echo ""
    echo "可用备份:"
    ls -lh "${BACKUP_DIR}"/*.tar.gz 2>/dev/null || echo "  无备份文件"
    exit 1
fi

BACKUP_FILE="$1"
if [[ ! "$BACKUP_FILE" == /* ]]; then
    BACKUP_FILE="${BACKUP_DIR}/${BACKUP_FILE}"
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}错误: 备份文件不存在: ${BACKUP_FILE}${NC}"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Yansemei AI Stack 系统恢复${NC}"
echo -e "${GREEN}  备份文件: ${BACKUP_FILE}${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${RED}⚠️  警告: 此操作将覆盖现有数据！${NC}"
read -p "确认继续? (输入 yes): " confirm
if [ "$confirm" != "yes" ]; then
    echo "已取消"
    exit 0
fi

# 解压备份
TEMP_DIR=$(mktemp -d)
echo -e "${YELLOW}[1/5] 解压备份文件...${NC}"
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
BACKUP_NAME=$(ls "$TEMP_DIR")
RESTORE_PATH="${TEMP_DIR}/${BACKUP_NAME}"

# 恢复配置文件
echo -e "${YELLOW}[2/5] 恢复配置文件...${NC}"
cp "${RESTORE_PATH}/configs/docker-compose.yml" "${PROJECT_DIR}/huice/"
cp "${RESTORE_PATH}/configs/fastgpt.env" "${PROJECT_DIR}/huice/"
cp "${RESTORE_PATH}/configs/fastgpt-config.json" "${PROJECT_DIR}/huice/"
cp "${RESTORE_PATH}/configs/.env" "${PROJECT_DIR}/huice/" 2>/dev/null || true
echo "  ✓ 配置文件已恢复"

# 恢复 MongoDB
echo -e "${YELLOW}[3/5] 恢复 MongoDB 数据库...${NC}"
docker cp "${RESTORE_PATH}/mongodb/dump" mongo:/restore
docker exec mongo mongorestore \
  -u root -p 'FastGPT2025Secure!' \
  --authenticationDatabase admin \
  --drop \
  /restore
docker exec mongo rm -rf /restore
echo "  ✓ MongoDB 已恢复"

# 恢复 PostgreSQL
echo -e "${YELLOW}[4/5] 恢复 PostgreSQL 数据库...${NC}"
cat "${RESTORE_PATH}/postgresql/all_databases.sql" | docker exec -i pg psql -U postgres
echo "  ✓ PostgreSQL 已恢复"

# 重启服务
echo -e "${YELLOW}[5/5] 重启所有服务...${NC}"
cd "${PROJECT_DIR}/huice"
docker-compose restart
echo "  ✓ 服务已重启"

# 清理
rm -rf "$TEMP_DIR"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ 恢复完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "请验证服务状态:"
echo "  docker ps"
echo "  访问 https://demo.yansemei.com"
