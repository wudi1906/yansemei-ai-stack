# 真实场景 AI 服务操作指南

> 基于 Fiverr/Upwork 2024-2025 市场需求数据
> 对应你的 VPS 双轨制架构 (FastGPT + Huice)
> 最后更新: 2025-12-26

---

## 市场需求数据摘要

根据最新市场数据：
- **Fiverr AI Agent 需求增长 18,347%** (2025年春季报告)
- **30% 的 Fiverr AI 订单是 Agent 开发**，从简单 chatbot 转向多 Agent 系统
- **Upwork AI 技能需求增长 220%**，特别是 AI 数据标注和生成式 AI
- **AI Chatbot 市场预计从 51 亿美元增长到 363 亿美元** (2023-2032)
- **n8n 自由职业市场占比超过 80%**

### 最热门的 5 类需求

| 排名 | 需求类型 | 典型预算 | 你的匹配度 |
|------|----------|----------|------------|
| 1 | AI Chatbot + 知识库问答 | $150-$2000 | ✅ 极高 (FastGPT + Huice) |
| 2 | 工作流自动化 (n8n/Zapier) | $100-$800 | ✅ 极高 (n8n) |
| 3 | RAG 系统搭建 | $300-$2000 | ✅ 极高 (LightRAG) |
| 4 | AI Agent 开发 | $500-$5000+ | ✅ 极高 (LangGraph) |
| 5 | 文档处理自动化 | $200-$1500 | ✅ 高 (RAG + n8n) |

---


## 场景 1: 为电商客户搭建 AI 客服机器人

### 客户背景
- **客户类型**: 中小型电商网站 (Shopify/WooCommerce)
- **需求**: 24/7 自动回答客户常见问题，减少人工客服压力
- **预算**: $200-$500
- **交付周期**: 3-5 天

### 典型客户需求描述
> "I need an AI chatbot for my e-commerce store that can answer questions about shipping, returns, product details, and order status. I have about 50 FAQ items and want the bot to handle 80% of customer queries automatically."

### 使用你的系统: 轨道 A (FastGPT)

**为什么选择 FastGPT:**
- 客户预算中等，需要快速交付
- 低代码可视化，客户可以自己维护
- 内置知识库功能，适合 FAQ 场景

---

### 详细操作步骤

#### 步骤 1: 登录 FastGPT

1. **打开浏览器**，访问: `https://demo.yansemei.com`
2. **输入凭证**:
   - 用户名: `root`
   - 密码: `FastGPT2025Admin!`
3. **点击** "登录" 按钮
4. **预期结果**: 看到 FastGPT 主界面，左侧有 "应用"、"知识库"、"账号" 等菜单

#### 步骤 2: 创建知识库

1. **点击** 左侧菜单 "知识库"
2. **点击** 右上角 "+ 新建" 按钮
3. **填写信息**:
   - 名称: `客户名-FAQ知识库` (例如: `ShopifyStore-FAQ`)
   - 描述: `电商客服常见问题`
4. **点击** "确认" 创建
5. **预期结果**: 看到新创建的知识库卡片

#### 步骤 3: 导入 FAQ 数据

1. **点击** 刚创建的知识库卡片，进入详情页
2. **点击** "导入数据" 或 "+" 按钮
3. **选择导入方式**:
   - **方式 A**: 手动输入 (适合少量 FAQ)
     - 点击 "手动输入"
     - 每条 FAQ 填写: 问题 + 答案
   - **方式 B**: 文件导入 (适合批量)
     - 准备 CSV 文件，格式: `问题,答案`
     - 或准备 TXT/MD 文件，每个问答用空行分隔
     - 点击 "文件导入" → 选择文件 → 上传
4. **等待索引完成** (通常 1-5 分钟，取决于数据量)
5. **预期结果**: 看到数据条目列表，状态显示 "已索引"

**示例 FAQ 数据 (CSV 格式):**
```csv
问题,答案
What is your shipping policy?,We offer free shipping on orders over $50. Standard shipping takes 3-5 business days.
How do I return an item?,You can return any item within 30 days of purchase. Please contact support@store.com to initiate a return.
Where is my order?,You can track your order using the tracking number sent to your email after shipment.
Do you ship internationally?,Yes, we ship to over 50 countries. International shipping takes 7-14 business days.
What payment methods do you accept?,We accept Visa, MasterCard, PayPal, and Apple Pay.
```

#### 步骤 4: 创建 AI 应用

1. **点击** 左侧菜单 "应用"
2. **点击** "+ 新建应用"
3. **选择** "简易模式" (适合快速搭建)
4. **填写信息**:
   - 名称: `客户名-AI客服` (例如: `ShopifyStore-Support`)
   - 头像: 选择一个客服图标
5. **配置 AI 模型**:
   - 模型: 选择 `DeepSeek-V3 (SiliconFlow)` (主力模型)
   - 温度: `0.3` (客服场景需要稳定回答)
6. **关联知识库**:
   - 点击 "添加知识库"
   - 选择刚创建的 `客户名-FAQ知识库`
   - 相似度阈值: `0.7` (推荐值)
7. **设置系统提示词**:
```
你是一个专业的电商客服助手。请根据知识库中的信息回答客户问题。

规则：
1. 只回答与店铺相关的问题
2. 如果知识库中没有相关信息，礼貌地建议客户联系人工客服
3. 保持友好、专业的语气
4. 回答要简洁明了
```
8. **点击** "保存"
9. **预期结果**: 应用创建成功，可以看到应用卡片

#### 步骤 5: 测试对话

1. **点击** 应用卡片，进入应用详情
2. **点击** 右上角 "调试" 或 "对话" 按钮
3. **发送测试消息**:
   - 输入: `What is your shipping policy?`
   - 点击发送
4. **预期结果**: AI 返回知识库中的运费政策信息
5. **继续测试**:
   - `How do I return an item?`
   - `Do you ship to Canada?`
   - `What's the weather today?` (测试边界情况)
6. **验证**: 
   - FAQ 相关问题应该准确回答
   - 无关问题应该引导联系人工客服

#### 步骤 6: 获取嵌入代码

1. **在应用详情页**，点击 "发布" 或 "分享"
2. **选择** "网页嵌入" 方式
3. **复制** 嵌入代码 (iframe 或 JS 代码)
4. **示例代码**:
```html
<iframe
  src="https://demo.yansemei.com/chat/share?shareId=xxx"
  style="width: 100%; height: 600px; border: none;"
></iframe>
```

#### 步骤 7: 交付给客户

**交付物清单:**
1. ✅ FastGPT 应用访问链接
2. ✅ 嵌入代码 (用于客户网站)
3. ✅ 知识库管理教程 (如何添加/修改 FAQ)
4. ✅ 使用说明文档

**客户自维护指南:**
```markdown
## 如何更新 FAQ

1. 登录 https://demo.yansemei.com
2. 进入 "知识库" → 选择你的知识库
3. 点击 "+" 添加新问答
4. 填写问题和答案
5. 等待索引完成 (1-2 分钟)
6. 新内容自动生效，无需重启
```

---

### 预期成果

| 指标 | 目标值 |
|------|--------|
| FAQ 覆盖率 | 80%+ 常见问题 |
| 回答准确率 | 90%+ |
| 响应时间 | < 3 秒 |
| 客户满意度 | 4.5+ 星 |

---


## 场景 2: 为企业搭建内部知识库 AI 问答系统

### 客户背景
- **客户类型**: 中型企业 (50-200 人)
- **需求**: 员工可以用 AI 查询公司内部文档、政策、流程
- **预算**: $500-$1500
- **交付周期**: 5-10 天

### 典型客户需求描述
> "We have hundreds of internal documents (HR policies, technical docs, SOPs) scattered across different systems. We need an AI assistant that employees can ask questions and get accurate answers with source references. Must be secure and not send data to external services."

### 使用你的系统: 轨道 B (Huice Core)

**为什么选择 Huice:**
- 高端客户，预算充足
- 需要知识图谱能力 (文档间关联)
- 需要更强的 RAG 检索能力
- 可以展示专业的 Admin UI

---

### 详细操作步骤

#### 步骤 1: 登录 RAG 管理界面

1. **打开浏览器**，访问: `https://chat.yansemei.com`
2. **预期结果**: 看到 LightRAG Admin UI 界面
3. **界面说明**:
   - 左侧: 文档管理、知识图谱、检索测试
   - 右侧: 主操作区域

#### 步骤 2: 上传企业文档

1. **点击** 左侧 "Documents" 或 "文档管理"
2. **点击** "Upload" 或 "上传文档" 按钮
3. **选择文件**:
   - 支持格式: PDF, TXT, MD, DOCX
   - 可以批量选择多个文件
4. **上传示例文档**:
   - `HR_Policy_2024.pdf` - 人事政策
   - `IT_Security_Guidelines.pdf` - IT 安全指南
   - `Employee_Handbook.pdf` - 员工手册
   - `Technical_SOPs.md` - 技术操作流程
5. **等待处理**:
   - 文档解析: 1-2 分钟/文档
   - 向量索引: 2-5 分钟
   - 知识图谱构建: 5-10 分钟
6. **预期结果**: 文档列表显示所有上传的文件，状态为 "Indexed"

#### 步骤 3: 查看知识图谱

1. **点击** 左侧 "Knowledge Graph" 或 "知识图谱"
2. **预期结果**: 看到可视化的知识图谱
   - 节点: 代表文档中的实体 (人名、部门、政策名称等)
   - 边: 代表实体间的关系
3. **交互操作**:
   - 鼠标滚轮: 缩放
   - 拖拽: 移动视图
   - 点击节点: 查看详情
4. **截图保存**: 这是向客户展示的亮点功能

#### 步骤 4: 测试检索效果

1. **点击** 左侧 "Retrieval" 或 "检索测试"
2. **输入测试问题**:
   ```
   What is the company's policy on remote work?
   ```
3. **点击** "Search" 或 "检索"
4. **查看结果**:
   - 相关文档片段
   - 相似度分数
   - 来源文档引用
5. **继续测试**:
   - `How do I request time off?`
   - `What are the IT security requirements for passwords?`
   - `Who should I contact for expense reimbursement?`
6. **预期结果**: 每个问题都能找到相关的文档片段

#### 步骤 5: 使用 Chat UI 进行对话测试

1. **打开新标签页**，访问: `https://aurora.yansemei.com`
2. **预期结果**: 看到 AuroraAI 对话界面
3. **发送测试消息**:
   ```
   What is the company's vacation policy?
   ```
4. **查看回答**:
   - AI 应该综合知识库信息回答
   - 可能包含多个文档的信息
   - 回答应该有条理
5. **测试多轮对话**:
   ```
   用户: What is the vacation policy?
   AI: [回答]
   用户: How do I apply for it?
   AI: [回答]
   用户: Who approves the request?
   AI: [回答]
   ```
6. **预期结果**: AI 能够保持上下文，进行连贯的多轮对话

#### 步骤 6: 通过 API 集成 (可选)

如果客户需要将 AI 集成到他们的内部系统：

1. **API 端点**: `https://agent.yansemei.com/chat`
2. **请求方式**: POST
3. **Headers**:
   ```
   Content-Type: application/json
   X-API-Key: 8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1
   ```
4. **请求体**:
   ```json
   {
     "query": "What is the vacation policy?",
     "thread_id": "user_123_session_001"
   }
   ```
5. **测试命令** (在 VPS 上执行):
   ```bash
   curl -X POST https://agent.yansemei.com/chat \
     -H "Content-Type: application/json" \
     -H "X-API-Key: 8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1" \
     -d '{"query": "What is the vacation policy?", "thread_id": "test_001"}'
   ```
6. **预期结果**: 返回 JSON 格式的 AI 回答

#### 步骤 7: 交付给客户

**交付物清单:**
1. ✅ Admin UI 访问链接 (文档管理)
2. ✅ Chat UI 访问链接 (员工使用)
3. ✅ API 文档 (如需集成)
4. ✅ 知识图谱截图 (展示数据关联)
5. ✅ 使用培训文档

**客户培训内容:**
```markdown
## 管理员操作指南

### 添加新文档
1. 访问 https://chat.yansemei.com
2. 点击 "Documents" → "Upload"
3. 选择文件上传
4. 等待索引完成 (5-10 分钟)

### 查看使用统计
1. 访问 Admin UI
2. 查看 "Analytics" 或 "统计" 页面
3. 可以看到: 查询次数、热门问题、用户活跃度

### 员工使用指南
1. 访问 https://aurora.yansemei.com
2. 在输入框输入问题
3. AI 会根据公司文档回答
4. 如果答案不满意，可以换个方式提问
```

---

### 预期成果

| 指标 | 目标值 |
|------|--------|
| 文档覆盖率 | 100% 核心文档 |
| 检索准确率 | 85%+ |
| 响应时间 | < 5 秒 |
| 员工采用率 | 60%+ (首月) |

---


## 场景 3: 搭建自动化工作流 (Lead 跟进 + AI 回复)

### 客户背景
- **客户类型**: 营销代理商 / SaaS 销售团队
- **需求**: 自动捕获 leads，AI 生成个性化跟进邮件
- **预算**: $200-$600
- **交付周期**: 3-5 天

### 典型客户需求描述
> "When someone fills out our contact form, I want to automatically: 1) Add them to our CRM, 2) Send a personalized AI-generated email based on their inquiry, 3) Create a follow-up task for our sales team. Currently this takes 15 minutes per lead manually."

### 使用你的系统: n8n + Agent Service

**为什么选择这个组合:**
- n8n 处理工作流编排
- Agent Service 提供 AI 能力
- 可以连接各种第三方服务

---

### 详细操作步骤

#### 步骤 1: 登录 n8n

1. **打开浏览器**，访问: `https://flow.yansemei.com`
2. **首次访问**: 需要创建账号
   - 输入邮箱和密码
   - 完成注册
3. **预期结果**: 看到 n8n 工作流编辑器界面

#### 步骤 2: 创建新工作流

1. **点击** 右上角 "New Workflow" 或 "+"
2. **命名工作流**: `Lead Auto-Response Workflow`
3. **预期结果**: 看到空白的工作流画布

#### 步骤 3: 添加触发器节点

1. **点击** 画布中的 "+" 或 "Add first step"
2. **搜索** "Webhook"
3. **选择** "Webhook" 节点
4. **配置**:
   - HTTP Method: `POST`
   - Path: `lead-capture`
5. **复制 Webhook URL**: 类似 `https://flow.yansemei.com/webhook/xxx/lead-capture`
6. **点击** "Execute" 测试 (保持监听状态)

#### 步骤 4: 添加 AI 处理节点

1. **点击** Webhook 节点右侧的 "+"
2. **搜索** "HTTP Request"
3. **选择** "HTTP Request" 节点
4. **配置**:
   - Method: `POST`
   - URL: `https://agent.yansemei.com/chat`
   - Authentication: `Generic Credential Type`
   - Generic Auth Type: `Header Auth`
   - Header Name: `X-API-Key`
   - Header Value: `8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1`
   - Body Content Type: `JSON`
   - Body:
   ```json
   {
     "query": "Generate a personalized sales follow-up email for a lead with the following information:\nName: {{ $json.name }}\nEmail: {{ $json.email }}\nCompany: {{ $json.company }}\nInquiry: {{ $json.message }}\n\nThe email should be professional, acknowledge their specific inquiry, and suggest a 15-minute call to discuss further.",
     "thread_id": "lead_{{ $json.email }}"
   }
   ```
5. **命名节点**: `AI Generate Email`

#### 步骤 5: 添加邮件发送节点

1. **点击** AI 节点右侧的 "+"
2. **搜索** "Send Email" 或 "Gmail"
3. **选择** 邮件服务节点 (Gmail/SMTP)
4. **配置 Gmail** (需要先设置 OAuth):
   - To: `{{ $('Webhook').item.json.email }}`
   - Subject: `Re: Your inquiry about {{ $('Webhook').item.json.company }}`
   - Body: `{{ $json.response }}` (来自 AI 节点的回复)
5. **命名节点**: `Send Follow-up Email`

#### 步骤 6: 添加 CRM 节点 (可选)

1. **点击** 邮件节点右侧的 "+"
2. **搜索** 客户使用的 CRM (HubSpot/Salesforce/Notion)
3. **以 Notion 为例**:
   - 选择 "Notion" 节点
   - 操作: "Create Database Item"
   - Database: 选择 Leads 数据库
   - 字段映射:
     - Name: `{{ $('Webhook').item.json.name }}`
     - Email: `{{ $('Webhook').item.json.email }}`
     - Company: `{{ $('Webhook').item.json.company }}`
     - Status: `New Lead`
     - AI Response: `{{ $('AI Generate Email').item.json.response }}`

#### 步骤 7: 测试工作流

1. **点击** 右上角 "Execute Workflow"
2. **使用 Postman 或 curl 发送测试请求**:
   ```bash
   curl -X POST https://flow.yansemei.com/webhook/xxx/lead-capture \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Smith",
       "email": "john@example.com",
       "company": "Acme Corp",
       "message": "I am interested in your AI chatbot services for our customer support team."
     }'
   ```
3. **检查每个节点的输出**:
   - Webhook: 应该收到请求数据
   - AI Generate Email: 应该返回个性化邮件内容
   - Send Email: 应该显示发送成功
   - CRM: 应该显示记录创建成功
4. **预期结果**: 整个流程自动执行，无需人工干预

#### 步骤 8: 激活工作流

1. **点击** 右上角的开关，将工作流设为 "Active"
2. **预期结果**: 工作流开始监听 Webhook 请求
3. **测试生产环境**: 再次发送测试请求，确认自动执行

#### 步骤 9: 交付给客户

**交付物清单:**
1. ✅ Webhook URL (用于表单集成)
2. ✅ 工作流截图和说明
3. ✅ 表单集成代码示例
4. ✅ 测试报告

**表单集成示例 (HTML):**
```html
<form id="lead-form">
  <input type="text" name="name" placeholder="Your Name" required>
  <input type="email" name="email" placeholder="Email" required>
  <input type="text" name="company" placeholder="Company">
  <textarea name="message" placeholder="How can we help?"></textarea>
  <button type="submit">Submit</button>
</form>

<script>
document.getElementById('lead-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData);
  
  await fetch('https://flow.yansemei.com/webhook/xxx/lead-capture', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
  alert('Thank you! We will contact you soon.');
});
</script>
```

---

### 完整工作流图

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│   Webhook   │────▶│ AI Generate     │────▶│ Send Email  │────▶│  Add to CRM │
│ (表单提交)  │     │ Email (Agent)   │     │ (Gmail)     │     │  (Notion)   │
└─────────────┘     └─────────────────┘     └─────────────┘     └─────────────┘
```

---

### 预期成果

| 指标 | 之前 (手动) | 之后 (自动化) |
|------|-------------|---------------|
| 处理时间/Lead | 15 分钟 | < 30 秒 |
| 响应延迟 | 2-4 小时 | 即时 |
| 人工成本 | 高 | 几乎为零 |
| 一致性 | 不稳定 | 100% 一致 |

---


## 场景 4: 为 SaaS 产品添加 AI 智能搜索功能

### 客户背景
- **客户类型**: SaaS 产品开发团队
- **需求**: 在现有产品中添加 AI 驱动的语义搜索
- **预算**: $300-$800
- **交付周期**: 5-7 天

### 典型客户需求描述
> "Our SaaS has a help center with 200+ articles. Users complain they can't find what they need. We want to add an AI search that understands natural language queries and returns relevant articles, not just keyword matches."

### 使用你的系统: RAG Core API + 客户前端集成

**为什么选择这个方案:**
- 客户已有前端，只需要 API
- RAG Core 提供语义搜索能力
- 可以返回相关度排序的结果

---

### 详细操作步骤

#### 步骤 1: 准备客户的文档数据

1. **获取客户的帮助文档**:
   - 通常是 Markdown 或 HTML 格式
   - 可能来自 Notion、GitBook、Zendesk 等
2. **整理文档格式**:
   - 每篇文章一个文件
   - 文件名包含标题
   - 内容保持结构化

**示例文档结构:**
```
help-articles/
├── getting-started.md
├── account-settings.md
├── billing-faq.md
├── api-documentation.md
├── troubleshooting-guide.md
└── ...
```

#### 步骤 2: 批量上传文档到 RAG Core

**方法 A: 通过 Admin UI 上传**

1. 访问 `https://chat.yansemei.com`
2. 点击 "Documents" → "Upload"
3. 批量选择所有文档文件
4. 等待索引完成

**方法 B: 通过 API 批量上传** (推荐大量文档)

```bash
# 在 VPS 上执行
cd /home/ai-stack/yansemei-ai-stack/huice

# 将客户文档放入 inputs 目录
cp -r /path/to/customer/docs/* inputs/

# 通过 API 触发索引
curl -X POST https://kb.yansemei.com/documents/scan \
  -H "Authorization: Bearer 75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa"
```

#### 步骤 3: 测试语义搜索

1. **通过 Admin UI 测试**:
   - 访问 `https://chat.yansemei.com`
   - 点击 "Retrieval" 或 "检索测试"
   - 输入自然语言查询: `How do I reset my password?`
   - 查看返回的相关文章

2. **通过 API 测试**:
```bash
curl -X POST https://kb.yansemei.com/query \
  -H "Authorization: Bearer 75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I reset my password?",
    "mode": "hybrid",
    "top_k": 5
  }'
```

3. **预期返回**:
```json
{
  "results": [
    {
      "content": "To reset your password, go to Settings > Security > Change Password...",
      "source": "account-settings.md",
      "score": 0.92
    },
    {
      "content": "If you forgot your password, click 'Forgot Password' on the login page...",
      "source": "troubleshooting-guide.md",
      "score": 0.87
    }
  ]
}
```

#### 步骤 4: 提供 API 文档给客户

**API 端点文档:**

```markdown
## RAG Search API

### Endpoint
`POST https://kb.yansemei.com/query`

### Headers
- `Authorization`: `Bearer YOUR_API_KEY`
- `Content-Type`: `application/json`

### Request Body
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 用户的搜索查询 |
| mode | string | 否 | 搜索模式: `naive`, `local`, `global`, `hybrid` (默认) |
| top_k | number | 否 | 返回结果数量 (默认 5) |

### Response
```json
{
  "results": [
    {
      "content": "文章内容片段",
      "source": "文章来源文件名",
      "score": 0.92
    }
  ]
}
```

### 示例代码 (JavaScript)
```javascript
async function searchHelpArticles(query) {
  const response = await fetch('https://kb.yansemei.com/query', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: query,
      mode: 'hybrid',
      top_k: 5
    })
  });
  
  return await response.json();
}

// 使用示例
const results = await searchHelpArticles('How do I reset my password?');
console.log(results);
```
```

#### 步骤 5: 帮助客户集成到前端

**React 组件示例:**

```jsx
import { useState } from 'react';

function AISearchBox() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('https://kb.yansemei.com/query', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer YOUR_API_KEY',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query: query,
          mode: 'hybrid',
          top_k: 5
        })
      });
      
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-search">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
      />
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Searching...' : 'Search'}
      </button>
      
      <div className="results">
        {results.map((result, index) => (
          <div key={index} className="result-item">
            <p>{result.content}</p>
            <small>Source: {result.source} | Relevance: {(result.score * 100).toFixed(0)}%</small>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AISearchBox;
```

#### 步骤 6: 交付给客户

**交付物清单:**
1. ✅ API Key (专属于客户)
2. ✅ API 文档 (Markdown 格式)
3. ✅ 前端集成代码示例
4. ✅ 测试报告 (搜索准确率)
5. ✅ 文档更新指南

---

### 预期成果

| 指标 | 传统关键词搜索 | AI 语义搜索 |
|------|----------------|-------------|
| 搜索成功率 | 40-50% | 85%+ |
| 用户满意度 | 3.2/5 | 4.5/5 |
| 支持工单量 | 基准 | 减少 30% |

---


## 场景 5: 构建多步骤 AI Agent (研究 + 报告生成)

### 客户背景
- **客户类型**: 咨询公司 / 研究机构
- **需求**: AI 自动研究某个主题，生成结构化报告
- **预算**: $800-$2000
- **交付周期**: 7-14 天

### 典型客户需求描述
> "We need an AI agent that can: 1) Take a research topic, 2) Search our internal knowledge base, 3) Optionally search the web, 4) Synthesize findings into a structured report with citations. Our analysts spend 4-6 hours on each research report."

### 使用你的系统: Agent Service (LangGraph) + RAG Core + n8n

**为什么选择这个方案:**
- 需要多步骤推理 (LangGraph Agent)
- 需要知识库检索 (RAG Core)
- 需要工具调用能力 (MCP)
- 这是你的最高端服务

---

### 详细操作步骤

#### 步骤 1: 理解 Agent 架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      Research Agent                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Plan    │───▶│ Research │───▶│ Analyze  │───▶│  Report  │  │
│  │  Step    │    │  Step    │    │  Step    │    │  Step    │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │               │               │               │          │
│       ▼               ▼               ▼               ▼          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │   LLM    │    │ RAG Core │    │   LLM    │    │   LLM    │  │
│  │ (规划)   │    │ (检索)   │    │ (分析)   │    │ (生成)   │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 步骤 2: 准备知识库

1. **上传客户的研究资料**:
   - 访问 `https://chat.yansemei.com`
   - 上传行业报告、研究论文、内部文档
   - 等待索引完成

2. **验证知识库**:
   - 测试几个相关查询
   - 确保能检索到相关内容

#### 步骤 3: 测试 Agent 对话

1. **访问 Chat UI**: `https://aurora.yansemei.com`

2. **发送研究请求**:
```
Please research the following topic and generate a structured report:

Topic: "AI adoption trends in e-commerce industry 2024"

Requirements:
- Executive summary (200 words)
- Key findings (5-7 bullet points)
- Market data and statistics
- Challenges and opportunities
- Recommendations
- Sources cited
```

3. **观察 Agent 行为**:
   - Agent 会先规划研究步骤
   - 然后查询知识库获取相关信息
   - 分析和综合信息
   - 生成结构化报告

4. **预期输出**:
```markdown
# AI Adoption Trends in E-commerce Industry 2024

## Executive Summary
[200 words summary of key findings...]

## Key Findings
1. AI chatbot adoption increased by 45% in e-commerce...
2. Personalization engines drive 35% higher conversion...
3. ...

## Market Data
- Global AI in e-commerce market: $7.3B (2024)
- Expected CAGR: 29.7% (2024-2030)
- ...

## Challenges
- Data privacy concerns
- Integration complexity
- ...

## Opportunities
- Hyper-personalization
- Voice commerce
- ...

## Recommendations
1. Start with customer service AI...
2. ...

## Sources
- [Source 1]: Internal report on AI adoption...
- [Source 2]: Industry analysis document...
```

#### 步骤 4: 通过 API 调用 Agent

```bash
curl -X POST https://agent.yansemei.com/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: 8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1" \
  -d '{
    "query": "Research and generate a report on AI adoption trends in e-commerce industry 2024. Include executive summary, key findings, market data, challenges, opportunities, and recommendations.",
    "thread_id": "research_project_001"
  }'
```

#### 步骤 5: 创建 n8n 工作流 (批量研究)

如果客户需要批量生成报告：

1. **访问 n8n**: `https://flow.yansemei.com`

2. **创建工作流**:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Schedule   │────▶│ Read Topics │────▶│ Call Agent  │────▶│ Save Report │
│  Trigger    │     │ (Sheets)    │     │   (HTTP)    │     │ (Drive)     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

3. **配置节点**:
   - Schedule Trigger: 每天早上 9 点
   - Read Topics: 从 Google Sheets 读取待研究主题
   - Call Agent: 调用 Agent Service API
   - Save Report: 保存到 Google Drive 或 Notion

#### 步骤 6: 交付给客户

**交付物清单:**
1. ✅ Agent 访问链接 (Chat UI)
2. ✅ API 文档和示例代码
3. ✅ n8n 批量工作流 (如需要)
4. ✅ 知识库管理指南
5. ✅ 报告模板定制说明

**定制报告模板:**
```markdown
## 如何定制报告格式

在发送研究请求时，可以指定报告格式：

### 简短报告
"Generate a brief report (500 words) on [topic] with key findings only."

### 详细报告
"Generate a comprehensive report on [topic] including:
- Executive summary
- Background
- Methodology
- Findings
- Analysis
- Recommendations
- Appendix"

### 特定格式
"Generate a report on [topic] in the following format:
1. 问题背景 (200字)
2. 数据分析 (表格形式)
3. 结论建议 (bullet points)"
```

---

### 预期成果

| 指标 | 人工研究 | AI Agent |
|------|----------|----------|
| 时间/报告 | 4-6 小时 | 5-10 分钟 |
| 成本/报告 | $200-$400 | < $1 (API 费用) |
| 一致性 | 因人而异 | 高度一致 |
| 可扩展性 | 受限于人力 | 无限制 |

---


## 场景对比总结

### 5 个场景的系统使用对比

| 场景 | 主要系统 | 复杂度 | 预算范围 | 交付周期 |
|------|----------|--------|----------|----------|
| 1. 电商 AI 客服 | FastGPT | ⭐⭐ | $200-$500 | 3-5 天 |
| 2. 企业知识库 | Huice (RAG) | ⭐⭐⭐ | $500-$1500 | 5-10 天 |
| 3. Lead 自动化 | n8n + Agent | ⭐⭐⭐ | $200-$600 | 3-5 天 |
| 4. AI 智能搜索 | RAG Core API | ⭐⭐ | $300-$800 | 5-7 天 |
| 5. 研究 Agent | Agent + RAG + n8n | ⭐⭐⭐⭐ | $800-$2000 | 7-14 天 |

### 系统选择决策树

```
客户需求
    │
    ├─► 简单 FAQ 问答？
    │       │
    │       └─► 是 ──► FastGPT (轨道 A)
    │
    ├─► 需要知识图谱/复杂检索？
    │       │
    │       └─► 是 ──► Huice RAG Core (轨道 B)
    │
    ├─► 需要工作流自动化？
    │       │
    │       └─► 是 ──► n8n + Agent Service
    │
    ├─► 只需要 API 集成？
    │       │
    │       └─► 是 ──► RAG Core API / Agent API
    │
    └─► 需要多步骤推理/自主决策？
            │
            └─► 是 ──► Agent Service (LangGraph)
```

---

## 快速参考卡片

### 系统访问地址

| 系统 | URL | 用途 |
|------|-----|------|
| FastGPT | https://demo.yansemei.com | 低代码 AI 应用 |
| OneAPI | https://api.yansemei.com | 模型路由管理 |
| Chat UI | https://aurora.yansemei.com | Agent 对话界面 |
| Admin UI | https://chat.yansemei.com | 知识库管理 |
| RAG API | https://kb.yansemei.com | RAG 检索 API |
| Agent API | https://agent.yansemei.com | Agent 服务 API |
| n8n | https://flow.yansemei.com | 工作流自动化 |

### API 密钥速查

| 服务 | Header | Key |
|------|--------|-----|
| Agent Service | X-API-Key | 8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1 |
| RAG Core | Authorization | Bearer 75f5b78ed421819d66394293e843872ef2fc2b74909da6b5edcce7d8f1eb33fa |
| OneAPI | Authorization | Bearer sk-kLGqLaHr4OsT8i7oBdE99725Fe7b45F78d2bB97119831086 |

### 登录凭证速查

| 系统 | 用户名 | 密码 |
|------|--------|------|
| FastGPT | root | FastGPT2025Admin! |
| OneAPI | root | 123456 (需修改!) |

---

## 客户沟通话术模板

### 初次咨询回复

```
Hi [Client Name],

Thank you for reaching out! Based on your requirements, I can help you build [specific solution].

Here's what I can deliver:
✅ [Deliverable 1]
✅ [Deliverable 2]
✅ [Deliverable 3]

Timeline: [X] days
Investment: $[amount]

I have a live demo you can try: [relevant URL]

Would you like to schedule a quick call to discuss the details?

Best,
[Your Name]
```

### 项目完成交付

```
Hi [Client Name],

Great news! Your [project name] is ready! 🎉

Here's what's been delivered:
1. [Deliverable 1] - [URL/Access info]
2. [Deliverable 2] - [URL/Access info]
3. Documentation - [Attached/Link]

Quick start guide:
1. [Step 1]
2. [Step 2]
3. [Step 3]

I've also included a guide for [maintenance/updates].

Please test it out and let me know if you have any questions!

Best,
[Your Name]
```

---

*文档版本: 1.0*
*最后更新: 2025-12-26*
*基于 Fiverr/Upwork 2024-2025 市场数据*
