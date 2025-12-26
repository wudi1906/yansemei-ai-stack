# Huice + yansemei.com 完整系统架构设计

> 最后更新: 2025-12-26
> 版本: 2.0 (双轨制架构)
> 状态: 生产环境

---

## 1. 架构概述

### 1.1 核心策略：双轨制交付

我们采用"双轨制"策略，针对不同客户群体提供不同的交付物：

| 轨道 | 目标客户 | 交付物 | 价格范围 | 后续维护 |
|------|----------|--------|----------|----------|
| **轨道 A** | 普通客户（非技术人员） | FastGPT 应用 | $100-$500 | 客户自维护 |
| **轨道 B** | 高端客户（有技术团队） | Huice Agent | $500-$2000+ | 需要你维护 |

### 1.2 为什么采用双轨制？

**技术能力 ≠ 客户接受度**

| 维度 | FastGPT | Huice |
|------|---------|-------|
| 技术能力 | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐⭐ 强大 |
| 客户接受度 | ⭐⭐⭐⭐⭐ 高 | ⭐⭐⭐ 中等 |
| 学习曲线 | ⭐ 低 | ⭐⭐⭐ 高 |
| 品牌认知 | ✅ 有 | ❌ 无 |
| 客户自维护 | ✅ 可以 | ❌ 不行 |

---

## 2. 系统架构图

```
互联网用户
    │
    ▼
UFW 防火墙 (22, 80, 443) - VPS: 148.135.57.133
    │
    ▼
Nginx Proxy Manager (NPM) - 统一入口
    │
    ├── demo.yansemei.com   → FastGPT:3001      [客户友好入口]
    ├── api.yansemei.com    → OneAPI:3002       [模型路由层]
    ├── aurora.yansemei.com → chat-ui:3000      [高级Agent演示]
    ├── agent.yansemei.com  → agent-service:2025 [Agent API]
    ├── chat.yansemei.com   → admin-ui:5173     [知识库管理]
    ├── kb.yansemei.com     → rag-core:9621     [RAG API]
    └── flow.yansemei.com   → n8n:5678          [工作流引擎]
    │
    ▼
Docker 内部网络 (npm_default)
    │
    ├── 轨道 A: FastGPT Stack
    │   ├── FastGPT (可视化Flow, 知识库管理)
    │   ├── OneAPI (模型路由)
    │   ├── PostgreSQL (向量库)
    │   ├── MongoDB (文档库)
    │   └── Redis (缓存)
    │
    ├── 轨道 B: Huice Core
    │   ├── chat-ui (Agent调试)
    │   ├── agent-service (LangGraph Agent)
    │   ├── rag-core (LightRAG 知识图谱)
    │   ├── admin-ui (图谱管理)
    │   └── mcp (RAG工具)
    │
    └── 工作流引擎
        └── n8n (自动化, 定时任务, Webhook)
    │
    ▼
SiliconFlow 云模型
    DeepSeek-V3 (推理) + Qwen Embedding (向量)
```

---

## 3. 服务清单

### 3.1 轨道 A: FastGPT Stack

| 服务 | 容器名 | 端口 | 域名 | 用途 |
|------|--------|------|------|------|
| FastGPT | fastgpt | 3001 | demo.yansemei.com | 客户友好型 AI 应用 |
| OneAPI | oneapi | 3002 | api.yansemei.com | 模型路由与配额管理 |
| PostgreSQL | pg | 5432 | - | 向量数据库 |
| MongoDB | mongo | 27017 | - | 文档数据库 |
| Redis | redis | 6379 | - | 缓存 |

### 3.2 轨道 B: Huice Core

| 服务 | 容器名 | 端口 | 域名 | 用途 |
|------|--------|------|------|------|
| RAG Core | huice-rag-core | 9621 | kb.yansemei.com | LightRAG 知识图谱 |
| MCP Server | huice-mcp | 8001 | - | RAG 工具服务 |
| Agent Service | huice-agent-service | 2025 | agent.yansemei.com | LangGraph Agent |
| Chat UI | huice-chat-ui | 3000 | aurora.yansemei.com | Agent 对话界面 |
| Admin UI | huice-admin-ui | 5173 | chat.yansemei.com | 知识库管理 |

### 3.3 共享基础设施

| 服务 | 容器名 | 端口 | 域名 | 用途 |
|------|--------|------|------|------|
| n8n | n8n | 5678 | flow.yansemei.com | 工作流自动化 |
| NPM | npm-app-1 | 80/443/81 | - | 反向代理 + SSL |

---

## 4. 双轨制交付策略

### 4.1 轨道 A: FastGPT (客户友好型)

**目标客户**: 非技术人员, 小团队, 预算 $100-$500

**交付物特点**:
- 可视化 Flow 编辑器
- 图形化知识库管理
- 一键嵌入代码
- 多应用管理
- 品牌认知度高

**典型项目**:
- AI 客服机器人: $150-$300
- 企业 FAQ Bot: $200-$400
- 内部知识库: $300-$500

### 4.2 轨道 B: Huice (高级能力型)

**目标客户**: 有技术团队, 预算 $500-$2000+

**交付物特点**:
- LangGraph 多步推理
- MCP 工具集成
- 知识图谱 RAG
- 定制化开发
- 持续维护收入

**典型项目**:
- 智能分析 Agent: $500-$1000
- 多工具协作 Agent: $800-$1500
- 企业级 RAG 系统: $1000-$2000+

### 4.3 混合模式

FastGPT 作为前端，Huice 作为后端：
```
用户 → FastGPT → (复杂问题) → Huice Agent → 返回结果
```

---

## 5. 模型策略

统一使用 SiliconFlow：

| 用途 | 模型 |
|------|------|
| 推理 | deepseek-ai/DeepSeek-V3 |
| Embedding | BAAI/bge-m3 |
| 备选 | Qwen/Qwen2.5-7B-Instruct |

API Key: `sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt`

---

## 6. 安全架构

### 6.1 "瓶子"安全模型

- 瓶壁 = UFW 防火墙 (只开放 22, 80, 443)
- 瓶口 = 各应用的内置登录系统
- 瓶内 = Docker 内部网络

### 6.2 API Key

| 服务 | API Key |
|------|---------|
| Agent Service | `8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1` |
| RAG Core | `75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa` |
| SiliconFlow | `sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt` |
| FastGPT | `sk-khvlnebzljzmhttquzghrbidptpygrzzoeymgpgfkklwltlw` |

---

## 7. 运维指南

### 7.1 常用命令

```bash
# 查看容器状态
docker ps --format "table {{.Names}}\t{{.Status}}"

# 重启 FastGPT
docker restart pg mongo redis oneapi fastgpt

# 重启 Huice
docker restart huice-rag-core huice-mcp huice-agent-service huice-chat-ui huice-admin-ui

# 查看日志
docker logs <container_name> --tail 100
```

### 7.2 健康检查

```bash
curl https://demo.yansemei.com/api/health   # FastGPT
curl https://api.yansemei.com/api/status    # OneAPI
curl https://agent.yansemei.com/ok          # Agent
curl https://kb.yansemei.com/health         # RAG
```

---

## 8. 相关文档

- `huice/.kiro/specs/vps-architecture-optimization/` - 架构优化规格
- `Server_Credentials_Final.md` - 服务器凭证
- `huice/Security_Config_Record.md` - 安全配置记录
- `AI_Product_Packages.md` - 产品方案

---

*最后更新: 2025-12-26*
