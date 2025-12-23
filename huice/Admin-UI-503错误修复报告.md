# Admin UI 503/500 代理错误修复报告

## 问题描述

在 Admin UI (端口 5173) 中访问文档管理功能时，出现以下错误：
- `503 Service Unavailable` - `/documents/paginated`
- `500 Internal Server Error` - `/documents/upload`

## 根本原因分析

经过深入分析，发现问题的**根本原因**是：

### 系统设置了 HTTP_PROXY 环境变量

```bash
HTTP_PROXY=http://xc999:xc123@154.40.43.229:38903
```

这导致 Vite 的 `http-proxy` 中间件在代理请求时，会尝试通过这个外部代理服务器连接本地的 RAG Core 服务 (`127.0.0.1:9621`)，而不是直接连接。

### 问题链路

```
浏览器 → Vite Dev Server (5173) → HTTP_PROXY (外部代理) → RAG Core (9621)
                                        ↑
                                   连接失败！
```

外部代理服务器无法访问本地的 `127.0.0.1:9621`，因此返回 503/500 错误。

## 解决方案

### 1. 修改 `start_all.py` - 启动 Admin UI 时清除代理环境变量

```python
# 5. Start Admin UI (Management Interface)
print("\n[5/5] Starting Admin UI...")
admin_ui_cmd = "bun run dev" if os.path.exists(...) else "npm run dev"

# 关键修复：清除代理环境变量，防止 Vite http-proxy 通过系统代理连接本地服务
admin_env = os.environ.copy()
admin_env["HTTP_PROXY"] = ""
admin_env["HTTPS_PROXY"] = ""
admin_env["http_proxy"] = ""
admin_env["https_proxy"] = ""

p_admin = run_service("Admin UI", admin_ui_cmd, cwd=..., env=admin_env)
```

### 2. 修改 `admin-ui/vite.config.ts` - 使用 IPv4 地址

```typescript
// RAG Core 后端地址 - 使用 IPv4 地址连接 (RAG Core 监听 0.0.0.0)
const BACKEND_URL = 'http://127.0.0.1:9621'

const proxyOptions = {
  target: BACKEND_URL,
  changeOrigin: true,
  secure: false
}
```

### 3. 修改 `start_all.py` - RAG Core 使用 IPv4 监听

```python
# 使用 0.0.0.0 监听所有 IPv4 地址 (macOS 上更可靠)
rag_api_cmd = f"{ENV_PYTHON} -m lightrag.api.lightrag_server --host 0.0.0.0 --port {PORTS['rag_api']}"
```

### 4. 更新 Python 路径配置

添加了 Homebrew miniconda 的路径支持：

```python
POSSIBLE_PYTHON_PATHS = [
    # Homebrew miniconda (macOS)
    "/opt/homebrew/Caskroom/miniconda/base/envs/rag-env/bin/python",
    # ... 其他路径
]
```

## 修改的文件

1. **`start_all.py`**
   - 添加 Homebrew miniconda Python 路径
   - RAG Core 使用 `0.0.0.0` 监听
   - Admin UI 启动时清除代理环境变量

2. **`admin-ui/vite.config.ts`**
   - 代理目标改为 `http://127.0.0.1:9621`
   - 简化代理配置

## 验证结果

修复后测试：

```bash
# 文档列表 - 成功
curl http://localhost:5173/documents/paginated -X POST \
  -H "Content-Type: application/json" \
  -d '{"page":1,"page_size":10,"sort_field":"created_at","sort_direction":"desc"}'
# 返回: HTTP/1.1 200 OK

# 文件上传 - 成功
curl http://localhost:5173/documents/upload -F "file=@test.txt"
# 返回: {"status":"success","message":"File 'test.txt' uploaded successfully..."}
```

## 经验教训

1. **环境变量影响**：系统级的代理设置会影响 Node.js 应用的网络请求
2. **本地服务连接**：本地服务之间的通信应该绕过系统代理
3. **IPv4 vs IPv6**：在 macOS 上，使用 IPv4 (`0.0.0.0`/`127.0.0.1`) 比 IPv6 (`::`) 更可靠
4. **调试方法**：检查 `env | grep -i proxy` 可以快速发现代理相关问题

## 额外修复：健康检查也受代理影响

`start_all.py` 中的健康检查使用 `urllib.request`，也会受到 `HTTP_PROXY` 环境变量的影响。

修复方法：创建不使用代理的 opener：

```python
# 创建不使用代理的 opener
no_proxy_handler = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(no_proxy_handler)

# 使用 opener 进行健康检查
req = opener.open(f"http://127.0.0.1:{PORTS['rag_api']}/health", timeout=2)
```

## 后续建议

如果用户在其他环境中遇到类似问题，可以：

1. 手动启动时清除代理：
   ```bash
   HTTP_PROXY= HTTPS_PROXY= npm run dev
   ```

2. 或在 `.bashrc`/`.zshrc` 中为本地开发设置 `NO_PROXY`：
   ```bash
   export NO_PROXY=localhost,127.0.0.1
   ```

3. 使用 `start_all.py` 启动所有服务（已内置代理绕过逻辑）
