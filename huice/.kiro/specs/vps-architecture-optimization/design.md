# VPS 架构优化设计文档

> 创建日期: 2025-12-26
> 状态: 进行中
> 目标: 实施双轨制交付策略，修复 FastGPT/OneAPI，优化整体架构

---

## 1. 设计概述

### 1.1 核心策略：双轨制交付

基于市场需求分析，我们采用"双轨制"策略：

- **轨道 A (FastGPT)**：面向普通客户，提供低代码、客户可自维护的交付物
- **轨道 B (Huice)**：面向高端客户，提供高级 AI Agent 能力

### 1.2 设计目标

1. 修复 FastGPT (demo.yansemei.com) - 当前 502 错误
2. 修复 OneAPI (api.yansemei.com) - 当前无响应
3. 集成 FastGPT 与 Huice，实现能力互补
4. 更新所有文档，保持一致性

---

## 2. 系统架构设计

### 2.1 完整架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              互联网用户                                      │
│                                                                              │
│    普通客户 (非技术人员)              高端客户 (有技术团队)                   │
│    预算: $100-$500                   预算: $500-$2000+                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         UFW 防火墙 (22, 80, 443)                             │
│                         VPS: 148.135.57.133                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Nginx Proxy Manager (NPM) - 统一入口                      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                           域名路由表                                     ││
│  │                                                                          ││
│  │  demo.yansemei.com   → FastGPT:3001      [客户友好入口] [需修复]        ││
│  │  api.yansemei.com    → OneAPI:3002       [模型路由层]   [需修复]        ││
│  │  aurora.yansemei.com → chat-ui:3000      [高级Agent演示] [已运行]       ││
│  │  agent.yansemei.com  → agent-service:2025 [Agent API]   [已运行]        ││
│  │  chat.yansemei.com   → admin-ui:5173     [知识库管理]   [已运行]        ││
│  │  kb.yansemei.com     → rag-core:9621     [RAG API]      [已运行]        ││
│  │  flow.yansemei.com   → n8n:5678          [工作流引擎]   [已运行]        ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Docker 内部网络 (npm_default)                           │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    轨道 A: 客户友好层 (FastGPT Stack)                   │  │
│  │                                                                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────┐  ┌─────────┐        │  │
│  │  │   FastGPT    │  │   OneAPI     │  │   pg    │  │  mongo  │        │  │
│  │  │    :3001     │  │    :3002     │  │  :5432  │  │ :27017  │        │  │
│  │  │              │  │              │  │         │  │         │        │  │
│  │  │ 可视化Flow   │  │ 模型路由     │  │ 向量库  │  │ 文档库  │        │  │
│  │  │ 知识库管理   │  │ 配额管理     │  │         │  │         │        │  │
│  │  │ 嵌入式部署   │  │ 成本监控     │  │         │  │         │        │  │
│  │  └──────┬───────┘  └──────┬───────┘  └─────────┘  └─────────┘        │  │
│  │         │                 │                                           │  │
│  │         │   HTTP 调用     │                                           │  │
│  │         ▼                 ▼                                           │  │
│  └─────────┼─────────────────┼───────────────────────────────────────────┘  │
│            │                 │                                               │
│  ┌─────────┼─────────────────┼───────────────────────────────────────────┐  │
│  │         │  轨道 B: 高级能力层 (Huice Core)                             │  │
│  │         │                 │                                            │  │
│  │  ┌──────▼───────┐  ┌──────▼──────────┐  ┌──────────┐  ┌─────────┐    │  │
│  │  │   chat-ui    │  │  agent-service  │  │ rag-core │  │admin-ui │    │  │
│  │  │    :3000     │  │     :2025       │  │   :9621  │  │  :5173  │    │  │
│  │  │              │  │                 │  │          │  │         │    │  │
│  │  │ Agent调试    │  │ LangGraph Agent │  │ LightRAG │  │ 图谱管理│    │  │
│  │  │ 高级演示     │  │ MCP工具调用     │  │ 知识图谱 │  │ 文档管理│    │  │
│  │  └──────────────┘  └────────┬────────┘  └──────────┘  └─────────┘    │  │
│  │                             │                                         │  │
│  │                             ▼                                         │  │
│  │                      ┌──────────┐                                     │  │
│  │                      │   mcp    │                                     │  │
│  │                      │  :8001   │                                     │  │
│  │                      │          │                                     │  │
│  │                      │ RAG工具  │                                     │  │
│  │                      └──────────┘                                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         工作流引擎层                                   │  │
│  │                                                                        │  │
│  │                      ┌──────────┐                                     │  │
│  │                      │   n8n    │                                     │  │
│  │                      │  :5678   │                                     │  │
│  │                      │          │                                     │  │
│  │                      │ 自动化   │                                     │  │
│  │                      │ 定时任务 │                                     │  │
│  │                      │ Webhook  │                                     │  │
│  │                      └──────────┘                                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SiliconFlow 云模型                                   │
│                                                                              │
│                    DeepSeek-V3 (推理) + Qwen Embedding (向量)                │
│                                                                              │
│                    API: https://api.siliconflow.cn/v1                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 服务清单

| 服务 | 容器名 | 端口 | 域名 | 状态 | 用途 |
|------|--------|------|------|------|------|
| FastGPT | fastgpt | 3001 | demo.yansemei.com | ❌ 需修复 | 客户友好型 AI 应用 |
| OneAPI | oneapi | 3002 | api.yansemei.com | ❌ 需修复 | 模型路由与配额管理 |
| PostgreSQL | pg | 5432 | - | ✅ 运行中 | FastGPT 向量库 |
| MongoDB | mongo | 27017 | - | ✅ 运行中 | FastGPT 文档库 |
| Redis | redis | 6379 | - | ✅ 运行中 | FastGPT 缓存 |
| RAG Core | huice-rag-core | 9621 | kb.yansemei.com | ✅ 运行中 | LightRAG 知识图谱 |
| MCP Server | huice-mcp | 8001 | - | ✅ 运行中 | RAG 工具服务 |
| Agent Service | huice-agent-service | 2025 | agent.yansemei.com | ✅ 运行中 | LangGraph Agent |
| Chat UI | huice-chat-ui | 3000 | aurora.yansemei.com | ✅ 运行中 | Agent 对话界面 |
| Admin UI | huice-admin-ui | 5173 | chat.yansemei.com | ✅ 运行中 | 知识库管理 |
| n8n | n8n | 5678 | flow.yansemei.com | ✅ 运行中 | 工作流自动化 |
| NPM | npm-app-1 | 80/443/81 | - | ✅ 运行中 | 反向代理 |

---

## 3. 双轨制交付策略详解

### 3.1 轨道 A: FastGPT (客户友好型)

**目标客户**：
- 非技术人员（创业者、运营、市场）
- 小团队（没有专职 AI 工程师）
- 预算有限（$100-$500）

**交付物特点**：
- ✅ 可视化 Flow 编辑器 - 客户可自己调整对话流程
- ✅ 图形化知识库管理 - 上传文档、管理 FAQ
- ✅ 一键嵌入代码 - 轻松集成到客户官网
- ✅ 多应用管理 - 为不同场景创建不同 Bot
- ✅ 品牌认知度高 - "FastGPT" 比自研系统更有信任度

**典型项目**：
| 项目类型 | 价格范围 | 交付内容 | 后续维护 |
|----------|----------|----------|----------|
| AI 客服机器人 | $150-$300 | FastGPT 应用 + 知识库 | 客户自维护 |
| 企业 FAQ Bot | $200-$400 | FastGPT 应用 + 嵌入代码 | 客户自维护 |
| 内部知识库 | $300-$500 | FastGPT 应用 + 培训 | 客户自维护 |

### 3.2 轨道 B: Huice (高级能力型)

**目标客户**：
- 有技术团队或愿意付费维护
- 需要复杂 AI 能力
- 预算充足（$500-$2000+）

**交付物特点**：
- ✅ LangGraph 多步推理 - 复杂任务分解与执行
- ✅ MCP 工具集成 - 调用外部 API 和服务
- ✅ 知识图谱 RAG - 比普通向量检索更智能
- ✅ 定制化开发 - 根据客户需求定制 Agent
- ✅ 持续维护收入 - 客户依赖你的技术支持

**典型项目**：
| 项目类型 | 价格范围 | 交付内容 | 后续维护 |
|----------|----------|----------|----------|
| 智能分析 Agent | $500-$1000 | Huice Agent + API | 需要你维护 |
| 多工具协作 Agent | $800-$1500 | Agent + MCP 工具 | 需要你维护 |
| 企业级 RAG 系统 | $1000-$2000+ | 完整 Huice 部署 | 需要你维护 |

### 3.3 混合模式: FastGPT + Huice

**适用场景**：
- 客户需要简单界面 + 高级能力
- FastGPT 作为前端，Huice 作为后端

**实现方式**：
```
用户 → FastGPT (简单问答)
         │
         │ 遇到复杂问题
         ▼
      FastGPT Flow (HTTP 节点)
         │
         │ 调用 Huice API
         ▼
      agent-service (复杂推理)
         │
         │ 返回结果
         ▼
      FastGPT (展示给用户)
```

---

## 4. 修复方案

### 4.1 FastGPT 修复方案

**当前问题**：demo.yansemei.com 返回 502 错误

**可能原因**：
1. FastGPT 容器未运行
2. FastGPT 配置错误
3. NPM 代理配置错误
4. 数据库连接问题

**诊断步骤**：
```bash
# 1. 检查容器状态
docker ps -a | grep -E "fastgpt|oneapi|pg|mongo|redis"

# 2. 查看 FastGPT 日志
docker logs fastgpt --tail 100

# 3. 检查 NPM 代理配置
# 访问 http://148.135.57.133:81 查看 demo.yansemei.com 的配置

# 4. 测试内部连接
docker exec -it fastgpt curl http://localhost:3001/api/health
```

**修复步骤**：
```bash
# 1. 进入 FastGPT 目录
cd /home/ai-stack/yansemei-ai-stack/huice

# 2. 查看 docker-compose 配置
cat docker-compose.yml | grep -A 20 fastgpt

# 3. 重启 FastGPT 相关服务
docker compose restart fastgpt oneapi pg mongo redis

# 4. 查看启动日志
docker logs -f fastgpt
```

### 4.2 OneAPI 修复方案

**当前问题**：api.yansemei.com 无响应

**可能原因**：
1. OneAPI 容器未运行
2. OneAPI 未配置 SiliconFlow 渠道
3. NPM 代理配置错误

**诊断步骤**：
```bash
# 1. 检查容器状态
docker ps -a | grep oneapi

# 2. 查看 OneAPI 日志
docker logs oneapi --tail 100

# 3. 测试内部连接
curl http://localhost:3002/api/status
```

**修复步骤**：
```bash
# 1. 重启 OneAPI
docker restart oneapi

# 2. 访问 OneAPI 管理界面配置 SiliconFlow
# http://api.yansemei.com (修复后)
# 或 http://148.135.57.133:3002 (直接访问)

# 3. 添加 SiliconFlow 渠道
# - 类型: OpenAI
# - Base URL: https://api.siliconflow.cn/v1
# - API Key: sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt
# - 模型: deepseek-ai/DeepSeek-V3, Qwen/Qwen2.5-7B-Instruct 等
```

---

## 5. 集成方案

### 5.1 FastGPT 调用 Huice Agent

在 FastGPT Flow 中添加 HTTP 节点，调用 agent-service：

**HTTP 节点配置**：
```json
{
  "url": "https://agent.yansemei.com/chat",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "X-API-Key": "8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1"
  },
  "body": {
    "query": "{{用户输入}}",
    "thread_id": "{{会话ID}}"
  }
}
```

### 5.2 n8n 调用 Huice Agent

在 n8n 工作流中添加 HTTP Request 节点：

**节点配置**：
```json
{
  "method": "POST",
  "url": "https://agent.yansemei.com/chat",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "options": {
    "headers": {
      "X-API-Key": "8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1"
    }
  },
  "bodyParameters": {
    "query": "={{$json.message}}",
    "thread_id": "={{$json.thread_id}}"
  }
}
```

---

## 6. 安全配置

### 6.1 API Key 管理

| 服务 | API Key | 用途 |
|------|---------|------|
| Agent Service | `8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1` | 外部调用 Agent API |
| RAG Core | `75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa` | 外部调用 RAG API |
| SiliconFlow | `sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt` | LLM 模型调用 |
| FastGPT | `sk-khvlnebzljzmhttquzghrbidptpygrzzoeymgpgfkklwltlw` | FastGPT API 调用 |

### 6.2 防火墙规则

```bash
# 当前 UFW 规则
ufw status verbose

# 应该只开放以下端口
22/tcp   - SSH
80/tcp   - HTTP (NPM)
443/tcp  - HTTPS (NPM)
81/tcp   - NPM 管理界面 (仅特定 IP)
```

---

## 7. 文件结构

### 7.1 VPS 目录结构

```
/home/ai-stack/
├── yansemei-ai-stack/
│   └── huice/
│       ├── docker-compose.yml      # 主编排文件
│       ├── .env                    # 环境变量
│       ├── rag-core/               # LightRAG
│       │   ├── .env
│       │   └── ...
│       ├── mcp-server/             # MCP 工具服务
│       ├── agent-service/          # LangGraph Agent
│       │   ├── .env
│       │   └── ...
│       ├── chat-ui/                # Agent 对话界面
│       ├── admin-ui/               # 知识库管理界面
│       ├── rag_storage/            # RAG 数据存储
│       ├── inputs/                 # 输入文档
│       └── Security_Config_Record.md
├── npm/                            # Nginx Proxy Manager
│   └── docker-compose.yml
└── n8n/                            # n8n 工作流
    └── docker-compose.yml
```

### 7.2 本地仓库结构

```
fiverr/
├── huice/                          # Huice 平台代码
│   ├── .kiro/
│   │   └── specs/
│   │       └── vps-architecture-optimization/
│   │           ├── requirements.md
│   │           ├── design.md
│   │           └── tasks.md
│   ├── docker-compose.yml
│   ├── Security_Config_Record.md
│   ├── VPS_Security_Guide.md
│   └── ...
├── System_Architecture_Huice_Yansemei.md  # 系统架构文档
├── Server_Credentials_Final.md            # 服务器凭证
├── AI_Product_Packages.md                 # 产品方案
├── Fiverr_Upwork_AI_Services_Top10_2025.md # 市场分析
└── ...
```

---

## 8. 测试验证

### 8.1 服务健康检查

| 服务 | 检查命令 | 预期结果 |
|------|----------|----------|
| FastGPT | `curl https://demo.yansemei.com/api/health` | `{"status":"ok"}` |
| OneAPI | `curl https://api.yansemei.com/api/status` | `{"success":true}` |
| RAG Core | `curl https://kb.yansemei.com/health` | `{"status":"healthy"}` |
| Agent Service | `curl https://agent.yansemei.com/ok` | `{"status":"ok"}` |
| Chat UI | `curl https://aurora.yansemei.com` | HTML 页面 |
| Admin UI | `curl https://chat.yansemei.com` | HTML 页面 |
| n8n | `curl https://flow.yansemei.com` | 登录页面 |

### 8.2 集成测试

**测试 FastGPT → Huice 调用**：
1. 在 FastGPT 中创建测试应用
2. 添加 HTTP 节点调用 agent-service
3. 发送测试消息，验证返回结果

**测试 n8n → Huice 调用**：
1. 在 n8n 中创建测试工作流
2. 添加 HTTP Request 节点调用 agent-service
3. 手动触发，验证返回结果

---

*设计文档版本: 1.0*
*最后更新: 2025-12-26*
