# 服务器部署关键信息备忘录 (Confidential & Final)

> **🔒 最高安全级别**：本服务器已完成企业级安全加固。所有数据库端口已物理隔离，仅允许通过 SSH 或 Nginx 网关访问。请务必妥善保管此文件。

## 1. 核心安全架构 (Security Architecture)
*   **防火墙 (UFW)**: ✅ 已启用
    *   **开放端口**: 22 (SSH), 80 (HTTP), 443 (HTTPS), 81 (网关管理)
    *   **拦截端口**: 3001, 3002, 5678, 27017, 6379, 5432 (仅限内网访问)
*   **访问方式**: 
    *   所有 Web 服务必须通过域名 (`https://demo.yansemei.com`) 访问。
    *   直接使用 `http://IP:端口` 将被防火墙拦截（为了安全）。

## 2. 服务组件与凭证清单 (Service Credentials)

### 2.1 网关服务 (Nginx Proxy Manager)
*   **状态**: 部署中 (端口 80/81/443)
*   **路径**: `/home/ai-stack/npm`
*   **管理面板**: `http://148.135.57.133:81`
*   **初始账号**: `admin@example.com`
*   **初始密码**: `changeme` (⚠️ 首次登录后请立即修改)

### 2.2 AI 知识库 (FastGPT)
*   **状态**: 运行中 (端口 3001, 仅内网)
*   **路径**: `/home/ai-stack/huice`
*   **内部地址**: `http://148.135.57.133:3001` (需通过网关转发)
*   **Root 用户**: `root`
*   **Root 密码**: `MyFastGPTPass2025!` (已配置强密码)
*   **API Key**: `sk-khvlnebzljzmhttquzghrbidptpygrzzoeymgpgfkklwltlw`

### 2.3 模型渠道 (OneAPI)
*   **状态**: 运行中 (端口 3002, 仅内网)
*   **路径**: `/home/ai-stack/huice` (与 FastGPT 同组)
*   **内部地址**: `http://148.135.57.133:3002` (需通过网关转发)
*   **Root 用户**: `root`
*   **Root 密码**: `123456` (⚠️ **警告**: 请登录后立即修改!)

### 2.4 工作流自动化 (n8n)
*   **状态**: 运行中 (端口 5678, 仅内网)
*   **路径**: `/home/ai-stack/n8n`
*   **内部地址**: `http://148.135.57.133:5678` (需通过网关转发)
*   **验证方式**: 首次访问需创建账号

---

## 3. 数据库凭证 (Database Internals)
> **注意**: 这些数据库端口不对外开放，仅供 Docker 内部连接。

### PostgreSQL (向量库)
*   **端口**: 5432
*   **用户**: `username`
*   **密码**: `MySuperSecurePgPass2025!`
*   **库名**: `postgres`

### Redis (缓存)
*   **端口**: 6379
*   **密码**: `MySuperSecureRedisPass2025!`

### MongoDB (文档库)
*   **端口**: 27017
*   **模式**: 副本集 (`rs0`)
*   **安全策略**: 内部网络隔离，无密码验证 (No-Auth in Private Network)

---

## 4. 故障排查与维护 (Maintenance)

### 如果 Nginx 网关启动失败 (端口 80 被占用)
请执行以下命令查找并停止占用 80 端口的旧容器：
```bash
# 查看谁占用了 80
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" | grep 80

# 停止相关容器 (假设 ID 为 abc12345)
docker stop abc12345
docker rm abc12345

# 重新启动 NPM
cd /home/ai-stack/npm && docker compose up -d
```

### 如何重启某个服务
```bash
# 重启 FastGPT/OneAPI
cd /home/ai-stack/huice && docker compose restart

# 重启网关
cd /home/ai-stack/npm && docker compose restart
```

---

## 5. 下一步行动指南 (Next Steps)
1.  **解决 80 端口占用**：参照第 4 节，确保 NPM 启动成功。
2.  **配置域名转发 (在 http://148.135.57.133:81)**：
    *   `demo.yansemei.com` -> `148.135.57.133` : `3001` (FastGPT)
    *   `flow.yansemei.com` -> `148.135.57.133` : `5678` (n8n)
    *   `api.yansemei.com` -> `148.135.57.133` : `3002` (OneAPI)
3.  **申请 SSL 证书**：在 NPM 中勾选 "Force SSL" 和 "Lets Encrypt"。

## 6. 系统架构与代码同步概览 (Summary)
- 当前生产环境的三大入口：
  - `demo.yansemei.com`：面向用户的 FastGPT 应用层。
  - `flow.yansemei.com`：n8n 工作流与自动化引擎。
  - `api.yansemei.com`：OneAPI（可选的模型路由层）。
- 本地 `huice/` 项目作为 **LightRAG + LangGraph Agent 内核**，后续将通过 Git 仓库与 VPS 上代码保持同步，用作：
  - 知识库构建与质量评估的“后端大脑”；
  - 高级分析 / 报表类 Agent 服务；
  - FastGPT 与 n8n 的高级工具提供者。
- 详细的整体架构和部署方案，见同目录下 `System_Architecture_Huice_Yansemei.md`。

## 7. Huice AI 平台整体目标与 Docker 化路线图

### 7.1 最终目标（抬头看路版）

- 打造一个 **完全 Docker 化、可一键启动/停止** 的 Huice AI 平台，包括：
  - 知识库内核：LightRAG / rag-core
  - 多代理后端：agent-service（聚合 rag-core、MCP、外部 LLM）
  - 对话前端：AuroraAI（chat-ui），通过域名 `aurora.yansemei.com` 访问
  - 知识管理前端：admin-ui（AnythingChatRAG WebUI），通过域名 `chat.yansemei.com/webui/` 访问
  - 辅助服务：FastGPT、OneAPI、n8n 等
- 所有 Web 访问统一走：**域名 + Nginx Proxy Manager + HTTPS**，不直接暴露内网端口。
- 提供一套 **可交付给乙方/运维** 的完整文档：
  - 架构图 + 文字说明
  - 启动/停止/重启/排错手册
  - 账号与密钥管理规范

### 7.4 近期执行计划与步骤（2025-12-25）

1) 基础部署补全  
   - Docker 化 MCP，加入 `/home/ai-stack/fiverr/huice/docker-compose.yml`，使 agent-service 工具链可用。  
   - 清理 compose `version` 警告（删除 version 行），统一所有路径使用 `/home/ai-stack/fiverr/huice/...`。  
   - 按本文档域名映射确保 NPM 转发与证书（demo/flow/api/aurora/chat）。

2) 接口与服务验证  
   - 后端健康检查：`/ok`、`/info`、`/threads/search`（应返回 []）、`/threads/{id}/history`（[]）、`/threads/{id}/runs/stream`（返回助手消息）；rag-core 对应健康接口也测一遍。  
   - 前端自测：Aurora（aurora.yansemei.com）、admin-ui（chat.yansemei.com/webui/）、FastGPT/OneAPI/n8n 进行 smoke test。

3) 安全加固（功能稳定后立即跟进）  
   - 收紧 CORS 到指定域名；为 agent-service/rag-core 增加 API Key/JWT 或在 NPM 层做访问控制。  
   - NPM 启用 Force SSL + 证书，关闭不必要的明文入口。  
   - .env 密钥管理与日志脱敏；必要时限流/防刷。

4) 运维与统一  
   - 将 rag-core、agent-service、MCP、前端、辅助服务统一在一个（或分层） compose；  
   - 编写启动/停止/排错手册，列出域名→服务→端口映射及健康检查命令。

### 7.2 当前 VPS 服务状态概览

- **已 Docker 化的核心组件**：
  - Nginx Proxy Manager：80/81/443，对外所有域名的统一入口，网络 `npm_default`。
  - FastGPT 栈（/home/ai-stack/huice/docker-compose.yml）：
    - PostgreSQL (pg)、MongoDB、Redis
    - OneAPI（3002 → api.yansemei.com）
    - FastGPT（3001 → demo.yansemei.com）
  - 前端：
    - `huice-chat-ui` 容器：Aurora 对话前端，端口 3000，经 NPM 暴露为 `aurora.yansemei.com`
    - `huice-admin-ui` 容器：知识管理前端，端口 5173，经 NPM 暴露为 `chat.yansemei.com/webui/`

- **尚未 Docker 化、仍在宿主机上的组件**：
  - rag-core（LightRAG API），端口 9621，.env 已配置账号与 LLM 相关参数。
  - agent-service（FastAPI `/chat`），端口 2025，用于对话编排。
  - MCP server（端口 8001），由 agent-service 调用。

### 7.3 需求拆解与任务清单（高层）

1. **架构与安全**
   - 所有核心服务 Docker 化，并纳入统一的 docker-compose 管理。
   - VPS 防火墙仅开放 22/80/81/443，所有 Web 入口必须经 NPM + HTTPS 域名访问。

2. **功能闭环**
   - admin-ui：
     - 使用自定义账号 `wudi1906@gmail.com / wudi058493` 登录。
     - 能查看 rag-core 健康状态、文档列表、扫描/处理进度，支持上传文档、构建知识图谱。
   - AuroraAI：
     - 前端通过 `agent-service` 调用 rag-core + MCP + 外部 LLM，完成端到端对话。

3. **运维与交付**
   - 在 `/home/ai-stack/huice` 或约定目录下，形成一份主 `docker-compose.yml`：
     - 包含 DB/缓存/OneAPI/FastGPT
     - 包含 rag-core、agent-service、MCP
     - （可选）包含 chat-ui / admin-ui 前端
   - 输出一份运维手册，包含：
     - 一键启动/停止命令
     - 常见故障排查（端口占用、容器挂掉、证书异常等）

### 7.4 分阶段路线图（当前进度标记）

1. **阶段 1：前端 Docker 化与域名打通** ✅
   - chat-ui / admin-ui 已以 Docker 形式运行，并通过 NPM 域名访问：
     - `https://aurora.yansemei.com`
     - `https://chat.yansemei.com/webui/`

2. **阶段 2：admin-ui ↔ rag-core 打通（进行中） 🟡**
   - rag-core `.env` 已配置登录账号与 JWT 秘钥。
   - 下一步：
     - 统一 rag-core 的启动方式（先在宿主机稳定运行）。
     - 为 rag-core 增加 NPM 代理（如 `kb.yansemei.com`），或在 admin-ui 中配置正确的 `backendBaseUrl`。

3. **阶段 3：rag-core / agent-service / MCP 全部 Docker 化（未开始） 🔴**
   - 新增 Dockerfile 与 docker-compose 服务定义：
     - `rag-core`：基于 Python 3 镜像，加载现有 `.env`，挂载 `inputs/` 与 `rag_storage/`。
     - `agent-service`：基于 FastAPI/Uvicorn 镜像或自定义 Dockerfile，暴露 2025 端口。
     - `mcp-server`：视需求决定是否单独暴露对外，仅需与 agent-service 可达即可。
   - 所有新服务加入 `npm_default` 网络，供 NPM 通过容器名转发。

4. **阶段 4：AuroraAI ↔ agent-service ↔ rag-core 端到端对话（未开始） 🔴**
   - 在 NPM 中为 agent-service 配置 `agent.yansemei.com`。
   - 在 Aurora 前端中设置：
     - 部署 URL：`https://agent.yansemei.com`
     - 助手/Graph ID：使用 `graph.json` 中定义的 ID（如 `chat_agent`）。
   - 验证完整对话链路：浏览器 → Aurora → agent-service → rag-core/MCP → LLM。

5. **阶段 5：统一 compose + 运维文档（未开始） 🔴**
   - 将所有 Huice 服务统一进 1–2 个 docker-compose 文件（生产与工具栈）。
   - 更新本备忘录与 `System_Architecture_Huice_Yansemei.md`，形成对外可交付的完整方案。

### 7.5 当前 VPS 运行状态（2025-12-25 11:13）

- 正在运行的容器（docker ps 摘要）：
  - `huice-agent-service` (2025) ✅
  - `huice-mcp` (8001) ⚠️ 现为 stub，必须替换为正式 mcp-server，避免工具链空列表
  - `huice-rag-core` (9621) ✅
  - `huice-chat-ui` (3000)、`huice-admin-ui` (5173) ✅
  - `fastgpt` (3001)、`oneapi` (3002)、`pg`、`mongo`、`redis` ✅
  - `n8n` (5678)、`npm-app-1` (80/81/443) ✅

- 重要告警与禁止事项：
  - **禁止再使用 MCP stub 充当正式服务。** 必须将 `/home/ai-stack/fiverr/huice/mcp` 替换为真实 `mcp-server` 代码并重建镜像，确保 `/tools` 返回完整工具列表，agent-service 启动时不再产生空工具或 fetch 失败。
  - 排查 huice 目录中的 legacy/demo 项目，不必全部上线，只保留生产必需组件（rag-core、agent-service、mcp-server、chat-ui、admin-ui、FastGPT/OneAPI/n8n/NPM），其余归档。

- 立即行动（MCP 替换与验证）：
  1) 确认 mcp-server 技术栈与入口：
     ```bash
     ls -la /home/ai-stack/fiverr/huice
     ls -la /home/ai-stack/fiverr/huice/mcp-server
     find /home/ai-stack/fiverr/huice/mcp-server -maxdepth 2 -type f \( -name "package.json" -o -name "requirements.txt" -o -name "pyproject.toml" \)
     ```
  2) 依据结果重写 `/home/ai-stack/fiverr/huice/mcp/Dockerfile`（Node: npm install/start；或 Python: pip install/启动入口），并将真实代码复制到 `/home/ai-stack/fiverr/huice/mcp`。
  3) 重建并启动：
     ```bash
     cd /home/ai-stack/fiverr/huice
     docker compose build --no-cache mcp
     docker compose up -d mcp
     docker compose build --no-cache agent-service
     docker compose up -d agent-service
     ```
  4) 验证：
     ```bash
     curl -s http://localhost:8001/tools
     docker logs agent-service --tail 200 | grep -i mcp
     ```
     目标：/tools 返回非空工具列表，agent-service 启动无 MCP fetch 警告。
