# VPS 架构优化实施任务清单

> 创建日期: 2025-12-26
> 状态: 进行中
> 预计工时: 6-8 小时

---

## 任务概览

- [x] **Phase 0**: 清理系统垃圾 (已完成)
  - Docker build cache: 4.84GB 已释放
  - 未使用卷: 32 个已删除
  - 系统日志: 192MB 已释放
  - 删除 `/home/ai-stack/fiverr` (旧重复目录)
- [ ] **Phase 1**: 部署 FastGPT/OneAPI (进行中)
- [ ] **Phase 2**: 集成 FastGPT 与 Huice (待开始)
- [ ] **Phase 3**: 更新文档与配置 (部分完成)
- [ ] **Phase 4**: 测试验证 (待开始)

---

## Phase 1: 诊断与修复 FastGPT/OneAPI

### 1.1 诊断当前状态

- [ ] **1.1.1 SSH 连接到 VPS**
  ```bash
  ssh root@148.135.57.133
  # 或使用你配置的 SSH 别名
  ```

- [ ] **1.1.2 检查所有容器状态**
  ```bash
  docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
  ```
  
  预期看到的容器：
  - `fastgpt` - 应该运行中
  - `oneapi` - 应该运行中
  - `pg` - 应该运行中
  - `mongo` - 应该运行中
  - `redis` - 应该运行中
  - `huice-rag-core` - 应该运行中
  - `huice-mcp` - 应该运行中
  - `huice-agent-service` - 应该运行中
  - `huice-chat-ui` - 应该运行中
  - `huice-admin-ui` - 应该运行中
  - `n8n` - 应该运行中
  - `npm-app-1` - 应该运行中

- [ ] **1.1.3 检查 FastGPT 日志**
  ```bash
  docker logs fastgpt --tail 200
  ```
  
  记录错误信息：
  ```
  [在这里记录看到的错误]
  ```

- [ ] **1.1.4 检查 OneAPI 日志**
  ```bash
  docker logs oneapi --tail 200
  ```
  
  记录错误信息：
  ```
  [在这里记录看到的错误]
  ```

- [ ] **1.1.5 检查 NPM 代理配置**
  ```bash
  # 临时开放 81 端口
  ufw allow from $(curl -s ifconfig.me) to any port 81
  
  # 访问 NPM 管理界面
  # http://148.135.57.133:81
  # 账号: admin@example.com
  # 密码: [你设置的密码]
  
  # 检查 demo.yansemei.com 和 api.yansemei.com 的代理配置
  ```

### 1.2 修复 FastGPT

- [ ] **1.2.1 查看 FastGPT docker-compose 配置**
  ```bash
  cd /home/ai-stack/yansemei-ai-stack/huice
  cat docker-compose.yml | grep -A 50 fastgpt
  ```
  
  或者查看独立的 FastGPT compose 文件：
  ```bash
  ls -la /home/ai-stack/
  # 找到 FastGPT 的 docker-compose.yml 位置
  ```

- [ ] **1.2.2 检查 FastGPT 环境变量**
  ```bash
  # 查看 FastGPT 的 .env 或 config.json
  cat /home/ai-stack/huice/config.json 2>/dev/null || echo "config.json 不存在"
  cat /home/ai-stack/huice/.env 2>/dev/null || echo ".env 不存在"
  ```

- [ ] **1.2.3 重启 FastGPT 相关服务**
  ```bash
  cd /home/ai-stack/yansemei-ai-stack/huice
  # 或 FastGPT 所在的目录
  
  docker compose restart pg mongo redis
  sleep 10
  docker compose restart oneapi
  sleep 5
  docker compose restart fastgpt
  ```

- [ ] **1.2.4 验证 FastGPT 启动**
  ```bash
  # 等待 30 秒让服务完全启动
  sleep 30
  
  # 检查容器状态
  docker ps | grep fastgpt
  
  # 测试内部连接
  curl -s http://localhost:3001/api/health
  
  # 测试外部连接
  curl -s https://demo.yansemei.com/api/health
  ```

### 1.3 修复 OneAPI

- [ ] **1.3.1 重启 OneAPI**
  ```bash
  docker restart oneapi
  sleep 10
  
  # 检查状态
  docker ps | grep oneapi
  
  # 测试连接
  curl -s http://localhost:3002/api/status
  ```

- [ ] **1.3.2 配置 OneAPI 渠道**
  
  访问 OneAPI 管理界面：
  - URL: `https://api.yansemei.com` 或 `http://148.135.57.133:3002`
  - 账号: `root`
  - 密码: `123456` (首次登录后修改!)
  
  添加 SiliconFlow 渠道：
  1. 进入 "渠道" 页面
  2. 点击 "添加渠道"
  3. 配置如下：
     - 类型: `OpenAI`
     - 名称: `SiliconFlow`
     - Base URL: `https://api.siliconflow.cn/v1`
     - API Key: `sk-ebuinjyygubsompogzhgmvabmtizghsuewvhvdfkohlrntyt`
     - 模型: 
       - `deepseek-ai/DeepSeek-V3`
       - `Qwen/Qwen2.5-7B-Instruct`
       - `BAAI/bge-m3` (Embedding)

- [ ] **1.3.3 测试 OneAPI**
  ```bash
  # 获取 OneAPI 的 API Key (在管理界面创建)
  # 测试调用
  curl https://api.yansemei.com/v1/chat/completions \
    -H "Authorization: Bearer YOUR_ONEAPI_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "deepseek-ai/DeepSeek-V3",
      "messages": [{"role": "user", "content": "Hello"}]
    }'
  ```

### 1.4 验证 NPM 代理配置

- [ ] **1.4.1 检查所有域名代理**
  
  在 NPM 管理界面检查以下域名配置：
  
  | 域名 | 目标 | SSL | 状态 |
  |------|------|-----|------|
  | demo.yansemei.com | fastgpt:3001 | ✅ | [ ] 已配置 |
  | api.yansemei.com | oneapi:3002 | ✅ | [ ] 已配置 |
  | aurora.yansemei.com | huice-chat-ui:3000 | ✅ | [ ] 已配置 |
  | agent.yansemei.com | huice-agent-service:2025 | ✅ | [ ] 已配置 |
  | chat.yansemei.com | huice-admin-ui:5173 | ✅ | [ ] 已配置 |
  | kb.yansemei.com | huice-rag-core:9621 | ✅ | [ ] 已配置 |
  | flow.yansemei.com | n8n:5678 | ✅ | [ ] 已配置 |

- [ ] **1.4.2 关闭 NPM 管理端口**
  ```bash
  # 完成配置后，关闭 81 端口
  ufw delete allow from $(curl -s ifconfig.me) to any port 81
  ```

---

## Phase 2: 集成 FastGPT 与 Huice

### 2.1 配置 FastGPT 调用 Huice

- [ ] **2.1.1 登录 FastGPT**
  
  访问: `https://demo.yansemei.com`
  账号: `root`
  密码: `MyFastGPTPass2025!`

- [ ] **2.1.2 创建测试应用**
  
  1. 点击 "新建应用"
  2. 选择 "高级编排"
  3. 命名为 "Huice Agent 集成测试"

- [ ] **2.1.3 添加 HTTP 节点**
  
  在 Flow 编辑器中：
  1. 添加 "HTTP 请求" 节点
  2. 配置如下：
     - URL: `https://agent.yansemei.com/chat`
     - 方法: `POST`
     - Headers:
       ```json
       {
         "Content-Type": "application/json",
         "X-API-Key": "8809969bcdb6fceaafe906f1788b90a0401f36453c89bddccff106e46bc568c1"
       }
       ```
     - Body:
       ```json
       {
         "query": "{{q}}",
         "thread_id": "fastgpt_{{appId}}_{{chatId}}"
       }
       ```

- [ ] **2.1.4 测试集成**
  
  1. 保存 Flow
  2. 点击 "调试"
  3. 发送测试消息
  4. 验证返回结果

### 2.2 配置 n8n 调用 Huice

- [ ] **2.2.1 登录 n8n**
  
  访问: `https://flow.yansemei.com`

- [ ] **2.2.2 创建测试工作流**
  
  1. 创建新工作流
  2. 添加 "Manual Trigger" 节点
  3. 添加 "HTTP Request" 节点
  4. 配置如下：
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
         "query": "你好，这是一个测试消息",
         "thread_id": "n8n_test_001"
       }
       ```

- [ ] **2.2.3 测试工作流**
  
  1. 保存工作流
  2. 点击 "Execute Workflow"
  3. 验证返回结果

---

## Phase 3: 更新文档与配置

### 3.1 更新本地文档

- [ ] **3.1.1 更新 System_Architecture_Huice_Yansemei.md**
  - 添加双轨制策略说明
  - 更新架构图
  - 更新服务清单

- [ ] **3.1.2 更新 Server_Credentials_Final.md**
  - 确认所有凭证正确
  - 添加 OneAPI 配置信息
  - 更新服务状态

- [ ] **3.1.3 更新 huice/Security_Config_Record.md**
  - 添加 FastGPT 安全配置
  - 添加 OneAPI 安全配置
  - 更新域名列表

- [ ] **3.1.4 更新 AI_Product_Packages.md**
  - 添加双轨制交付说明
  - 更新产品方案

### 3.2 同步到 VPS

- [ ] **3.2.1 提交本地更改**
  ```bash
  cd ~/fiverr  # 或你的本地仓库路径
  git add .
  git commit -m "feat: 实施双轨制架构优化"
  git push
  ```

- [ ] **3.2.2 在 VPS 上拉取更新**
  ```bash
  ssh root@148.135.57.133
  cd /home/ai-stack/yansemei-ai-stack
  git pull
  ```

---

## Phase 4: 测试验证

### 4.1 服务健康检查

- [ ] **4.1.1 检查所有服务**
  ```bash
  # FastGPT
  curl -s https://demo.yansemei.com/api/health && echo " ✅ FastGPT"
  
  # OneAPI
  curl -s https://api.yansemei.com/api/status && echo " ✅ OneAPI"
  
  # RAG Core
  curl -s https://kb.yansemei.com/health && echo " ✅ RAG Core"
  
  # Agent Service
  curl -s https://agent.yansemei.com/ok && echo " ✅ Agent Service"
  
  # Chat UI
  curl -s -o /dev/null -w "%{http_code}" https://aurora.yansemei.com && echo " ✅ Chat UI"
  
  # Admin UI
  curl -s -o /dev/null -w "%{http_code}" https://chat.yansemei.com && echo " ✅ Admin UI"
  
  # n8n
  curl -s -o /dev/null -w "%{http_code}" https://flow.yansemei.com && echo " ✅ n8n"
  ```

### 4.2 功能测试

- [ ] **4.2.1 测试 FastGPT 基本功能**
  1. 访问 https://demo.yansemei.com
  2. 登录管理后台
  3. 创建简单知识库
  4. 创建简单应用
  5. 测试对话功能

- [ ] **4.2.2 测试 Huice 基本功能**
  1. 访问 https://aurora.yansemei.com
  2. 发送测试消息
  3. 验证 Agent 响应

- [ ] **4.2.3 测试 FastGPT → Huice 集成**
  1. 使用之前创建的集成测试应用
  2. 发送复杂问题
  3. 验证 Huice Agent 被调用

- [ ] **4.2.4 测试 n8n → Huice 集成**
  1. 执行之前创建的测试工作流
  2. 验证返回结果

### 4.3 记录测试结果

| 测试项 | 状态 | 备注 |
|--------|------|------|
| FastGPT 访问 | [ ] | |
| OneAPI 访问 | [ ] | |
| FastGPT 知识库 | [ ] | |
| FastGPT 对话 | [ ] | |
| Huice Agent 对话 | [ ] | |
| FastGPT → Huice | [ ] | |
| n8n → Huice | [ ] | |

---

## 故障排查指南

### 常见问题

**问题 1: FastGPT 502 错误**
```bash
# 检查容器状态
docker ps -a | grep fastgpt

# 查看日志
docker logs fastgpt --tail 100

# 常见原因:
# 1. 数据库连接失败 - 检查 pg/mongo/redis 是否运行
# 2. 配置错误 - 检查 config.json 或 .env
# 3. 端口冲突 - 检查 3001 端口是否被占用
```

**问题 2: OneAPI 无响应**
```bash
# 检查容器状态
docker ps -a | grep oneapi

# 查看日志
docker logs oneapi --tail 100

# 常见原因:
# 1. 容器未启动 - docker start oneapi
# 2. 端口未暴露 - 检查 docker-compose.yml
# 3. NPM 代理配置错误 - 检查 NPM 设置
```

**问题 3: NPM 代理不工作**
```bash
# 检查 NPM 容器
docker ps | grep npm

# 查看 NPM 日志
docker logs npm-app-1 --tail 100

# 常见原因:
# 1. SSL 证书过期 - 在 NPM 中重新申请
# 2. 目标服务未运行 - 检查目标容器
# 3. 网络配置错误 - 确保都在 npm_default 网络
```

---

## 完成检查清单

- [ ] FastGPT (demo.yansemei.com) 可正常访问
- [ ] OneAPI (api.yansemei.com) 可正常访问
- [ ] OneAPI 已配置 SiliconFlow 渠道
- [ ] FastGPT 可调用 Huice Agent
- [ ] n8n 可调用 Huice Agent
- [ ] 所有文档已更新
- [ ] 代码已同步到 VPS

---

*任务清单版本: 1.0*
*最后更新: 2025-12-26*
