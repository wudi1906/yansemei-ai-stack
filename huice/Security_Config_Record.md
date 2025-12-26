# Huice AI Platform - 安全配置记录

> 配置日期: 2025-12-26
> 配置人员: Dean Wu
> VPS: racknerd-7655d0d

---

## 📊 当前安全状态总览

| 安全层 | 状态 | 说明 |
|--------|------|------|
| 防火墙 (UFW) | ✅ 已启用 | 仅开放 22, 80, 443 端口 |
| 暴力破解防护 (Fail2Ban) | ✅ 已启用 | SSH 3次失败即封禁1小时 |
| API Key 认证 | ✅ 已配置 | Agent Service + RAG Core |
| HTTPS | ✅ 已启用 | 通过 NPM 自动管理 SSL 证书 |
| 健康检查 | ✅ 已配置 | 每5分钟自动检查 |
| NPM 访问控制 | ⏳ 待配置 | 需要手动在 NPM 界面设置 |

---

## 🔑 密钥记录（请妥善保管）

### Agent Service API Key
```
8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1
```

### RAG Core API Key
```
75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa
```

### SiliconFlow API Key
```
sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt
```

> ⚠️ 重要：请将这些密钥保存到密码管理器中，不要泄露给他人！

---

## 🌐 服务访问地址

| 服务 | 域名 | 用途 | 认证方式 |
|------|------|------|----------|
| Admin UI | https://chat.yansemei.com/webui/ | 知识库管理 | NPM Basic Auth (待配置) |
| Chat UI | https://aurora.yansemei.com | AI 对话界面 | NPM Basic Auth (待配置) |
| Agent API | https://agent.yansemei.com | Agent 服务 API | API Key Header |
| RAG Core | https://kb.yansemei.com | 知识库 API | API Key Header |
| FastGPT | https://demo.yansemei.com | FastGPT 应用 | FastGPT 内置认证 |
| n8n | https://flow.yansemei.com | 工作流自动化 | n8n 内置认证 |
| NPM 管理 | http://VPS-IP:81 | 反向代理管理 | NPM 内置认证 |

---

## 🛡️ 安全架构说明

### 1. 网络层安全 (UFW 防火墙)

```
互联网 → [UFW 防火墙] → [Nginx Proxy Manager] → [Docker 容器]
              ↓
    仅允许: 22(SSH), 80(HTTP), 443(HTTPS)
    拒绝: 81, 3000, 3001, 5173, 2025, 8001, 9621 等内部端口
```

**当前规则：**
- ✅ 22/tcp (SSH) - 允许
- ✅ 80/tcp (HTTP) - 允许
- ✅ 443/tcp (HTTPS) - 允许
- ❌ 81/tcp (NPM 管理) - 拒绝外部访问
- ❌ 其他端口 - 默认拒绝

### 2. 应用层安全 (API Key)

```
用户请求 → [NPM 反向代理] → [API Key 验证] → [服务处理]
                                  ↓
                          无效 Key → 401 Unauthorized
```

**API 调用示例：**
```bash
# Agent Service
curl -X POST https://agent.yansemei.com/chat \
  -H "X-API-Key: 8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1" \
  -H "Content-Type: application/json" \
  -d '{"query": "你好"}'

# RAG Core
curl https://kb.yansemei.com/query \
  -H "X-API-Key: 75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa" \
  -H "Content-Type: application/json" \
  -d '{"query": "搜索内容"}'
```

### 3. 入侵防护 (Fail2Ban)

```
SSH 登录尝试 → [Fail2Ban 监控] → 3次失败 → 封禁 IP 1小时
```

**查看封禁状态：**
```bash
fail2ban-client status sshd
```

---

## 📋 日常运维命令

### 查看服务状态
```bash
# 所有容器状态
docker ps --format "table {{.Names}}\t{{.Status}}"

# 健康检查
/home/ai-stack/health_check.sh

# 查看健康检查日志
tail -50 /var/log/huice_health.log
```

### 防火墙管理
```bash
# 查看规则
ufw status verbose

# 临时允许某 IP 访问 81 端口（NPM 管理）
ufw allow from YOUR_IP to any port 81

# 删除规则
ufw delete allow from YOUR_IP to any port 81
```

### Fail2Ban 管理
```bash
# 查看状态
fail2ban-client status

# 查看 SSH 封禁列表
fail2ban-client status sshd

# 手动解封 IP
fail2ban-client set sshd unbanip IP_ADDRESS
```

### 日志查看
```bash
# Agent Service 日志
docker logs huice-agent-service --tail 100

# RAG Core 日志
docker logs huice-rag-core --tail 100

# NPM 日志
docker logs npm-app-1 --tail 100
```

### 服务重启
```bash
cd /home/ai-stack/yansemei-ai-stack/huice

# 重启单个服务
docker restart huice-agent-service
docker restart huice-rag-core

# 重启所有 huice 服务
docker restart huice-rag-core huice-mcp huice-agent-service huice-chat-ui huice-admin-ui
```

---

## ⏳ 待完成：NPM 访问控制配置

### 步骤 1：临时开放 81 端口
```bash
# 获取你当前的公网 IP
curl ifconfig.me

# 临时允许你的 IP 访问 NPM 管理界面
ufw allow from YOUR_IP to any port 81
```

### 步骤 2：登录 NPM 管理界面
- 访问: http://你的VPS-IP:81
- 默认账号: admin@example.com
- 默认密码: changeme（首次登录后修改）

### 步骤 3：创建 Access List
1. 进入 **Access Lists** 标签
2. 点击 **Add Access List**
3. 配置：
   - Name: `Huice-Auth`
   - Authorization: 添加用户名密码
     - Username: `admin`
     - Password: `你的强密码`

### 步骤 4：应用到域名
1. 进入 **Proxy Hosts**
2. 编辑 `chat.yansemei.com`
3. 切换到 **Access** 标签
4. 选择 `Huice-Auth`
5. 保存
6. 对 `aurora.yansemei.com` 重复以上步骤

### 步骤 5：关闭 81 端口
```bash
ufw delete allow from YOUR_IP to any port 81
```

---

## 🔄 密钥轮换指南

建议每 90 天轮换一次 API Key：

```bash
cd /home/ai-stack/yansemei-ai-stack/huice

# 1. 生成新的 Agent Service API Key
NEW_AGENT_KEY=$(openssl rand -hex 32)
echo "新 Agent API Key: $NEW_AGENT_KEY"

# 2. 更新配置
sed -i "s/^API_KEY=.*/API_KEY=$NEW_AGENT_KEY/" agent-service/.env

# 3. 重启服务
docker restart huice-agent-service

# 4. 更新所有使用该 Key 的客户端
```

---

## 📝 配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| Agent Service 配置 | `/home/ai-stack/yansemei-ai-stack/huice/agent-service/.env` | API Key 等 |
| RAG Core 配置 | `/home/ai-stack/yansemei-ai-stack/huice/rag-core/.env` | 模型配置、API Key |
| Docker Compose | `/home/ai-stack/yansemei-ai-stack/huice/docker-compose.yml` | 容器编排 |
| UFW 规则 | `/etc/ufw/user.rules` | 防火墙规则 |
| Fail2Ban 配置 | `/etc/fail2ban/jail.local` | 入侵防护配置 |
| 健康检查脚本 | `/home/ai-stack/health_check.sh` | 自动健康检查 |
| 健康检查日志 | `/var/log/huice_health.log` | 检查结果日志 |

---

*最后更新: 2025-12-26*
