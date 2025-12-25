# Huice AI Platform - VPS 安全加固指南

## 📋 目录

1. [清理战场](#1-清理战场)
2. [Nginx Proxy Manager 访问控制](#2-nginx-proxy-manager-访问控制)
3. [API 安全配置](#3-api-安全配置)
4. [防火墙配置](#4-防火墙配置)
5. [Docker 安全加固](#5-docker-安全加固)
6. [监控与告警](#6-监控与告警)

---

## 1. 清理战场

### 1.1 清理调试文件（本地仓库）

以下文件是调试过程中产生的，可以删除：

```bash
# 在本地执行
cd huice

# 删除调试报告文件
rm -f 代码对比分析报告.md
rm -f 请求流程分析.md
rm -f 完整影响分析报告.md
rm -f 问题修复方案-Admin-UI.md
rm -f 系统清理完成.md
rm -f 项目功能与场景分析_扩展版.md
rm -f 项目功能与场景分析.md
rm -f 修改影响分析与改进.md
rm -f 运维记录-MCP-Agent-20251225.md
rm -f 最终问题分析.md
rm -f Admin-UI-503错误修复报告.md

# 删除测试脚本（如果不再需要）
rm -f ollama_concurrent_chat.py
rm -f ollama_ping.py
rm -f ollama_single_chat.py

# 删除日志文件
rm -f lightrag.log

# 提交清理
git add -A
git commit -m "chore: 清理调试文件和临时报告"
git push
```

### 1.2 VPS 清理命令

```bash
# 在 VPS 上执行
cd /home/ai-stack/yansemei-ai-stack/huice

# 拉取最新代码（包含清理）
git pull

# 清理 Docker 无用资源
docker system prune -af --volumes

# 清理旧的日志文件
find . -name "*.log" -type f -mtime +7 -delete

# 查看磁盘使用情况
df -h
du -sh /home/ai-stack/*
```

---

## 2. Nginx Proxy Manager 访问控制

### 2.1 创建 Access List（访问列表）

在 NPM 管理界面 (http://your-vps-ip:81) 中：

1. 进入 **Access Lists** 标签
2. 点击 **Add Access List**
3. 配置如下：

**Details 标签：**
- Name: `Huice-Admin-Auth`
- Satisfy Any: `关闭`（需要同时满足所有条件）

**Authorization 标签：**
- 添加用户名和密码：
  - Username: `admin`
  - Password: `你的强密码`（建议 16+ 字符，包含大小写、数字、特殊字符）

**Access 标签（可选 - IP 白名单）：**
- 如果你有固定 IP，可以添加：
  - Allow: `你的IP地址`
  - Deny: `all`

### 2.2 为各服务应用 Access List

在 NPM 的 **Proxy Hosts** 中，编辑每个需要保护的域名：

| 域名 | 是否需要认证 | 说明 |
|------|-------------|------|
| `chat.yansemei.com` (Admin UI) | ✅ 是 | 管理界面，必须保护 |
| `aurora.yansemei.com` (Chat UI) | ✅ 是 | 对话界面，建议保护 |
| `agent.yansemei.com` (Agent API) | ⚠️ API Key | 使用 API Key 认证 |
| `kb.yansemei.com` (RAG Core) | ⚠️ API Key | 使用 API Key 认证 |
| `demo.yansemei.com` (FastGPT) | ✅ 是 | FastGPT 自带认证 |
| `flow.yansemei.com` (n8n) | ✅ 是 | n8n 自带认证 |

**操作步骤：**
1. 点击域名右侧的 **⋮** → **Edit**
2. 切换到 **Access** 标签
3. 选择刚创建的 `Huice-Admin-Auth`
4. 保存

### 2.3 添加安全 Headers

在每个 Proxy Host 的 **Advanced** 标签中添加：

```nginx
# 安全 Headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

# 隐藏服务器信息
proxy_hide_header X-Powered-By;
server_tokens off;
```

---

## 3. API 安全配置

### 3.1 RAG Core API Key 认证

编辑 `rag-core/.env`，添加：

```bash
# API Key 认证
LIGHTRAG_API_KEY=your-secure-api-key-here-32chars

# 白名单路径（不需要认证的接口）
WHITELIST_PATHS=/health
```

### 3.2 Agent Service API Key 认证

在 `agent-service/.env` 中添加：

```bash
# API 认证
API_KEY=your-agent-service-api-key-here
```

修改 `agent-service/start_server.py`，添加 API Key 验证中间件：

```python
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY", "")

async def verify_api_key(x_api_key: str = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# 在需要保护的路由上添加依赖
@app.post("/chat", dependencies=[Depends(verify_api_key)])
async def chat(...):
    ...
```

### 3.3 Rate Limiting（速率限制）

在 NPM 的 Advanced 配置中添加：

```nginx
# 速率限制 - 每秒 10 个请求，突发 20 个
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req zone=api_limit burst=20 nodelay;
limit_req_status 429;

# 连接数限制
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
limit_conn conn_limit 10;
```

---

## 4. 防火墙配置

### 4.1 UFW 基础配置

```bash
# 安装 UFW（如果没有）
apt install ufw -y

# 默认策略：拒绝所有入站，允许所有出站
ufw default deny incoming
ufw default allow outgoing

# 允许 SSH（重要！先执行这个）
ufw allow 22/tcp

# 允许 HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# 允许 NPM 管理端口（建议限制 IP）
ufw allow from YOUR_IP to any port 81

# 启用防火墙
ufw enable

# 查看状态
ufw status verbose
```

### 4.2 禁止直接访问内部端口

确保以下端口只能通过 NPM 反向代理访问，不对外开放：

```bash
# 这些端口不应该对外开放
# 3000 - Chat UI
# 5173 - Admin UI
# 2025 - Agent Service
# 8001 - MCP Server
# 9621 - RAG Core

# 检查当前开放的端口
ufw status
netstat -tlnp
```

### 4.3 Fail2Ban 防暴力破解

```bash
# 安装 Fail2Ban
apt install fail2ban -y

# 创建本地配置
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5
ignoreip = 127.0.0.1/8

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 5

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
EOF

# 重启 Fail2Ban
systemctl restart fail2ban
systemctl enable fail2ban

# 查看状态
fail2ban-client status
```

---

## 5. Docker 安全加固

### 5.1 限制容器资源

在 `docker-compose.yml` 中为每个服务添加资源限制：

```yaml
services:
  rag-core:
    # ... 其他配置
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 5.2 使用非 root 用户运行容器

在 Dockerfile 中添加：

```dockerfile
# 创建非 root 用户
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser
```

### 5.3 只读文件系统（可选）

```yaml
services:
  rag-core:
    read_only: true
    tmpfs:
      - /tmp
```

---

## 6. 监控与告警

### 6.1 日志集中管理

```bash
# 创建日志目录
mkdir -p /var/log/huice

# 配置 Docker 日志驱动（在 docker-compose.yml 中）
services:
  rag-core:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 6.2 健康检查脚本

创建 `/home/ai-stack/health_check.sh`：

```bash
#!/bin/bash

WEBHOOK_URL="your-notification-webhook-url"  # 可选：钉钉/飞书/Slack webhook

check_service() {
    local name=$1
    local url=$2
    local expected=$3
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 10)
    
    if [ "$response" != "$expected" ]; then
        echo "[ALERT] $name is DOWN! Expected: $expected, Got: $response"
        # 可选：发送告警
        # curl -X POST "$WEBHOOK_URL" -d "{\"text\": \"$name is DOWN!\"}"
        return 1
    else
        echo "[OK] $name is healthy"
        return 0
    fi
}

echo "=== Health Check $(date) ==="
check_service "RAG Core" "http://localhost:9621/health" "200"
check_service "Agent Service" "http://localhost:2025/ok" "200"
check_service "Admin UI" "http://localhost:5173" "200"
check_service "Chat UI" "http://localhost:3000" "200"
check_service "MCP Server" "http://localhost:8001/sse" "200"
```

设置定时任务：

```bash
chmod +x /home/ai-stack/health_check.sh

# 添加 crontab（每 5 分钟检查一次）
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/ai-stack/health_check.sh >> /var/log/huice/health.log 2>&1") | crontab -
```

---

## 🔐 安全检查清单

执行完上述配置后，使用以下清单验证：

- [ ] 所有调试文件已清理
- [ ] Docker 无用资源已清理
- [ ] NPM Access List 已创建并应用
- [ ] 安全 Headers 已添加
- [ ] RAG Core API Key 已配置
- [ ] Agent Service API Key 已配置
- [ ] UFW 防火墙已启用
- [ ] 只有 22, 80, 443 端口对外开放
- [ ] Fail2Ban 已安装并运行
- [ ] 健康检查脚本已配置
- [ ] 所有服务使用 HTTPS

---

## 📝 密码管理建议

1. 使用密码管理器（如 1Password, Bitwarden）
2. 所有密码至少 16 字符
3. 定期轮换 API Key（建议每 90 天）
4. 不要在代码中硬编码密码
5. 使用 `.env` 文件管理敏感信息，确保 `.gitignore` 包含 `.env`

---

*最后更新: 2025-12-25*
