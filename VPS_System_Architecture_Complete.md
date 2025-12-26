# VPS 系统架构完整文档

> 服务器: 148.135.57.133 (racknerd-7655d0d)
> 最后更新: 2025-12-26
> 架构: 双轨制 AI 交付平台

---

## 1. 系统概览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              互联网用户                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Nginx Proxy Manager (npm-app-1)                          │
│                        端口: 80/443 (公网) + 81 (管理)                        │
│                                                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │demo.yansemei│ │api.yansemei │ │aurora.yanse │ │agent.yanseme│            │
│  │   .com      │ │   .com      │ │  mei.com    │ │   i.com     │            │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘            │
│         │               │               │               │                    │
│  ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐            │
│  │chat.yansemei│ │kb.yansemei  │ │flow.yansemei│                            │
│  │   .com      │ │   .com      │ │   .com      │                            │
│  └─────────────┘ └─────────────┘ └─────────────┘                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
```


## 2. 双轨制架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           双轨制 AI 交付平台                                  │
├─────────────────────────────────┬───────────────────────────────────────────┤
│                                 │                                           │
│   ╔═══════════════════════════╗ │ ╔═══════════════════════════════════════╗ │
│   ║     轨道 A: FastGPT       ║ │ ║        轨道 B: Huice Core             ║ │
│   ║   (普通客户 $100-$500)    ║ │ ║     (高端客户 $500-$2000+)            ║ │
│   ╠═══════════════════════════╣ │ ╠═══════════════════════════════════════╣ │
│   ║                           ║ │ ║                                       ║ │
│   ║  ┌─────────────────────┐  ║ │ ║  ┌─────────────────────────────────┐  ║ │
│   ║  │     FastGPT         │  ║ │ ║  │      Agent Service              │  ║ │
│   ║  │  demo.yansemei.com  │  ║ │ ║  │   agent.yansemei.com:2025       │  ║ │
│   ║  │     端口: 3001      │  ║ │ ║  │   LangGraph Agent 大脑          │  ║ │
│   ║  └──────────┬──────────┘  ║ │ ║  └───────────────┬─────────────────┘  ║ │
│   ║             │             ║ │ ║                  │                    ║ │
│   ║             ▼             ║ │ ║                  ▼                    ║ │
│   ║  ┌─────────────────────┐  ║ │ ║  ┌─────────────────────────────────┐  ║ │
│   ║  │      OneAPI         │  ║ │ ║  │         MCP Server              │  ║ │
│   ║  │  api.yansemei.com   │  ║ │ ║  │        端口: 8001               │  ║ │
│   ║  │     端口: 3002      │  ║ │ ║  │      RAG 工具服务               │  ║ │
│   ║  └──────────┬──────────┘  ║ │ ║  └───────────────┬─────────────────┘  ║ │
│   ║             │             ║ │ ║                  │                    ║ │
│   ║             ▼             ║ │ ║                  ▼                    ║ │
│   ║  ┌─────────────────────┐  ║ │ ║  ┌─────────────────────────────────┐  ║ │
│   ║  │   云端 LLM API      │  ║ │ ║  │        RAG Core                 │  ║ │
│   ║  │ • SiliconFlow (主)  │  ║ │ ║  │    kb.yansemei.com:9621         │  ║ │
│   ║  │ • DeepSeek (备)     │  ║ │ ║  │   LightRAG 知识图谱引擎         │  ║ │
│   ║  └─────────────────────┘  ║ │ ║  └─────────────────────────────────┘  ║ │
│   ║                           ║ │ ║                                       ║ │
│   ╚═══════════════════════════╝ │ ╚═══════════════════════════════════════╝ │
│                                 │                                           │
└─────────────────────────────────┴───────────────────────────────────────────┘
```

---

## 3. 容器清单 (12个运行中)

| 容器名 | 镜像 | 端口 | 所属轨道 | 用途 |
|--------|------|------|----------|------|
| npm-app-1 | jc21/nginx-proxy-manager | 80,81,443 | 基础设施 | 反向代理 + SSL |
| fastgpt | fastgpt:v4.8.1 | 3001 | 轨道 A | 低代码 AI 应用平台 |
| oneapi | justsong/one-api | 3002 | 轨道 A | 模型路由与配额管理 |
| pg | pgvector/pgvector:pg15 | 5432 | 轨道 A | 向量数据库 |
| mongo | mongo:5.0.18 | 27017 | 轨道 A | 文档数据库 (Replica Set) |
| redis | redis:7-alpine | 6379 | 轨道 A | 缓存 |
| huice-agent-service | huice-agent-service | 2025 | 轨道 B | LangGraph Agent |
| huice-mcp | huice-mcp | 8001 | 轨道 B | MCP 工具服务 |
| huice-rag-core | huice-rag-core | 9621 | 轨道 B | LightRAG 知识图谱 |
| huice-chat-ui | huice-chat-ui | 3000 | 轨道 B | AuroraAI 对话界面 |
| huice-admin-ui | huice-admin-ui | 5173 | 轨道 B | 知识库管理界面 |
| n8n | n8nio/n8n:2.0.2 | 5678 | 共享 | 工作流自动化 |


---

## 4. 域名路由表

| 域名 | 目标容器 | 端口 | SSL | 用途 |
|------|----------|------|-----|------|
| demo.yansemei.com | fastgpt | 3001 | ✅ Let's Encrypt | FastGPT 客户入口 |
| api.yansemei.com | oneapi | 3002 | ✅ Let's Encrypt | 模型 API 网关 |
| aurora.yansemei.com | huice-chat-ui | 3000 | ✅ Let's Encrypt | Agent 演示界面 |
| agent.yansemei.com | huice-agent-service | 2025 | ✅ Let's Encrypt | Agent API |
| chat.yansemei.com | huice-admin-ui | 5173 | ✅ Let's Encrypt | 知识库管理 |
| kb.yansemei.com | huice-rag-core | 9621 | ✅ Let's Encrypt | RAG API |
| flow.yansemei.com | n8n | 5678 | ✅ Let's Encrypt | 工作流编辑器 |

---

## 5. 数据流向图

### 5.1 轨道 A: FastGPT 数据流

```
用户浏览器
    │
    │ HTTPS
    ▼
┌─────────────────┐
│ demo.yansemei   │
│     .com        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    FastGPT      │────▶│     OneAPI      │────▶│  SiliconFlow    │
│   (端口 3001)   │     │   (端口 3002)   │     │  云端 LLM API   │
└────────┬────────┘     └─────────────────┘     └─────────────────┘
         │                                              │
         │                                              │ (备用)
         │                                              ▼
         │                                      ┌─────────────────┐
         │                                      │    DeepSeek     │
         │                                      │  云端 LLM API   │
         │                                      └─────────────────┘
         │
    ┌────┴────┬─────────────┐
    ▼         ▼             ▼
┌───────┐ ┌───────┐   ┌───────────┐
│MongoDB│ │  PG   │   │   Redis   │
│(文档) │ │(向量) │   │  (缓存)   │
└───────┘ └───────┘   └───────────┘
```

### 5.2 轨道 B: Huice 数据流

```
用户浏览器
    │
    │ HTTPS
    ▼
┌─────────────────┐
│aurora.yansemei  │
│     .com        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Chat UI        │
│ (端口 3000)     │
└────────┬────────┘
         │
         │ HTTP (内部)
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Agent Service   │────▶│   MCP Server    │
│ (端口 2025)     │     │  (端口 8001)    │
└────────┬────────┘     └────────┬────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │   RAG Core      │
         │              │  (端口 9621)    │
         │              └────────┬────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │  rag_storage/   │
         │              │  (本地文件)     │
         │              └─────────────────┘
         │
         ▼
┌─────────────────┐
│  SiliconFlow    │
│  云端 LLM API   │
└─────────────────┘
```


---

## 6. 服务间调用关系

### 6.1 完整调用链路图

```
                                    ┌──────────────────────────────────────┐
                                    │           云端 LLM 服务               │
                                    │  ┌────────────┐  ┌────────────────┐  │
                                    │  │SiliconFlow │  │   DeepSeek     │  │
                                    │  │   (主力)   │  │    (备用)      │  │
                                    │  │api.silicon │  │api.deepseek.com│  │
                                    │  │ flow.com   │  │                │  │
                                    │  └─────▲──────┘  └───────▲────────┘  │
                                    └────────┼─────────────────┼───────────┘
                                             │                 │
                    ┌────────────────────────┼─────────────────┼────────────┐
                    │                        │                 │            │
                    │              ┌─────────┴─────────────────┴──────┐     │
                    │              │            OneAPI                 │     │
                    │              │      api.yansemei.com:3002        │     │
                    │              │   (模型路由 + 配额管理 + 负载均衡) │     │
                    │              └─────────────────▲─────────────────┘     │
                    │                                │                       │
                    │         ┌──────────────────────┼───────────────┐       │
                    │         │                      │               │       │
                    │         │                      │               │       │
┌───────────────────┼─────────┼──────────────────────┼───────────────┼───────┼───┐
│                   │         │                      │               │       │   │
│  ┌────────────────┴───┐  ┌──┴──────────────┐  ┌────┴────────┐  ┌───┴───┐   │   │
│  │     FastGPT        │  │  Agent Service  │  │  RAG Core   │  │  n8n  │   │   │
│  │ demo.yansemei.com  │  │agent.yansemei   │  │kb.yansemei  │  │ flow. │   │   │
│  │     :3001          │  │  .com:2025      │  │ .com:9621   │  │yanse  │   │   │
│  └─────────┬──────────┘  └────────┬────────┘  └──────▲──────┘  │mei.com│   │   │
│            │                      │                  │         └───────┘   │   │
│            │                      │                  │                     │   │
│            │                      ▼                  │                     │   │
│            │             ┌─────────────────┐         │                     │   │
│            │             │   MCP Server    │─────────┘                     │   │
│            │             │    :8001        │                               │   │
│            │             └─────────────────┘                               │   │
│            │                                                               │   │
│            │                                                               │   │
│  ┌─────────┴─────────────────────────────────────────────────────────┐     │   │
│  │                        数据库层                                    │     │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │     │   │
│  │  │   MongoDB    │  │  PostgreSQL  │  │    Redis     │             │     │   │
│  │  │   :27017     │  │    :5432     │  │    :6379     │             │     │   │
│  │  │  (Replica    │  │  (pgvector)  │  │   (缓存)     │             │     │   │
│  │  │    Set)      │  │              │  │              │             │     │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │     │   │
│  └───────────────────────────────────────────────────────────────────┘     │   │
│                                                                            │   │
│                              npm_default 网络                               │   │
└────────────────────────────────────────────────────────────────────────────┘   │
                                                                                 │
                                        VPS 148.135.57.133                       │
─────────────────────────────────────────────────────────────────────────────────┘
```


---

## 7. 各服务详细配置

### 7.1 轨道 A: FastGPT Stack

#### FastGPT (demo.yansemei.com)
- 镜像: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.8.1`
- 端口: 3001 → 3000
- 依赖: MongoDB, PostgreSQL, Redis, OneAPI
- 配置文件:
  - `fastgpt.env` - 环境变量
  - `fastgpt-config.json` - 模型配置

**环境变量:**
```
OPENAI_BASE_URL=http://oneapi:3000/v1
CHAT_API_KEY=sk-kLGqLaHr4OsT8i7oBdE99725Fe7b45F78d2bB97119831086
MONGODB_URI=mongodb://root:***@mongo:27017/fastgpt?authSource=admin
PG_URL=postgresql://postgres:***@pg:5432/fastgpt
REDIS_URL=redis://:***@redis:6379
```

**模型配置:**
| 模型 | 名称 | 用途 | 来源 |
|------|------|------|------|
| deepseek-ai/DeepSeek-V3 | DeepSeek-V3 (SiliconFlow) | 主力对话模型 | SiliconFlow |
| Qwen/Qwen2.5-7B-Instruct | Qwen2.5-7B (SiliconFlow) | 轻量对话模型 | SiliconFlow |
| deepseek-chat | DeepSeek-Chat (官方备用) | 备用模型 | DeepSeek |
| BAAI/bge-m3 | BGE-M3 (SiliconFlow) | 向量嵌入 | SiliconFlow |

#### OneAPI (api.yansemei.com)
- 镜像: `justsong/one-api:latest`
- 端口: 3002 → 3000
- 依赖: PostgreSQL, Redis
- 功能: 模型路由、配额管理、负载均衡

**渠道配置:**
| 渠道名 | Base URL | 优先级 | 模型 |
|--------|----------|--------|------|
| SiliconFlow (主力) | https://api.siliconflow.com | 高 | deepseek-ai/DeepSeek-V3, Qwen/Qwen2.5-7B-Instruct, BAAI/bge-m3 |
| DeepSeek (备用) | https://api.deepseek.com | 低 | deepseek-chat |

#### 数据库

**MongoDB (Replica Set 模式)**
- 镜像: `mongo:5.0.18`
- 端口: 27017
- 用户: root / FastGPT2025Secure!
- 特殊配置: `--replSet rs0 --keyFile /data/keyfile`
- 用途: FastGPT 文档存储、会话记录

**PostgreSQL (pgvector)**
- 镜像: `pgvector/pgvector:pg15`
- 端口: 5432
- 用户: postgres / FastGPT2025Secure!
- 数据库: fastgpt, oneapi
- 用途: 向量存储、OneAPI 数据

**Redis**
- 镜像: `redis:7-alpine`
- 端口: 6379
- 密码: FastGPT2025Secure!
- 用途: 缓存、会话管理


### 7.2 轨道 B: Huice Core

#### Agent Service (agent.yansemei.com)
- 镜像: 自建 `huice-agent-service`
- 端口: 2025
- 依赖: MCP Server, RAG Core, SiliconFlow API
- 功能: LangGraph Agent 大脑，处理复杂对话

**环境变量:**
```
API_KEY=8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1
SILICONFLOW_API_KEY=sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt
LLM_PROVIDER=siliconflow
```

**调用链:**
```
Chat UI → Agent Service → MCP Server → RAG Core
                ↓
          SiliconFlow API
```

#### MCP Server
- 镜像: 自建 `huice-mcp`
- 端口: 8001
- 依赖: RAG Core
- 功能: Model Context Protocol 工具服务

**环境变量:**
```
RAG_CORE_API_URL=http://rag-core:9621
```

#### RAG Core (kb.yansemei.com)
- 镜像: 自建 `huice-rag-core`
- 端口: 9621
- 依赖: SiliconFlow API (LLM + Embedding)
- 功能: LightRAG 知识图谱引擎

**环境变量:**
```
LLM_BINDING=openai
LLM_MODEL=deepseek-ai/DeepSeek-V3
LLM_BINDING_HOST=https://api.siliconflow.com/v1
EMBEDDING_MODEL=BAAI/bge-large-zh-v1.5
EMBEDDING_DIM=1024
WORKING_DIR=./rag_storage
LIGHTRAG_API_KEY=75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa
```

#### Chat UI (aurora.yansemei.com)
- 镜像: 自建 `huice-chat-ui`
- 端口: 3000
- 依赖: Agent Service
- 功能: AuroraAI 对话界面

**环境变量:**
```
NEXT_PUBLIC_API_URL=https://agent.yansemei.com
NEXT_PUBLIC_ASSISTANT_ID=chat_agent
```

#### Admin UI (chat.yansemei.com)
- 镜像: 自建 `huice-admin-ui`
- 端口: 5173
- 依赖: RAG Core
- 功能: LightRAG 知识库管理界面

**环境变量:**
```
VITE_BACKEND_URL=http://rag-core:9621
```

### 7.3 共享基础设施

#### n8n (flow.yansemei.com)
- 镜像: `n8nio/n8n:2.0.2`
- 端口: 5678 (仅本地监听)
- 功能: 工作流自动化
- 可调用: Agent Service, RAG Core, FastGPT

#### Nginx Proxy Manager
- 镜像: `jc21/nginx-proxy-manager`
- 端口: 80, 443 (公网), 81 (管理)
- 功能: 反向代理、SSL 证书管理


---

## 8. 网络架构

### 8.1 Docker 网络

所有服务都连接到 `npm_default` 网络，实现容器间通信：

```
┌─────────────────────────────────────────────────────────────────┐
│                      npm_default 网络                            │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │npm-app-1 │ │ fastgpt  │ │ oneapi   │ │   pg     │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │  mongo   │ │  redis   │ │   n8n    │ │huice-mcp │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │huice-rag │ │huice-chat│ │huice-    │ │huice-    │            │
│  │  -core   │ │   -ui    │ │admin-ui  │ │agent-svc │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 端口映射

| 容器 | 内部端口 | 外部端口 | 访问方式 |
|------|----------|----------|----------|
| npm-app-1 | 80,81,443 | 80,81,443 | 公网直接访问 |
| fastgpt | 3000 | 3001 | 通过 NPM 代理 |
| oneapi | 3000 | 3002 | 通过 NPM 代理 |
| pg | 5432 | 5432 | 仅内部访问 |
| mongo | 27017 | 27017 | 仅内部访问 |
| redis | 6379 | 6379 | 仅内部访问 |
| huice-agent-service | 2025 | 2025 | 通过 NPM 代理 |
| huice-mcp | 8001 | 8001 | 仅内部访问 |
| huice-rag-core | 9621 | 9621 | 通过 NPM 代理 |
| huice-chat-ui | 3000 | 3000 | 通过 NPM 代理 |
| huice-admin-ui | 5173 | 5173 | 通过 NPM 代理 |
| n8n | 5678 | 5678 (localhost) | 通过 NPM 代理 |

### 8.3 防火墙规则 (UFW)

| 端口 | 状态 | 用途 |
|------|------|------|
| 22/tcp | ✅ 开放 | SSH |
| 80/tcp | ✅ 开放 | HTTP |
| 443/tcp | ✅ 开放 | HTTPS |
| 81/tcp | ⚠️ 按需开放 | NPM 管理 |
| 其他 | ❌ 拒绝 | 默认拒绝 |


---

## 9. 数据存储

### 9.1 Docker 卷

| 卷名 | 用途 | 使用者 |
|------|------|--------|
| huice_pg_data | PostgreSQL 数据 | pg |
| huice_mongo_data | MongoDB 数据 | mongo |
| huice_redis_data | Redis 数据 | redis |
| huice_oneapi_data | OneAPI 数据 | oneapi |
| huice_rag_storage | RAG 知识图谱数据 | huice-rag-core |
| huice_rag_inputs | RAG 输入文件 | huice-rag-core |
| huice_mcp_storage | MCP 存储 | huice-mcp |

### 9.2 目录结构

```
/home/ai-stack/
├── yansemei-ai-stack/
│   └── huice/
│       ├── docker-compose.yml      # 主配置文件
│       ├── fastgpt.env             # FastGPT 环境变量
│       ├── fastgpt-config.json     # FastGPT 模型配置
│       ├── agent-service/          # Agent Service 源码
│       │   └── .env                # Agent 环境变量
│       ├── rag-core/               # RAG Core 源码
│       │   └── .env                # RAG 环境变量
│       ├── chat-ui/                # Chat UI 源码
│       ├── admin-ui/               # Admin UI 源码
│       ├── mcp-server/             # MCP Server 源码
│       ├── rag_storage/            # RAG 数据存储
│       └── inputs/                 # RAG 输入文件
├── mongo-keyfile/
│   └── keyfile                     # MongoDB Replica Set 密钥
├── npm/
│   └── docker-compose.yml          # NPM 配置
└── n8n/
    ├── docker-compose.yml          # n8n 配置
    └── data/                       # n8n 数据
```

---

## 10. API 密钥汇总

### 10.1 内部服务密钥

| 服务 | 密钥类型 | 值 |
|------|----------|-----|
| OneAPI | 令牌 | sk-kLGqLaHr4OsT8i7oBdE99725Fe7b45F78d2bB97119831086 |
| Agent Service | API Key | 8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1 |
| RAG Core | API Key | 75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa |

### 10.2 外部 API 密钥

| 服务 | Base URL | API Key |
|------|----------|---------|
| SiliconFlow | https://api.siliconflow.com | sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt |
| DeepSeek | https://api.deepseek.com | sk-ce1dd0750e824f369b4833c6ced9835a |

### 10.3 数据库凭证

| 数据库 | 用户 | 密码 |
|--------|------|------|
| PostgreSQL | postgres | FastGPT2025Secure! |
| MongoDB | root | FastGPT2025Secure! |
| Redis | - | FastGPT2025Secure! |

### 10.4 Web 界面凭证

| 服务 | URL | 用户 | 密码 |
|------|-----|------|------|
| FastGPT | demo.yansemei.com | root | FastGPT2025Admin! |
| OneAPI | api.yansemei.com | root | 123456 (需修改!) |
| NPM | 148.135.57.133:81 | wudi1906@gmail.com | [你设置的密码] |


---

## 11. 请求流程详解

### 11.1 FastGPT 对话请求流程

```
1. 用户访问 https://demo.yansemei.com
   │
2. NPM 接收请求，SSL 终止，转发到 fastgpt:3001
   │
3. FastGPT 处理请求
   │
   ├─► 查询 MongoDB (会话历史、应用配置)
   │
   ├─► 查询 PostgreSQL (向量检索，如果有知识库)
   │
   ├─► 查询 Redis (缓存)
   │
   └─► 调用 OneAPI (http://oneapi:3000/v1)
       │
       └─► OneAPI 路由到 SiliconFlow
           │
           └─► SiliconFlow 返回 LLM 响应
               │
               └─► 响应返回给用户
```

### 11.2 Huice Agent 对话请求流程

```
1. 用户访问 https://aurora.yansemei.com
   │
2. NPM 接收请求，SSL 终止，转发到 huice-chat-ui:3000
   │
3. Chat UI 发送请求到 Agent Service
   │   POST https://agent.yansemei.com/chat
   │   Headers: X-API-Key: 8809969...
   │
4. Agent Service (LangGraph) 处理请求
   │
   ├─► 判断是否需要 RAG
   │   │
   │   └─► 调用 MCP Server (http://mcp:8001)
   │       │
   │       └─► MCP 调用 RAG Core (http://rag-core:9621)
   │           │
   │           └─► RAG Core 查询知识图谱 (rag_storage/)
   │               │
   │               └─► 返回相关知识
   │
   └─► 调用 SiliconFlow API (直接调用，不经过 OneAPI)
       │
       └─► SiliconFlow 返回 LLM 响应
           │
           └─► Agent 组装最终响应
               │
               └─► 响应返回给用户
```

### 11.3 n8n 工作流调用 Huice

```
1. 用户在 https://flow.yansemei.com 创建工作流
   │
2. 工作流触发 (手动/定时/Webhook)
   │
3. HTTP Request 节点调用 Agent Service
   │   POST https://agent.yansemei.com/chat
   │   Headers: X-API-Key: 8809969...
   │   Body: {"query": "...", "thread_id": "..."}
   │
4. Agent Service 处理并返回结果
   │
5. n8n 继续执行后续节点
```

---

## 12. 健康检查命令

```bash
# 检查所有容器状态
docker ps --format "table {{.Names}}\t{{.Status}}"

# FastGPT
curl -s https://demo.yansemei.com | head -c 100

# OneAPI
curl -s https://api.yansemei.com/api/status

# Agent Service
curl -s https://agent.yansemei.com/ok

# RAG Core
curl -s https://kb.yansemei.com/health

# Chat UI
curl -s -o /dev/null -w "%{http_code}" https://aurora.yansemei.com

# Admin UI
curl -s -o /dev/null -w "%{http_code}" https://chat.yansemei.com

# n8n
curl -s -o /dev/null -w "%{http_code}" https://flow.yansemei.com
```

---

## 13. 常见运维操作

### 13.1 重启服务

```bash
# 重启 FastGPT Stack
docker restart pg mongo redis oneapi fastgpt

# 重启 Huice Core
docker restart huice-rag-core huice-mcp huice-agent-service huice-chat-ui huice-admin-ui

# 重启所有服务
cd /home/ai-stack/yansemei-ai-stack/huice
docker compose restart
```

### 13.2 查看日志

```bash
# FastGPT 日志
docker logs fastgpt --tail 100

# Agent Service 日志
docker logs huice-agent-service --tail 100

# RAG Core 日志
docker logs huice-rag-core --tail 100
```

### 13.3 更新代码

```bash
# 在 VPS 上
cd /home/ai-stack/yansemei-ai-stack
git pull

# 重建服务
cd huice
docker compose build --no-cache huice-agent-service
docker compose up -d huice-agent-service
```

---

*文档版本: 1.0*
*最后更新: 2025-12-26*
*作者: Kiro AI Assistant*
