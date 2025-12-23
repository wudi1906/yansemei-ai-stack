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
