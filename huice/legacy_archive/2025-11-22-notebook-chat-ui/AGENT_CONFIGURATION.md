# 智能体链接配置指南

## 概述

本项目支持两个独立的智能体：
1. **源代理 (Source Agent)** - 处理左侧"添加来源"上传的文件
2. **聊天代理 (Chat Agent)** - 处理中间对话区域的消息

所有配置都在 `.env` 文件中进行，支持灵活的环境切换。

## 环境变量配置

### 基础配置

```env
# LangGraph API 服务器地址
NEXT_PUBLIC_API_URL=http://localhost:2025

# 默认助手 ID
NEXT_PUBLIC_ASSISTANT_ID=agent

# LangSmith API Key
LANGSMITH_API_KEY=danwen
```

### 智能体链接配置

```env
# 聊天代理 - 前端 UI 链接（用于中间对话区域）
NEXT_PUBLIC_CHAT_AGENT_URL=http://localhost:3002/?apiUrl=http://localhost:2025&assistantId=chat_agent

# 源代理 - 前端 UI 链接（用于左侧添加来源）
NEXT_PUBLIC_SOURCE_AGENT_URL=http://localhost:3002/?apiUrl=http://localhost:2025&assistantId=source_agent
```

**注意**：源代理和聊天代理的 API 通信都通过 `NEXT_PUBLIC_API_URL` 进行，使用 LangGraph SDK Client 自动处理。

## 工作流程

### 源代理工作流程

```
用户操作：
1. 点击左侧"+ 添加来源"按钮
   ↓
2. 选择文件（支持图片和 PDF）
   ↓
3. 文件显示在列表中
   ↓
4. 点击"确认"按钮
   ↓
5. 系统使用 LangGraph SDK Client 创建一个新的线程
   ↓
6. 使用 Client.runs.create() 提交文件到源代理
   ↓
7. 显示成功/失败提示
```

### 聊天代理工作流程

```
用户操作：
1. 在中间对话区域输入消息
   ↓
2. 点击发送按钮
   ↓
3. 消息发送到聊天代理
   ↓
4. 接收 AI 响应
```

## 配置示例

### 本地开发环境

```env
NEXT_PUBLIC_API_URL=http://localhost:2025
NEXT_PUBLIC_ASSISTANT_ID=agent
LANGSMITH_API_KEY=danwen
```

### 生产环境

```env
NEXT_PUBLIC_API_URL=https://your-api-server.com/api
NEXT_PUBLIC_ASSISTANT_ID=agent
LANGSMITH_API_KEY=lsv2_your_key_here
```

### 自定义智能体 ID

源代理的 ID 在 `src/hooks/use-source-agent.ts` 中硬编码为 `"source_agent"`。如果需要修改，请编辑该文件：

```typescript
const sourceAgentId = "source_agent"; // 修改为您的智能体 ID
```

## 支持的文件类型

源代理支持以下文件类型：
- **图片**: JPEG, PNG, GIF, WebP
- **文档**: PDF

## 实现细节

### 使用 LangGraph SDK Client

源代理功能使用 LangGraph SDK 的 Client 类来与 LangGraph 服务器通信：

```typescript
import { Client } from "@langchain/langgraph-sdk";
import { getApiKey } from "@/lib/api-key";

// 创建客户端
const client = new Client({
  apiUrl: process.env.NEXT_PUBLIC_API_URL,
  apiKey: getApiKey() ?? undefined,
});

// 创建线程
const thread = await client.threads.create();

// 提交消息到源代理
const run = await client.runs.create(threadId, "source_agent", {
  input: {
    messages: [
      {
        role: "user",
        content: contentBlocks, // ContentBlock.Multimodal.Data[]
      },
    ],
  },
});
```

### 支持的内容块类型

```typescript
// 图片
{
  type: "image",
  mimeType: "image/png",
  data: "base64_encoded_data",
  metadata: { name: "image.png" }
}

// PDF 文件
{
  type: "file",
  mimeType: "application/pdf",
  data: "base64_encoded_data",
  metadata: { filename: "document.pdf" }
}
```

## 错误处理

系统会自动处理以下错误情况：

1. **配置缺失** - 如果环境变量未配置，显示错误提示
2. **网络错误** - 如果 API 请求失败，显示错误信息
3. **文件验证** - 如果文件类型不支持，显示警告
4. **重复文件** - 如果上传重复文件，显示提示

## 调试

### 查看环境变量

在浏览器控制台中运行：
```javascript
console.log(process.env.NEXT_PUBLIC_SOURCE_AGENT_API_URL)
console.log(process.env.NEXT_PUBLIC_CHAT_AGENT_API_URL)
```

### 查看网络请求

1. 打开浏览器开发者工具 (F12)
2. 切换到 "Network" 标签
3. 点击"确认"按钮
4. 查看 POST 请求的详情

## 常见问题

### Q: 如何修改智能体 ID？
A: 编辑 `.env` 文件中的 `NEXT_PUBLIC_SOURCE_AGENT_API_URL` 和 `NEXT_PUBLIC_CHAT_AGENT_API_URL`，将 `source_agent` 和 `chat_agent` 替换为您的智能体 ID。

### Q: 支持哪些文件类型？
A: 支持 JPEG, PNG, GIF, WebP 图片和 PDF 文档。

### Q: 如何处理 CORS 错误？
A: 确保您的 API 服务器配置了正确的 CORS 头。

### Q: 如何在生产环境中使用？
A: 将 `.env` 文件中的 `localhost` 替换为您的生产服务器地址。

## 相关文件

- `.env` - 环境变量配置
- `src/hooks/use-source-agent.ts` - 源代理 Hook
- `src/components/thread/SourcesPanel.tsx` - 源面板组件
- `src/components/thread/index.tsx` - 主线程组件
