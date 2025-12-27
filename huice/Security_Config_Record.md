# Huice AI Platform - 安全配置记录

> 最后更新: 2025-12-26
> 版本: 2.0 (双轨制架构)
> VPS: 148.135.57.133 (racknerd-7655d0d)

---

## 1. 当前安全状态总览

| 安全层 | 状态 | 说明 |
|--------|------|------|
| 防火墙 (UFW) | ✅ 已启用 | 仅开放 22, 80, 443 端口 |
| 暴力破解防护 (Fail2Ban) | ✅ 已启用 | SSH 3次失败即封禁1小时 |
| API Key 认证 | ✅ 已配置 | Agent Service + RAG Core |
| HTTPS | ✅ 已启用 | 通过 NPM 自动管理 SSL 证书 |
| 健康检查 | ✅ 已配置 | 每5分钟自动检查 |

---

## 2. "瓶子"安全模型

```
┌─────────────────────────────────────────┐
│              互联网                      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         UFW 防火墙 (瓶壁)                │
│         只开放 22, 80, 443              │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         NPM + 应用登录 (瓶口)            │
│         FastGPT/n8n 内置登录            │
│         API Key 认证                    │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         Docker 内部网络 (瓶内)           │
│         服务间自由通信                   │
└─────────────────────────────────────────┘
```

---

## 3. 服务访问地址与登录凭据

### 3.1 轨道 A: FastGPT Stack

| 服务 | 域名 | 用户名 | 密码 |
|------|------|--------|------|
| FastGPT | https://demo.yansemei.com | root | FastGPT2025Admin! |
| OneAPI | https://api.yansemei.com | wudi1906 | wudi123456 |

### 3.2 轨道 B: Huice Core

| 服务 | 域名 | 用户名 | 密码 |
|------|------|--------|------|
| Chat UI | https://aurora.yansemei.com | 公开访问 | - |
| Admin UI | https://chat.yansemei.com | wudi1906 | wudi123456 |
| Agent API | https://agent.yansemei.com | API Key | 见下方 API Key 记录 |
| RAG Core | https://kb.yansemei.com | API Key | 见下方 API Key 记录 |

### 3.3 共享基础设施

| 服务 | 域名 | 用户名 | 密码 |
|------|------|--------|------|
| n8n | https://flow.yansemei.com | wudi1906@gmail.com | Wudi123456 |
| NPM 管理 | http://148.135.57.133:81 | wudi1906@gmail.com | wudi123456 |

---

## 4. 数据库凭据

### 4.1 基础设施数据库

| 服务 | 用户名 | 密码 |
|------|--------|------|
| PostgreSQL | postgres | FastGPT2025Secure! |
| MongoDB | root | FastGPT2025Secure! |
| Redis | - | FastGPT2025Secure! |

---

## 5. API Key 记录

### 5.1 Huice 服务

```bash
# Agent Service API Key
8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1

# RAG Core API Key
75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa
```

### 5.2 FastGPT

```bash
# FastGPT API Key
sk-khvlnebzljzmhttquzghrbidptpygrzzoeymgpgfkklwltlw
```

### 5.3 云服务

```bash
# SiliconFlow API Key
sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt

# OneAPI Token
sk-kLGqLaHr4OsT8i7oBdE99725Fe7b45F78d2bB97119831086
```

---

## 6. 外部 API 调用示例

### 6.1 调用 Agent Service

```bash
curl -X POST https://agent.yansemei.com/chat \
  -H "X-API-Key: 8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1" \
  -H "Content-Type: application/json" \
  -d '{"query": "你好"}'
```

### 6.2 调用 RAG Core

```bash
curl https://kb.yansemei.com/query \
  -H "X-API-Key: 75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa" \
  -H "Content-Type: application/json" \
  -d '{"query": "搜索内容"}'
```

### 6.3 调用 FastGPT

```bash
curl -X POST https://demo.yansemei.com/api/v1/chat/completions \
  -H "Authorization: Bearer sk-khvlnebzljzmhttquzghrbidptpygrzzoeymgpgfkklwltlw" \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "test",
    "stream": false,
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

---

## 7. 防火墙管理

### 7.1 查看规则

```bash
ufw status verbose
```

### 7.2 临时开放 NPM 管理端口

```bash
# 获取你的公网 IP
curl ifconfig.me

# 允许你的 IP 访问 81 端口
ufw allow from YOUR_IP to any port 81

# 完成后关闭
ufw delete allow from YOUR_IP to any port 81
```

---

## 8. Fail2Ban 管理

```bash
# 查看状态
fail2ban-client status

# 查看 SSH 封禁列表
fail2ban-client status sshd

# 手动解封 IP
fail2ban-client set sshd unbanip IP_ADDRESS
```

---

## 9. 日志查看

```bash
# FastGPT 日志
docker logs fastgpt --tail 100

# Agent Service 日志
docker logs huice-agent-service --tail 100

# RAG Core 日志
docker logs huice-rag-core --tail 100

# NPM 日志
docker logs npm-app-1 --tail 100
```

---

## 10. 服务重启

```bash
cd /home/ai-stack/yansemei-ai-stack/huice

# 重启 FastGPT Stack
docker restart pg mongo redis oneapi fastgpt

# 重启 Huice Core
docker restart huice-rag-core huice-mcp huice-agent-service huice-chat-ui huice-admin-ui

# 重启全部
docker compose restart
```

---

## 11. 健康检查

| 服务 | 检查命令 | 预期结果 |
|------|----------|----------|
| FastGPT | `curl https://demo.yansemei.com/api/health` | `{"status":"ok"}` |
| OneAPI | `curl https://api.yansemei.com/api/status` | `{"success":true}` |
| RAG Core | `curl https://kb.yansemei.com/health` | `{"status":"healthy"}` |
| Agent Service | `curl https://agent.yansemei.com/ok` | `{"status":"ok"}` |
| Chat UI | `curl -s -o /dev/null -w "%{http_code}" https://aurora.yansemei.com` | `200` |
| Admin UI | `curl -s -o /dev/null -w "%{http_code}" https://chat.yansemei.com` | `200` |
| n8n | `curl -s -o /dev/null -w "%{http_code}" https://flow.yansemei.com` | `200` |

---

## 12. 配置文件位置

| 文件 | 路径 |
|------|------|
| Agent Service 配置 | `/home/ai-stack/yansemei-ai-stack/huice/agent-service/.env` |
| RAG Core 配置 | `/home/ai-stack/yansemei-ai-stack/huice/rag-core/.env` |
| Docker Compose | `/home/ai-stack/yansemei-ai-stack/huice/docker-compose.yml` |
| n8n 配置 | `/home/ai-stack/n8n/docker-compose.yml` |
| UFW 规则 | `/etc/ufw/user.rules` |
| Fail2Ban 配置 | `/etc/fail2ban/jail.local` |

---

## 13. 密钥轮换指南

建议每 90 天轮换一次 API Key：

```bash
cd /home/ai-stack/yansemei-ai-stack/huice

# 生成新的 Agent Service API Key
NEW_AGENT_KEY=$(openssl rand -hex 32)
echo "新 Agent API Key: $NEW_AGENT_KEY"

# 更新配置
sed -i "s/^API_KEY=.*/API_KEY=$NEW_AGENT_KEY/" agent-service/.env

# 重启服务
docker restart huice-agent-service

# 更新所有使用该 Key 的客户端
```

---

*最后更新: 2025-12-27*
