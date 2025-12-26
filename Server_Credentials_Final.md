# 服务器部署关键信息备忘录

> 最后更新: 2025-12-26
> 版本: 2.0 (双轨制架构)
> VPS: 148.135.57.133 (racknerd-7655d0d)

---

## 1. 核心安全架构

### 1.1 防火墙 (UFW)

| 端口 | 状态 | 用途 |
|------|------|------|
| 22/tcp | ✅ 开放 | SSH |
| 80/tcp | ✅ 开放 | HTTP (NPM) |
| 443/tcp | ✅ 开放 | HTTPS (NPM) |
| 81/tcp | ⚠️ 按需开放 | NPM 管理界面 |
| 其他 | ❌ 拒绝 | 默认拒绝 |

### 1.2 访问方式

所有 Web 服务必须通过域名访问，直接 IP:端口 会被防火墙拦截。

---

## 2. 服务凭证清单

### 2.1 轨道 A: FastGPT Stack

#### FastGPT (demo.yansemei.com)
- 端口: 3001
- 账号: `root`
- 密码: `FastGPT2025Admin!`
- API Key: `sk-khvlnebzljzmhttquzghrbidptpygrzzoeymgpgfkklwltlw`

#### OneAPI (api.yansemei.com)
- 端口: 3002
- 账号: `root`
- 密码: `123456` ⚠️ 首次登录后修改!

#### 数据库
| 服务 | 端口 | 用户 | 密码 |
|------|------|------|------|
| PostgreSQL | 5432 | postgres | FastGPT2025Secure! |
| MongoDB | 27017 | root | FastGPT2025Secure! |
| Redis | 6379 | - | FastGPT2025Secure! |

#### FastGPT 内部密钥
- TOKEN_KEY: `fastgpt-token-key-2025-secure`
- ROOT_KEY: `fastgpt-root-key-2025-secure`
- FILE_TOKEN_KEY: `fastgpt-file-token-2025`

### 2.2 轨道 B: Huice Core

#### Agent Service (agent.yansemei.com)
- 端口: 2025
- API Key: `8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1`

#### RAG Core (kb.yansemei.com)
- 端口: 9621
- API Key: `75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa`

#### Chat UI (aurora.yansemei.com)
- 端口: 3000
- 认证: 公开访问

#### Admin UI (chat.yansemei.com)
- 端口: 5173
- 认证: LightRAG WebUI 内置登录

### 2.3 共享基础设施

#### n8n (flow.yansemei.com)
- 端口: 5678
- 认证: 首次访问创建账号

#### NPM (http://148.135.57.133:81)
- 账号: admin@example.com
- 密码: [你设置的密码]

### 2.4 云服务

#### SiliconFlow
- API Key: `sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt`
- Base URL: `https://api.siliconflow.cn/v1`

---

## 3. 域名路由表

| 域名 | 目标 | 用途 | 状态 |
|------|------|------|------|
| demo.yansemei.com | fastgpt:3001 | 客户友好入口 | 需修复 |
| api.yansemei.com | oneapi:3002 | 模型路由 | 需修复 |
| aurora.yansemei.com | chat-ui:3000 | Agent 演示 | ✅ 运行 |
| agent.yansemei.com | agent-service:2025 | Agent API | ✅ 运行 |
| chat.yansemei.com | admin-ui:5173 | 知识库管理 | ✅ 运行 |
| kb.yansemei.com | rag-core:9621 | RAG API | ✅ 运行 |
| flow.yansemei.com | n8n:5678 | 工作流 | ✅ 运行 |

---

## 4. 目录结构

```
/home/ai-stack/
├── yansemei-ai-stack/
│   └── huice/
│       ├── docker-compose.yml
│       ├── rag-core/
│       ├── mcp-server/
│       ├── agent-service/
│       ├── chat-ui/
│       ├── admin-ui/
│       ├── rag_storage/
│       └── inputs/
├── npm/
│   └── docker-compose.yml
└── n8n/
    └── docker-compose.yml
```

---

## 5. 常用运维命令

### 5.1 查看状态

```bash
# 所有容器
docker ps --format "table {{.Names}}\t{{.Status}}"

# 特定服务日志
docker logs fastgpt --tail 100
docker logs huice-agent-service --tail 100
```

### 5.2 重启服务

```bash
# FastGPT Stack
docker restart pg mongo redis oneapi fastgpt

# Huice Core
docker restart huice-rag-core huice-mcp huice-agent-service huice-chat-ui huice-admin-ui

# 全部重启
cd /home/ai-stack/yansemei-ai-stack/huice
docker compose restart
```

### 5.3 健康检查

```bash
curl https://demo.yansemei.com/api/health   # FastGPT
curl https://api.yansemei.com/api/status    # OneAPI
curl https://agent.yansemei.com/ok          # Agent
curl https://kb.yansemei.com/health         # RAG
```

### 5.4 NPM 管理

```bash
# 临时开放 81 端口
ufw allow from $(curl -s ifconfig.me) to any port 81

# 完成后关闭
ufw delete allow from $(curl -s ifconfig.me) to any port 81
```

---

## 6. 故障排查

### 6.1 FastGPT 502 错误

```bash
# 检查容器
docker ps -a | grep fastgpt

# 查看日志
docker logs fastgpt --tail 100

# 重启
docker restart pg mongo redis
sleep 10
docker restart fastgpt
```

### 6.2 OneAPI 无响应

```bash
# 检查容器
docker ps -a | grep oneapi

# 查看日志
docker logs oneapi --tail 100

# 重启
docker restart oneapi
```

---

## 7. 相关文档

- `System_Architecture_Huice_Yansemei.md` - 系统架构
- `huice/Security_Config_Record.md` - 安全配置
- `huice/.kiro/specs/vps-architecture-optimization/` - 优化规格

---

*最后更新: 2025-12-26*
