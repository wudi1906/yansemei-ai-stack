# 开发仓库与 GitHub 策略（fiverr + huice）

## 1. 设计目标

- **只维护一套仓库结构**，便于长期进化和备份。
- 兼顾：
  - 本地开发（Mac 本机）；
  - VPS 部署（yansemei.com）；
  - GitHub 版本管理与展示（作品集 / Demo）。
- 不强求继续维持历史上的“单独 huice 仓库”，以 **当前 fiverr 项目为中心** 重新整理更简单的结构。

---

## 2. 推荐仓库结构

### 2.1 顶层：fiverr 仓库

**建议：以当前 `fiverr/` 目录作为唯一 Git 仓库的根目录。**

典型目录结构：

- `huice/`
  - LightRAG + MCP + Agent + chat-ui + admin-ui 全栈代码（完整新系统的内核）；
- `fastgpt-stack/`（建议后续补充）
  - FastGPT 的 `docker-compose.yml`、`config.json`、`.env.example` 等配置模板；
- `deployment/`
  - `deployment/yansemei/`：生产环境（yansemei.com VPS）的部署步骤与注意事项；
  - `deployment/client-template/`：面向客户的标准化部署文档；
- 各种说明文档：
  - `Server_Credentials_Final.md`
  - `System_Architecture_Huice_Yansemei.md`
  - `n8n_AI_Workflow_Guide.md`
  - 产品说明书（如 `Product_Spec_01_AI_Customer_Support.md` 等）。

这样做的好处：

- **所有代码 + 配置 + 文档都在一个仓库里**，方便维护与备份；
- VPS 上只需要 `git pull` 一个仓库即可同步所有更新；
- 将来对外开源或者作为作品集展示时，也只需要给出一个 GitHub 仓库地址。

### 2.2 关于历史 huice 仓库

- 你之前已经为 `huice/` 单独建过 Git 仓库并上传到 GitHub：
  - 这个历史仓库可以：
    - 作为“早期版本”的存档继续保留；
    - 或者在其 README 中注明“新版本已迁移到 fiverr 总仓库”，引导读者跳转。
- **后续开发建议集中到 fiverr 仓库中进行**：
  - 即：`huice/` 不再单独作为一个独立 Git 仓库，而是 fiverr 仓库的子目录。

如有需要，我们也可以在未来使用 `git subtree` 等方式把历史提交合并进 fiverr 仓库，但短期内不是必须。

---

## 3. 在本地配置 Git 与 GitHub（以 fiverr 为根）

以下步骤假设你在本地 Mac 上已经进入 `fiverr/` 目录。

### 3.1 初始化或复用 Git 仓库

1. 如果 `fiverr/` 还不是一个 Git 仓库：

   ```bash
   git init
   ```

2. 添加 `.gitignore`（如尚未存在）：
   - 忽略内容建议包括：
     - Python: `__pycache__/`, `.venv/`, `*.pyc`
     - Node: `node_modules/`, `.next/`, `dist/`, `build/`
     - 其他临时文件：`.DS_Store`, `*.log`, `.env`, `.env.*`

3. 将当前代码加入暂存并提交首个版本：

   ```bash
   git add .
   git commit -m "Initial unified repo for fiverr + huice platform"
   ```

### 3.2 连接到 GitHub

1. 在 GitHub 上新建一个仓库：
   - 仓库名可以是：
     - `huice-fullstack-platform`
     - 或 `yansemei-ai-stack` 等，只要你自己记得就好。

2. 将 GitHub 仓库设为远程：

   ```bash
   git remote add origin git@github.com:<your-username>/<your-repo-name>.git
   ```

3. 推送本地代码到 GitHub：

   ```bash
   git push -u origin main
   ```

> 如果当前默认分支不是 `main`，而是 `master`，可根据实际情况调整命令里的分支名。

### 3.3 后续开发与部署流程

- 本地修改代码或文档后：

  ```bash
  git add .
  git commit -m "feat: <简要说明本次改动>"
  git push
  ```

- 在 VPS 上更新代码：

  ```bash
  cd /home/ai-stack/fiverr
  git pull
  ```

- 对于 Docker 服务（FastGPT、n8n 等）：
  - 如配置有变更，再执行对应目录下的 `docker compose up -d` 以套用最新配置。

---

## 4. 常驻服务与 Git 的关系

- 所有服务（FastGPT、n8n、huice 全栈）在 VPS 上都可以保持“常开”，只要：
  - 不在本机运行大模型推理（全部交给 SiliconFlow）；
  - 合理设置 LightRAG 并发与批处理任务的时间窗口。
- 通过 Git 统一管理代码与配置，可以：
  - 快速回滚到某次稳定版本；
  - 在本地做实验，验证后再推送到 VPS。

---

## 5. 总结：推荐实践

- **唯一主仓库**：以 `fiverr/` 为 Git 根目录，统一管理 huice + FastGPT + n8n + 文档。
- **GitHub 只建一个主仓库**：作为对外展示与备份；老的 huice 仓库可以作为历史存档保留。
- **VPS 只从这个仓库部署**：
  - `/home/ai-stack/fiverr` → huice 全栈 + 部署脚本；
  - `/home/ai-stack/huice`（旧 FastGPT docker 目录）可以逐步重构为从 `fiverr/fastgpt-stack` 同步配置。

这样，你可以继续在本地舒适地开发、在 VPS 上保持所有服务常开，并且通过 GitHub 安全地托管与展示整个“完整新系统”。
