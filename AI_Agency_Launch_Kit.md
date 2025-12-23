# AI Agency 独立开发者实战交付手册：从部署到变现
> **核心战略**：左手 "Huice" (大脑/RAG)，右手 "n8n" (双手/Workflow)。
> **目标**：打造一套可复用、可展示、可交付的标准化技术底座，从“卖时间”转向“卖产品”。

---

## 第一部分：技术主干——你的“数字军火库”搭建 (Infrastructure)

在去见客户之前，你必须先在云端建立你的根据地。这不是为了跑代码，而是为了**“秀肌肉” (Demo)**。

### 1.1 服务器选购与环境准备
不要用自己的 MacBook 做服务器。你需要一台 7x24 小时在线的云服务器。

*   **服务器推荐**：
    *   **性价比之选**：Hetzner (德国/芬兰) - CX31/CX41 系列。约 €5-€10/月。性能极其强悍。
    *   **开发者友好**：DigitalOcean / Vultr。约 $10-$20/月。界面简单，一键部署 Docker。
    *   **配置建议**：
        *   CPU: 2 vCPU
        *   RAM: 4GB+ (跑 RAG 比较吃内存，建议 8GB 更稳)
        *   OS: Ubuntu 22.04 LTS
*   **域名准备**：
    *   去 Namecheap / Godaddy 买个便宜域名（如 `your-ai-lab.com`）。
    *   你需要两个子域名：
        *   `demo.your-ai-lab.com` (给客户看 Huice RAG 系统)
        *   `flow.your-ai-lab.com` (给你自己用的 n8n)

### 1.2 核心全栈部署 (The Stack)
我们需要用 Docker Compose 一键拉起所有服务。

**架构图 (Mermaid)**：

```mermaid
graph TD
    User[外部客户/你] -->|HTTPS| Nginx[Nginx Proxy Manager (网关)]
    Nginx -->|demo.domain.com| Huice[Huice RAG 系统]
    Nginx -->|flow.domain.com| N8N[n8n 自动化平台]
    
    subgraph "Huice System (Docker)"
        Huice --> AdminUI[Admin UI (前端)]
        Huice --> Agent[Agent Service]
        Huice --> RAGCore[RAG Core (向量库+LLM)]
    end
    
    subgraph "n8n System (Docker)"
        N8N --> Webhook[Webhook Receiver]
        N8N --> Worker[Worker Nodes]
    end
```

**实操文件：`production-docker-compose.yml`**
(这是你的核心资产，保存在服务器根目录)

```yaml
version: '3.8'

services:
  # 1. 网关与SSL证书管理 (让你的服务能通过 https 访问)
  npm:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: always
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./npm/data:/data
      - ./npm/letsencrypt:/etc/letsencrypt

  # 2. 你的核心大脑: Huice RAG (这里假设你已经把 huice 打包成了 Docker 镜像)
  # 注意：实际部署时需要构建镜像，这里用示例代替
  huice-rag-core:
    build: ./rag-core
    environment:
      - WORKSPACE_DIR=/app/data
    volumes:
      - ./huice_data:/app/data

  huice-admin-ui:
    build: ./admin-ui
    ports:
      - '3000:3000'
    depends_on:
      - huice-rag-core

  # 3. 你的核心双手: n8n
  n8n:
    image: n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=flow.your-ai-lab.com
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://flow.your-ai-lab.com/
    volumes:
      - ./n8n_data:/home/node/.n8n
```

---

## 第二部分：三大黄金场景的交付流程 (SOP)

有了服务器，现在我们来谈**怎么卖**。每一个场景都分为“演示”、“配置”、“交付”三个阶段。

### 场景一：企业智能知识库 (The Brain)
**目标客户**：有大量 PDF 手册/合同/文档的公司。
**基于系统**：Huice RAG

#### 1. 演示阶段 (The Hook)
*   **动作**：
    1.  打开你的 `demo.your-ai-lab.com`。
    2.  当着客户的面，上传一份**他给你的真实文档**（比如他的员工手册）。
    3.  上传完成后，立刻在聊天框提问：“公司关于迟到的规定是什么？”
    4.  系统秒回准确答案。
*   **话术**：“看，这是你的专属 AI，它已经学会了这份文档。想象一下它学会你们公司 10 年积累的所有文档会怎样？”

#### 2. 配置阶段 (Implementation)
*   **数据清洗**：客户给的 PDF 往往很乱（扫描件、格式错误）。你需要用 n8n 里的 OCR 节点或者 Python 脚本先清洗一遍，转成干净的 Markdown 或 TXT。
*   **Prompt 调优**：在 Huice 的 Admin UI 里调整系统提示词。比如：“你是一名严谨的法律顾问，回答必须引用原文条款...”

#### 3. 交付物 (Deliverables)
你可以提供三种不同价位的交付：

*   **🥉 青铜版 (SaaS账号)**：
    *   **交付物**：一个账号密码（在你的 `demo` 服务器上开一个租户）。
    *   **形式**：通过邮件发送登录链接。
    *   **优点**：你掌握数据，客户按月付费，粘性高。
*   **🥈 白银版 (私有化部署)**：
    *   **交付物**：一份部署脚本 + 操作手册。
    *   **形式**：你远程登录客户的服务器，帮他把 Docker 跑起来。
    *   **文档**：`《Huice系统管理员维护手册.pdf》` (包含如何上传文档、如何查看日志)。
*   **🥇 黄金版 (源码买断)**：
    *   **交付物**：GitHub 仓库权限 + 架构文档。
    *   **形式**：签订《技术转让合同》，移交所有源代码。价格通常是白银版的 5-10 倍。

---

### 场景二：全自动情报/内容引擎 (The Engine)
**目标客户**：营销公司、需要写大量 SEO 文章的博主。
**基于系统**：n8n + LLM API

#### 1. 演示阶段
*   **动作**：录制一个 2 分钟的 Loom 视频。展示 n8n 界面上，数据如何从 Google Search 自动流向 ChatGPT，最后自动变成一篇 WordPress 文章发布出去。
*   **关键点**：展示**“批量”**的力量（Excel 里有 100 个关键词，一键全自动生成）。

#### 2. 配置阶段
*   **流程设计**：在 n8n 画布里设计逻辑（Loop, If, HTTP Request）。
*   **Prompt 保护**：**这是你的核心资产！** 不要直接把 Prompt 写在 n8n 的公开节点里。
    *   *技巧*：你可以把核心 Prompt 放在你自己的 Huice RAG 系统里，让 n8n 调用你的 Huice API 来获取 Prompt。这样客户拿到了 n8n 流程也拿不到你的核心 Prompt。

#### 3. 交付物 (Deliverables)

*   **📦 标准交付包**：
    1.  **Workflow JSON 文件**：客户可以直接导入他的 n8n。
    2.  **Config 表格**：一个 Excel 模板，告诉客户在哪里填 API Key，在哪里填关键词。
    3.  **视频教程**：`《如何导入并运行自动化流水线.mp4》`。
*   **☁️ 托管服务 (Service)**：
    *   客户不需要懂 n8n。
    *   你给他一个 **Webhook URL** (API接口)。
    *   告诉他：“你只要往这个地址发一个关键词，我的系统就会自动帮你写好文章并发到你的博客。”
    *   **按量计费**：每篇文章收 ¥10。

---

### 场景三：AI 销售/客服机器人 (The Agent)
**目标客户**：电商卖家、独立站。
**基于系统**：Huice Agent Service + 微信/飞书接口

#### 1. 演示阶段
*   让他加你的测试微信号/飞书号。
*   让他扮演刁钻客户来提问。
*   展示 AI 如何完美应对，甚至引导下单。

#### 2. 配置阶段
*   **知识库挂载**：把产品的 SKU 表、FAQ 喂给 Huice。
*   **渠道接入**：配置 Coze 或 微信机器人框架（如 WxWork）。

#### 3. 交付物 (Deliverables)

*   **交付物清单**：
    1.  **Bot 实例**：已经配置好的机器人，拉入客户的群。
    2.  **《话术调优指南》**：教客户如何通过修改知识库来改变 AI 的回答。
    3.  **应急开关**：一个简单的网页链接，点击就能从“AI 自动回复”切换回“人工接管”。(这是客户最想要的安全感)。

---

## 第三部分：资产管理与防守 (IP Protection)

在把东西给客户之前，如何保护自己？

1.  **核心代码服务器化**：
    *   尽量不要把复杂的 Python 脚本直接发给客户。
    *   做成 API。客户的系统调用你的 API。这样逻辑永远在你手里。
2.  **Prompt 编译化**：
    *   不要给客户明文的 Prompt。
    *   告诉客户：“这是系统内置的商业逻辑”，这是黑盒。
3.  **合同约束**：
    *   交付文档中注明：“本系统仅授权给甲方内部使用，严禁二次转售或开源。”

---

## 第四部分：你的行动清单 (Checklist)

### 🟢 本周必做 (生存基础)
1.  [ ] **购买 VPS**：推荐 Hetzner 或 DigitalOcean。
2.  [ ] **购买域名**：哪怕是 `.xyz` 这种便宜的。
3.  [ ] **跑通 Hello World**：让外网能访问你的 `demo.your-domain.com` (显示 Huice 界面) 和 `flow.your-domain.com` (显示 n8n 界面)。
4.  [ ] **投递简历**：每天投递 5 份“远程技术支持”或“软件测试”的简历，确保底仓收入。

### 🟡 下周计划 (产品包装)
1.  [ ] **录制 Demo 视频**：场景 2 (情报引擎) 最容易录，先录这个。
2.  [ ] **完善 Huice 数据**：把你自己的简历、INFP 报告喂给 Huice，测试它的问答能力。

### 🔴 商业尝试 (变现)
1.  [ ] **发布闲鱼商品**：标题参考“企业级 AI 知识库部署 | 标书分析神器”。
2.  [ ] **朋友圈/社群宣发**：发你的 Demo 视频，配文“终于把繁琐的工作自动化了”。

---

这个文档已经保存在你的根目录：`AI_Agency_Launch_Kit.md`。它不仅是技术指南，更是你的**创业说明书**。
