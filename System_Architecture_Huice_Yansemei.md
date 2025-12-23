# Huice + yansemei.com 完整新系统架构设计

## 1. 背景与目标

本文件记录当前阶段我们基于 **huice 项目 + yansemei.com 线上环境** 的统一架构设计与部署规划，目标是：

- **只维护一套代码与配置**，减少维护成本。
- 充分利用：
  - 本地 `huice/` 项目提供的 **LightRAG + LangGraph Agent + MCP 工具** 能力；
  - 线上 `demo.yansemei.com`（FastGPT）、`flow.yansemei.com`（n8n）、SiliconFlow 云模型。
- 打造一个：
  - **功能最完整**（RAG + Agent + 工作流 + 图谱）、
  - **性能可控**（关键并发参数可调）、
  - **智能性最高、可持续升级** 的统一平台。

---

## 2. 组件与角色划分

### 2.1 外部入口与上层平台

- **FastGPT（docker stack，`demo.yansemei.com`）**
  - 面向客户的应用层：知识库、应用编排（Flow）、对话入口、HTTP 模块。
  - 当前已接入 **SiliconFlow**（DeepSeek-V3 + Qwen3-Embedding-0.6B）。

- **n8n（`flow.yansemei.com`）**
  - 工作流与自动化引擎。
  - 通过 Webhook 接收 FastGPT 事件（问题+答案），执行：日志、通知、外部 API 调用等。

- **Nginx Proxy Manager（NPM）**
  - 对外统一入口与 SSL 终端：
    - `demo.yansemei.com` → FastGPT 容器（3001）；
    - `flow.yansemei.com` → n8n 容器（5678）；
    - `api.yansemei.com` → OneAPI 容器（3002，可选）。

### 2.2 核心智能引擎（huice 项目）

本地 `huice/` 目录提供一整套 **图谱 RAG + Agent 引擎**：

- **rag-core/**：LightRAG
  - 图谱 + 向量混合检索（`mode="mix"`）。
  - 支持多种 LLM/Embedding 提供方，通过 `env.example` 配置：
    - `LLM_BINDING=openai` + `LLM_BINDING_HOST` → 可对接 **SiliconFlow 的 OpenAI 兼容接口**；
    - `EMBEDDING_BINDING=openai` 同理；
    - 细粒度并发与 token 预算：`MAX_ASYNC`, `MAX_PARALLEL_INSERT`, `MAX_TOTAL_TOKENS`, `TOP_K` 等。

- **mcp-server/**：RAG 工具 MCP Server
  - `mcp_server_rag_anything/` 中：
    - `rag_core_client.py`：与 LightRAG API 通信；
    - `tools.py`：封装 `query`、文档写入、统计等为 MCP 工具；
    - `server.py`：以 SSE MCP Server 形式对外提供标准 Tool 接口。

- **agent-service/**：LangGraph Agent 大脑
  - `agent_rag_anything.py`：
    - 使用 `create_react_agent` 创建智能知识库 Agent；
    - 模型由 `get_model()` 决定（可配置为 DeepSeek-V3 等线上模型）；
    - 工具来自 `get_mcp_rag_tools()`（上面 MCP Server 注册的一组 RAG 工具）。

- **chat-ui/**：Agent Chat 前端
  - 基于 LangChain 官方 `agent-chat-ui`，Next.js 19 + Tailwind。
  - 面向“工程师/内部用户”的对话与调试界面。

- **admin-ui/**：LightRAG Web UI
  - 图谱可视化、文档管理、参数调优界面。

### 2.3 底层算力与存储

- **SiliconFlow**
  - 承担所有重型推理计算：DeepSeek-V3、Qwen Embedding 等。
  - VPS 只做编排和 I/O，不做本地大模型推理。

- **PostgreSQL / MongoDB / Redis**（FastGPT stack 内部）：
  - 向量、文档与缓存存储。

- **LightRAG 自身存储**（`rag-core/rag_storage/` 或 Postgres/Mongo/Neo4J）：
  - 知识图谱与向量数据，作为“离线知识工程”底层库。

### 2.4 统一模型策略（仅使用 SiliconFlow，无本地 LLM）

- **不在 VPS 上运行任何本地大模型服务**（如 Ollama 等），避免 CPU / 内存被推理任务占满。
- 全系统所有 LLM / Embedding 调用统一走 **SiliconFlow**：
  - FastGPT：已配置为使用 SiliconFlow 的 DeepSeek-V3 + Qwen3-Embedding-0.6B；
  - huice（rag-core + mcp-server + agent-service）：
    - 通过 `rag-core/.env` 与各自 `.env` 使用 `LLM_BINDING=openai` + `LLM_BINDING_HOST=https://api.siliconflow.com/v1`；
    - 统一使用 SiliconFlow 提供的 DeepSeek 系列模型作为主要推理模型；
    - 其他场景（如分类、抽取）可以按业务需要选用 SiliconFlow 中更高性价比的模型（如 Qwen 系列）。
  - n8n 中如需调用 LLM，也应通过 HTTP 调 SiliconFlow 接口或 OneAPI（未来的模型路由层）。
- 所有与 SiliconFlow 相关的 Key 通过 `.env` 管理，不在代码中明文硬编码，方便统一替换和安全管控。

### 2.4.1 DeepSeek 官方 API vs SiliconFlow DeepSeek（性价比分析）

目前我们有两种访问 DeepSeek 模型的路径：

- 直接使用 **DeepSeek 官方 API Key**（`https://api.deepseek.com`）；
- 通过 **SiliconFlow 的 DeepSeek 系列模型**（如 `deepseek-ai/DeepSeek-V3`、`DeepSeek-V3.2` 等）。

从公开信息可知：

- 在 SiliconFlow 上，DeepSeek-V3 系列的参考价格约为：
  - `DeepSeek-V3`：输入约 **$0.25 / M tokens**，输出约 **$1.0 / M tokens**；
  - 更新迭代版本（V3.1/3.2 等）在相近价位区间，具体数字以后可能调整；
- DeepSeek 官方文档中提供了自己的定价表，但当前抓取到的片段未包含具体数值，价格可能会随时间动态变化，需要以官网为准。

在无法精确对比每个时间点具体单价的前提下，我们从“综合性价比”的角度做如下决策：

- **工程与运维简化**：
  - 统一在 SiliconFlow 上管理 DeepSeek + Qwen 等多种模型，可以显著简化配置、限流与监控；
  - FastGPT 与 huice（rag-core / Agent）都走同一个 OpenAI 兼容入口（SiliconFlow），避免“双通道”带来的配置分裂。
- **成本与弹性**：
  - SiliconFlow 在其官网中强调相对其他大模型有较高的性价比（以 token 单价 + 吞吐量综合衡量）；
  - 即便 DeepSeek 官方在某些场景下略便宜，考虑到工程复杂度与未来可能集成多家模型供应商，**统一走 SiliconFlow 仍然是当前阶段性价比更高的选择**。

因此：

- **当前默认策略**：
  - 所有生产环境调用统一通过 SiliconFlow 完成；
  - DeepSeek 官方 API Key 作为 **备用通道**（例如：
    - 当 SiliconFlow 出现区域性故障；
    - 或未来你经过详细测算发现官方通道在某个特定业务场景下明显更便宜时），
    再通过 OneAPI 或直接在配置中切换到官方。
- **未来切换成本非常低**：
  - 只需在 `.env` 中调整 `LLM_BINDING_HOST` 与 `API_KEY`，即可从 SiliconFlow 切回 DeepSeek 官方或反向切换。

---

## 3. 统一架构总览

### 3.1 逻辑架构（功能视角）

```mermaid
graph TD
    U[👤 用户 / 客户] --> NPM[Nginx Proxy Manager]

    NPM --> FG[FastGPT 应用层\n demo.yansemei.com]
    NPM --> N8N[n8n 工作流\n flow.yansemei.com]

    FG --> SF[SiliconFlow 云模型\n DeepSeek-V3 + Qwen Embedding]
    FG --> N8N

    %% 高级能力：调用 huice Agent
    FG -. HTTP/工具 .-> AG[huice Agent API\n (LangGraph)]
    N8N -. HTTP / Webhook .-> AG

    AG --> RAG[LightRAG Core\n 图谱 + 向量检索]
    RAG --> RAGDB[(RAG 图谱/向量存储)]
```

- **日常对话 / 普通客户项目**：
  - 用户 → FastGPT → SiliconFlow → 返回回答；
  - FastGPT 可选地把问答推送到 n8n 做日志/通知。

- **需要“更强智能/分析/图谱”的场景**：
  - FastGPT Flow 或 n8n Workflow 通过 HTTP 调用 huice Agent API；
  - Agent 使用 MCP 工具访问 LightRAG，对知识图谱做更复杂的检索、分析、报告生成。

### 3.2 部署视角（VPS 上）

```mermaid
graph TD
    subgraph VPS[yansemei.com VPS]
        subgraph docker_stack[Docker Stack]
            NPM[Nginx Proxy Manager]
            FASTGPT[FastGPT + DBs]
            N8N[n8n]
            ONEAPI[OneAPI(可选)]
        end

        subgraph huice_core[Huice RAG & Agent (Python + Node)]
            RAGCORE[rag-core: LightRAG API]
            MCPSRV[MCP RAG Server]
            AGSRV[Agent Service (LangGraph API)]
            CHATUI[Chat UI]
            ADMINUI[Admin UI]
        end
    end

    FASTGPT -->|LLM/向量| SF[SiliconFlow]
    RAGCORE -->|LLM/向量| SF
```

建议：

- **FastGPT + n8n 继续用 Docker 管理**（已经稳定运行）。
- **huice RAG & Agent 可以首期以“独立 Python 进程 + Node 前端”的形式部署在 VPS 上**：
  - 持续运行：`rag-core` API + `MCP Server` + `Agent Service`；
  - 默认也持续运行：`chat-ui` / `admin-ui` 前端，用于向客户展示图谱 RAG 与 Agent 的高级能力；
  - 如遇明显资源压力，可临时将 `chat-ui` / `admin-ui` 调整为按需启动，但架构上仍按“常驻、可对外演示”来设计。

### 3.3 典型业务流程与系统分工（以 AI 客服 / 项目制服务为例）

从真实需求来看（企业客服场景、Fiverr/Upwork 项目制服务场景），我们希望“**前台看起来只有一个系统，后台多引擎协同**”。

- **终端用户 / 客服团队 / 客户员工**（前台视角）：
  - 默认入口：`demo.yansemei.com` 上的 FastGPT 应用（或嵌入客户官网的聊天窗口）；
  - 典型操作：提问、查看方案草稿、触发简单业务办理（如下单、留资、报表请求）。

- **你本人 / 内部 AI 团队**（专家视角）：
  - 高级入口：
    - `agent.yansemei.com`：huice `chat-ui`（高级对话与 Agent 调试）；
    - `graph.yansemei.com`：huice `admin-ui`（图谱与知识库管理、参数调优）。
  - 典型操作：设计与调试 Agent、构建与优化知识库/图谱、配置与排查自动化流程。

- **后台协同模式（避免割裂）**：
  - 日常简单问答：
    - 用户 → FastGPT → SiliconFlow → 返回回答；
  - 遇到“复杂分析 / 报表 / 图谱推理”等高阶需求时：
    - FastGPT Flow 或 n8n Workflow 通过 HTTP 调用 huice `Agent Service`；
    - huice 使用 MCP 工具 + LightRAG 图谱完成真正的“深度智能”工作；
    - 结果再通过 FastGPT 或 n8n 返回给用户/业务系统。

这样设计后：

- **对外（客户/运营）**：主要只看见 FastGPT 界面 + 可能的嵌入式机器人；
- **对内（你）**：
  - 所有高阶能力只在 huice 实现一次，FastGPT 与 n8n 都通过 API/HTTP 来“调用 huice”；
  - 避免了“在 FastGPT 里把复杂能力重复造一遍”的重复劳动。

---

## 4. 本地与生产环境的代码同步策略

### 4.1 本地仓库布局（当前）

- 本地 `fiverr/` 目录：
  - `huice/`：完整的 LightRAG + MCP + Agent + UI 项目（**内核平台**）。
  - `Server_Credentials_Final.md`：服务器端口、路径与安全策略。
  - `n8n_AI_Workflow_Guide.md` 等：工作流设计文档。

### 4.2 建议的统一仓库布局（目标）

后续建议：

- 在 `fiverr/` 仓库中新增：
  - `fastgpt-stack/`：
    - 存放 VPS 上 `/home/ai-stack/huice` 里 FastGPT 的 `docker-compose.yml`、`config.json`、`.env.example` 模板；
    - 以及 NPM 反向代理配置说明。
  - `deployment/`：
    - `deployment/yansemei/`：记录在当前 VPS 上部署的所有服务与步骤；
    - `deployment/client-template/`：面向客户的标准部署流程说明。

- 将本地 `fiverr/` 作为 **唯一代码来源（Single Source of Truth）**：
  - VPS 上新建 `/home/ai-stack/fiverr`，使用 `git clone` 拉取；
  - huice RAG & Agent 在 VPS 上直接从 `fiverr/huice` 启动；
  - FastGPT stack 则从 `fiverr/fastgpt-stack` 中读取配置文件（或拷贝到 `/home/ai-stack/huice` 目录）。

---

## 5. VPS 清理与组件取舍策略

### 5.1 建议保留的核心组件

- **必须保留**：
  - Nginx Proxy Manager（80/81/443）；
  - FastGPT stack（Web + Postgres + Mongo + Redis）；
  - n8n；
  - 生产用数据卷（数据库数据、FastGPT 配置）。

- **可选 / 视需求保留**：
  - OneAPI：
    - 如果 FastGPT 已直接调用 SiliconFlow，则 OneAPI 可以：
      - 暂时保留但关闭容器（`docker compose stop one-api`）；
      - 或未来重新设计成“统一模型路由层”再启用。

### 5.2 清理建议（思路级别）

> 具体执行前，务必用 `docker ps` / `docker compose ps` 确认容器用途，再 stop / rm。

- 使用 `docker ps` 找出：
  - 老旧的测试容器（比如旧版 Nginx、旧版数据库、无名容器）。
- 对 **不再需要的容器**：
  - 先 `docker stop <container>`；
  - 再 `docker rm <container>`；
- 对 **Compose 中暂时不用的服务**（如 OneAPI）：
  - 在对应 `docker-compose.yml` 中注释该服务；
  - 执行 `docker compose up -d`，确认其他服务正常。

> 当前阶段，我们更关注“稳定运行 + 清晰边界”，不用一开始就激进删除所有旧东西，可以循序渐进。

---

## 6. 强化 huice 项目：让能力最大化又安全

### 6.1 对接 SiliconFlow

目标：**huice 的 rag-core 和 Agent 与 FastGPT 一致，统一使用 SiliconFlow 模型**。

- 在 `rag-core/.env`（由 `env.example` 拷贝）中：
  - 设置：
    - `LLM_BINDING=openai`
    - `LLM_BINDING_HOST=https://api.siliconflow.com/v1`
    - `LLM_BINDING_API_KEY=<SiliconFlow_API_Key>`
  - Embedding 同理：
    - `EMBEDDING_BINDING=openai`
    - 对应 `EMBEDDING_BINDING_HOST`、`EMBEDDING_BINDING_API_KEY` 指向 SiliconFlow。

- 在 `agent-service` / `mcp-server` 的 `.env` 中，同样统一指向 SiliconFlow。

### 6.2 控制并发与资源占用

在 VPS 环境下，为了兼顾性能与稳定性，建议：

- `rag-core/.env`：
  - `MAX_ASYNC=4`
  - `MAX_PARALLEL_INSERT=2`
  - （如有大批量索引需求，可酌情增大，但要观察内存与外网带宽。）

- 不在 VPS 上运行本地大模型（Ollama 等），所有 LLM 调用交给 SiliconFlow；
- 将重资源操作（大批量索引、长时间分析）安排在低峰期执行。

### 6.3 与 FastGPT / n8n 的联动

- **从 FastGPT 调用 huice Agent**：
  - 在 FastGPT Flow 里新增 HTTP 模块，指向 Agent Service 的 `/invoke`（或未来约定的 API）；
  - 用于高级任务：复杂报表、图谱分析、跨知识库总结等。

- **从 n8n 调用 huice（批处理/定时任务）**：
  - 使用 HTTP Request 节点，向 rag-core 或 Agent Service 发送任务：
    - 如“每晚 3 点重新构建知识图谱”、“每周生成客户问题分析报告”。

### 6.4 UI 策略：功能去重与角色划分

为避免给客户带来混乱，同时又展示“最大性能、最高智能性”，三套 UI 的定位如下：

- **FastGPT（demo.yansemei.com）**：
  - 面向“日常业务用户 / 客服团队”的主入口；
  - 负责：常规问答、知识库检索、简单流程编排（Flow）、Webhook 到 n8n；
  - 不再重复构建复杂图谱可视化或 Agent 调试界面。

- **chat-ui（建议未来通过 `agent.yansemei.com` 暴露）**：
  - 面向“对智能程度有高要求的客户 / 内部 AI 团队”；
  - 展示 LangGraph Agent 的多步推理、工具调用轨迹、RAG 过程；
  - 作为 huice 平台的“高级智能 Demo”与内测入口，不与 FastGPT 的基础聊天功能重复，而是更强调：
    - 工具链调用；
    - 复杂任务（报表、分析、多轮规划）。

- **admin-ui（建议未来通过 `graph.yansemei.com` 或内部路径暴露）**：
  - 面向“运营 / 数据 / AI 工程师”等专业用户；
  - 负责知识图谱与向量库的可视化、调试与评估；
  - 不与 FastGPT 的知识库上传/管理 UI 竞争，而是专注在：
    - 图谱结构、关系洞察；
    - 高级参数调优与质量诊断。

整体规则：

- **对标准客户**：
  - 默认提供 FastGPT + n8n 作为主要操作界面；
  - 视客户成熟度，逐步开放 chat-ui / admin-ui 作为“专家模式”界面，并配培训。
- **对高要求 / 展示场景**：
  - 三个界面都保持在线，通过不同域名区分角色；
  - 文档中明确每个入口的用途，避免功能重叠和定位模糊。

### 6.5 FastGPT 与 huice 的长期演进路线

结合当前代码与产品形态，我们的长期目标是：**逐渐将平台能力收拢到 huice 上，但在过渡阶段保留 FastGPT 带来的“低代码壳”优势**。

- **当前阶段（过渡期）**：
  - FastGPT：
    - 作为客户/运营侧的主要操作界面（知识库上传、简单流程编排、聊天入口）；
    - 遇到复杂任务时，通过 Flow/HTTP 调用 huice Agent API，让 huice 执行复杂 RAG + Agent 推理；
  - huice：
    - 作为唯一的“高级智能内核”，集中实现：图谱 RAG、多工具 Agent、复杂报表与项目分析；
    - `chat-ui` / `admin-ui` 主要面向你本人与内部专家团队，用于调试与高级分析。

- **中期目标**：
  - 在 huice 的 `admin-ui` 中逐步补齐：
    - 知识库/KG 管理（上传/更新/清洗）界面；
    - 应用 / Agent 配置界面（类似 FastGPT 的 App Builder，但更贴合你自己的业务）；
    - 轻量级流程/集成配置（如配置某个 Agent 在满足条件时调用指定 n8n 工作流）。
  - 当这些能力成熟后：
    - 新项目可以直接在 huice 平台上全流程落地；
    - FastGPT 更多作为“历史项目的承载壳”或个别客户的专用入口。

- **长期目标（可选，但方向明确）**：
  - 理论上，未来可以完全依靠：
    - huice（RAG + Agent + 平台 UI）；
    - n8n（自动化与外部系统集成）；
  - FastGPT 退居为“可选组件”，逐步让“完整新系统”收敛为：
    - **huice = 大脑（Brain + Memory + 图谱）**；
    - **n8n = 手脚（Actions + 集成）**；
    - 多个前端（官网 Chat、小程序、内部 Web 控制台）统一调用这两个核心。

在这一演进路径上，**所有新增的高阶能力一律优先实现到 huice 内核与 UI 上，再按需暴露给 FastGPT/n8n**，避免未来再次出现平台能力分散的问题。

### 6.6 多租户与企业分组数据模型（规划阶段）

为了支持你后续对外提供“多企业、多账号”的服务，需要在架构上提前明确：

- **租户 / 企业 (Tenant / Company)**：
  - 代表一个公司或组织（例如公司 E）；
  - 其下可以有多个用户（A、B 等）、多个项目空间、多个知识库。

- **用户 (User)**：
  - 从属某个租户；
  - 拥有自己的 `user_id`，并可被赋予不同角色（企业管理员、运营、客服、访客等）。

- **可见性与数据分层**：
  - 所有重要数据实体（文档、向量/图谱节点、会话、工作流配置等）都应具备以下字段：
    - `tenant_id`：所属企业，用于确保 **跨企业之间绝对隔离**；
    - `owner_user_id`：创建者；
    - `visibility`：
      - `private`：仅创建者本人可见；
      - `org`：本企业内所有有权限的用户可见（例如 A 上传的 PDF，B 也可以正常使用和查看）；
      - `public`：全局共享（通常仅由超级管理员或平台方维护的通用知识，如“如何使用 DeepSeek 模型”）。

- **角色与权限（示意）**：
  - `global_admin`（平台级管理员）：可以查看和运维所有租户的数据，用于内部运维与诊断；
  - `tenant_admin`（企业管理员）：
    - 仅能管理本企业 (`tenant_id`) 下的用户、知识库与工作流；
    - 可以配置“默认可见性”（例如：本企业默认文档为 `org`，但允许个人建 `private` 笔记）。
  - `member`（普通成员，如 A、B）：
    - 默认可以访问本企业的 `org` 级文档与知识库；
    - 其个人创建的 `private` 内容只能自己看到。

在实现节奏上：

- 当前阶段：
  - 整个系统可以视为“单租户 = 你自己的工作室”，在配置中写死一个 `DEFAULT_TENANT_ID` 即可；
  - 代码与数据模型设计时，提前预留 `tenant_id` / `visibility` 等字段，避免未来大改表结构和接口。 
- 后续阶段（多租户化改造）：
  - 在 huice 的 rag-core / MCP Server / Agent Service / 前端 UI 中逐步引入上述字段与过滤逻辑；
  - 与 FastGPT 的空间/应用概念、n8n 的 workflow 命名规范结合，实现真正意义上的“多企业 + 企业内多账号 + 管理员全局视图”。

---

## 7. VPS 性能与容量评估（高层结论）

> 由于当前尚未在代码中记录 VPS 的 CPU / 内存配置，这里给出通用评估思路：

- **有利条件**：
  - 所有大模型推理都在 SiliconFlow 云端执行，VPS 主要承担：
    - Web 前端 + 反向代理；
    - 数据库与缓存；
    - RAG 编排与 Agent 逻辑；
    - 工作流（n8n）。
  - 只要不在本机跑大模型，CPU/内存压力主要来自并发请求数量与 LightRAG 的索引任务。

- **对典型 2C4G / 2C8G VPS 的建议**：
  - **设计目标**：
    - 在不运行本地大模型的前提下，让所有核心服务在 VPS 上“常开”：
      - Nginx Proxy Manager
      - FastGPT stack
      - n8n
      - huice 的：`rag-core` + `MCP Server` + `Agent Service` + `chat-ui` + `admin-ui`
  - **资源不足时的降级路径（从轻到重）**：
    1. 先调低 LightRAG 的并发参数（`MAX_ASYNC`、`MAX_PARALLEL_INSERT`）；
    2. 再考虑将 `chat-ui`、`admin-ui` 改为“按需启动”（展示或调试时再开）；
    3. 如仍不够，再评估升级 VPS 配置，或将重型批处理/离线任务迁移到专用 Worker 机器。
  - 在以上策略下，可以在“功能最完整、智能性最高”和“资源安全边界”之间取得平衡。

- **当并发量或任务复杂度提升时**：
  - 优先升级 VPS 内存与网络带宽；
  - 将大规模批处理任务（如全量重建图谱）迁移到专用 Worker 机器或离线环境；
  - 通过 OneAPI（未来）做多云模型路由与限流。

---

## 8. 后续实施路线图（概要）

1. **代码层统一**：
   - 以本地 `fiverr/` 作为统一仓库；
   - 在其中加入 `fastgpt-stack/`、`deployment/` 等目录，纳入版本管理。

2. **VPS 环境整理**：
   - 梳理 docker 容器，保留 FastGPT、DB、NPM、n8n；
   - 评估 OneAPI 的实际用途，必要时先停用以节省资源。

3. **huice RAG & Agent 部署到 VPS**：
   - 在 VPS 上 `git clone` 当前仓库；
   - 配置 rag-core/.env 指向 SiliconFlow；
   - 启动：LightRAG API + MCP Server + Agent Service；
   - 视资源情况选择性启动 Chat UI / Admin UI。

4. **打通 FastGPT / n8n 与 huice**：
   - 在 FastGPT Flow 中增加调用 huice Agent API 的 HTTP 节点；
   - 在 n8n Workflow 中增加调用 huice 的 HTTP 节点，用于批处理任务。

5. **标准化交付物**：
   - FastGPT 应用 Flow JSON 模板；
   - n8n Workflow JSON 模板；
   - FastGPT docker-stack 模板（docker-compose.yml + config.json + .env.example）；
   - huice RAG & Agent 环境配置模板（.env.example）；
   - 一份类似本文件的系统架构说明文档（客户版）。

6. **多租户与企业分组设计与落地（后续阶段）**：
   - 在 huice / FastGPT / n8n 的数据与接口层面，统一引入：`tenant_id`、`user_id`、`visibility`、`role` 等概念；
   - 优先在 huice 的 rag-core / MCP / Agent / UI 中实现“单实例多企业”的能力（公司内共享、跨公司隔离、管理员全局视图）；
   - 待当前单租户完整部署与对外演示稳定后，再启动这一阶段的设计与编码工作，并在此文档中持续更新方案。

> 本文件为当前内部“完整新系统”的权威说明，后续如有架构变更（包括多租户与企业分组能力的落地），应在此文件中同步更新。
