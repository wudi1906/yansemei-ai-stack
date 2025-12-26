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

## 3. 服务访问地址与认证方式

### 3.1 轨道 A: FastGPT Stack

| 服务 | 域名 | 认证方式 |
|------|------|----------|
| FastGPT | https://demo.yansemei.com | FastGPT 内置登录 |
| OneAPI | https://api.yansemei.com | OneAPI 内置登录 |

### 3.2 轨道 B: Huice Core

| 服务 | 域名 | 认证方式 |
|------|------|----------|
| Chat UI | https://aurora.yansemei.com | 公开访问 |
| Admin UI | https://chat.yansemei.com | LightRAG WebUI 登录 |
| Agent API | https://agent.yansemei.com | API Key |
| RAG Core | https://kb.yansemei.com | API Key |

### 3.3 共享基础设施

| 服务 | 域名 | 认证方式 |
|------|------|----------|
| n8n | https://flow.yansemei.com | n8n 内置登录 |
| NPM 管理 | http://148.135.57.133:81 | NPM 内置登录 |

---

## 4. API Key 记录

### 4.1 Huice 服务

```bash
# Agent Service API Key
8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1

# RAG Core API Key
75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa
```

### 4.2 FastGPT

```bash
# FastGPT API Key
sk-khvlnebzljzmhttquzghrbidptpygrzzoeymgpgfkklwltlw
```

### 4.3 云服务

```bash
# SiliconFlow API Key
sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt
```

---

## 5. 外部 API 调用示例

### 5.1 调用 Agent Service

```bash
curl -X POST https://agent.yansemei.com/chat \
  -H "X-API-Key: 8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1" \
  -H "Content-Type: application/json" \
  -d '{"query": "你好"}'
```

### 5.2 调用 RAG Core

```bash
curl https://kb.yansemei.com/query \
  -H "X-API-Key: 75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa" \
  -H "Content-Type: application/json" \
  -d '{"query": "搜索内容"}'
```

### 5.3 调用 FastGPT

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

## 6. 防火墙管理

### 6.1 查看规则

```bash
ufw status verbose
```

### 6.2 临时开放 NPM 管理端口

```bash
# 获取你的公网 IP
curl ifconfig.me

# 允许你的 IP 访问 81 端口
ufw allow from YOUR_IP to any port 81

# 完成后关闭
ufw delete allow from YOUR_IP to any port 81
```

---

## 7. Fail2Ban 管理

```bash
# 查看状态
fail2ban-client status

# 查看 SSH 封禁列表
fail2ban-client status sshd

# 手动解封 IP
fail2ban-client set sshd unbanip IP_ADDRESS
```

---

## 8. 日志查看

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

## 9. 服务重启

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

## 10. 健康检查

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

## 11. 配置文件位置

| 文件 | 路径 |
|------|------|
| Agent Service 配置 | `/home/ai-stack/yansemei-ai-stack/huice/agent-service/.env` |
| RAG Core 配置 | `/home/ai-stack/yansemei-ai-stack/huice/rag-core/.env` |
| Docker Compose | `/home/ai-stack/yansemei-ai-stack/huice/docker-compose.yml` |
| UFW 规则 | `/etc/ufw/user.rules` |
| Fail2Ban 配置 | `/etc/fail2ban/jail.local` |

---

## 12. 密钥轮换指南

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

*最后更新: 2025-12-26*
