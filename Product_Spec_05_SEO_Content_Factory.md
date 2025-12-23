# Product Spec 05: SEO 内容自动生成工厂 (Content Factory)

> **基于梁宁“真需求”理论分析**：流量是互联网生意的血液。对于依靠 SEO（搜索引擎优化）获客的企业，内容的“产量”和“质量”直接决定了生死。本产品解决的是 **“高人力成本 vs 规模化获客”** 之间的矛盾。

---

## 1. 产品定义 (Product Definition)

### 1.1 一句话描述 (Elevator Pitch)
搭建一条 24 小时不停工的“AI 编辑部”，从关键词挖掘到大纲策划，再到长文撰写与发布，全链路自动化，批量生产符合 Google/百度 SEO 标准的高质量内容。

### 1.2 核心价值主张 (Value Proposition)
* **痛点 (Pain - 恐惧)**：
    * **流量枯竭**：不写文章就没有流量，但人工写一篇高质量长文需要 1-2 天，成本太高。
    * **排名下跌**：更新频率跟不上，排名被竞争对手挤下去。
* **爽点 (Pleasure)**：
    * **规模化打击**：一夜之间覆盖行业内 1000 个长尾关键词。
    * **躺赚模式**：设置好关键词表，系统每天自动发文，流量像自来水一样慢慢涨起来。
* **差异化竞争优势**：
    * 相比 **纯 AI 生成**：我们引入 **“Human-in-the-loop (人工审核)”** 节点，确保不发垃圾内容。
    * **SEO 深度优化**：集成关键词密度控制、内链自动插入、H 标签结构化，符合搜索引擎喜好。

---

## 2. 用户画像 (User Persona)

### 2.1 核心用户 (大明 - 需求清晰)
* **角色 A：Niche 站长 / 个人博主**
    * **痛点**：一个人要干 10 个人的活，写文章写到吐。
    * **诉求**：保持网站活跃度，用海量内容博取长尾流量。
* **角色 B：企业内容营销经理**
    * **痛点**：外包写手质量参差不齐，管理成本高。

### 2.2 用户体验地图 (User Experience Map)

| 阶段 | 触点 | 用户情绪 | 现有土办法 | AI 产品机会点 |
| :--- | :--- | :--- | :--- | :--- |
| **选题策划** | 关键词工具 | 迷茫 | 手工挑词，填 Excel | **自动拉取 SEMRush/Ahrefs 数据，AI 聚类选题** |
| **内容撰写** | Word | 枯燥/低效 | 憋字数，查资料 | **AI 基于 SERP 前 10 结果，生成更全的大纲与正文** |
| **配图排版** | CMS 后台 | 繁琐 | 找免费图，手动排版 | **AI 自动配图 (Unsplash/DALL-E)，Markdown 自动转 HTML** |
| **发布推广** | 网站/社媒 | 机械 | 登录后台，点击发布 | **API 自动发布到 WordPress/Ghost/Webflow** |

---

## 3. 场景与功能架构

### 3.1 核心场景
1.  **批量长尾覆盖**：
    *   针对“怎么选咖啡机”、“2025 最好的蓝牙耳机”等 500 个长尾词，批量生成 1500 字以上的评测/指南文章。
2.  **热点资讯跟进**：
    *   监控行业新闻（如：DeepSeek 发布新模型），1 小时内自动生成一篇深度解读并发布。

### 3.2 技术架构 (The Stack)

```mermaid
graph TD
    Keywords[Google Sheets 关键词表] -->|Schedule| n8n[n8n Workflow]
    
    subgraph "AI Editorial Room"
        n8n -->|1. Outline| Agent_Editor[主编 Agent: 审大纲]
        Agent_Editor -->|Approved| Agent_Writer[写手 Agent: 写正文]
        Agent_Writer -->|Draft| Agent_SEO[SEO 专家 Agent: 优化关键词]
        Agent_SEO -->|Review| Human[人工审核 (可选)]
    end
    
    subgraph "Publishing"
        Human -->|Approve| WordPress[发布到 WordPress]
        WordPress -->|Link| Social[分发到 Twitter/LinkedIn]
    end
    
    Agent_Writer -.->|Call| OneAPI[OneAPI (DeepSeek)]
```

---

## 4. 实施路线图 (Implementation Roadmap)

### Phase 1: 辅助写作 (2 周)
*   **目标**：人机耦合，提升 5 倍效率。
*   **功能**：输入关键词 -> AI 生成大纲 -> 人工调整 -> AI 生成正文 -> 人工润色发布。
*   **交付**：n8n 半自动化工作流。

### Phase 2: 全自动流水线 (1 个月)
*   **目标**：无人值守，批量生产。
*   **功能**：读取表格 -> 批量生成 -> 自动配图 -> 存入草稿箱（等待一键发布）。
*   **交付**：支持批量处理的 n8n Loop 工作流。

### Phase 3: 智能 SEO 优化 (2 个月)
*   **目标**：提升收录率和排名。
*   **功能**：自动插入内链（Internal Linking），自动检测关键词密度，自动生成 Meta Description。

---

## 5. 交付标准与物料清单

1.  **n8n Workflow**：`Content_Factory_v1.json`（含 Loop 节点和 WordPress 节点）。
2.  **Prompt 调优包**：
    *   `Outline_Generator.md`（生成逻辑清晰的大纲）
    *   `Article_Writer.md`（生成语气自然、非 AI 味的正文）
3.  **运营 SOP**：
    *   《如何构建高价值关键词库》.pdf
    *   《AI 文章的人工审核标准》.md

---

## 6. 附录：风险提示
*   **Google 算法更新**：纯 AI 内容可能被降权。
*   **对策**：强调 **E-E-A-T**（经验、专业、权威、信任），必须在 AI 内容中加入独特的观点、数据或案例，这也是为什么我们保留“人工审核”节点的原因。
