import subprocess
import sys
import os
import time
import signal
import platform

# --- Configuration ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Try to locate the conda environment python
POSSIBLE_PYTHON_PATHS = [
    # Homebrew miniconda (macOS)
    "/opt/homebrew/Caskroom/miniconda/base/envs/rag-env/bin/python",
    # Standard anaconda paths
    os.path.expanduser("~/anaconda3/envs/rag-env/bin/python"),
    os.path.expanduser("~/opt/anaconda3/envs/rag-env/bin/python"),
    os.path.expanduser("~/miniconda3/envs/rag-env/bin/python"),
    os.path.expanduser("~/.conda/envs/rag-env/bin/python"),
    sys.executable
]

ENV_PYTHON = "python"
for path in POSSIBLE_PYTHON_PATHS:
    if os.path.exists(path):
        ENV_PYTHON = path
        break

print(f"🚀 Using Python interpreter: {ENV_PYTHON}")

# Ports configuration
PORTS = {
    "rag_api": 9621,   # LightRAG Core API (Backend for Admin UI)
    "mcp": 8001,       # MCP Server (Tool Interface)
    "agent": 2025,     # Agent Service (LangGraph Brain)
    "chat_ui": 3000,   # User Chat Interface
    "admin_ui": 5173   # Admin Management Interface
}

# --- Helper Functions ---

def run_service(name, command, cwd=None, env=None):
    """Runs a service in a subprocess."""
    print(f"Starting {name}...")
    if cwd:
        print(f"  📂 Working Directory: {cwd}")
    
    if env is None:
        env = os.environ.copy()
    
    # CRITICAL: Add project roots to PYTHONPATH
    # This allows mcp-server to import raganything from rag-core
    # and agent-service to import everything needed.
    current_pythonpath = env.get("PYTHONPATH", "")
    new_pythonpath = (
        f"{ROOT_DIR}/rag-core:"      # Core logic (LightRAG + RagAnything)
        f"{ROOT_DIR}/mcp-server/src:" # MCP Server logic
        f"{ROOT_DIR}/agent-service/src:" # Agent logic
        f"{current_pythonpath}"
    )
    env["PYTHONPATH"] = new_pythonpath
    
    try:
        process = subprocess.Popen(
            command, 
            cwd=cwd, 
            env=env, 
            shell=True,
            preexec_fn=os.setsid if platform.system() != "Windows" else None
        )
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def kill_process_group(process):
    """Kills a process and its children."""
    if not process:
        return
    try:
        if platform.system() != "Windows":
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        else:
            process.terminate()
    except Exception:
        pass

def cleanup_ports(ports):
    """Kills processes listening on specified ports."""
    print("🧹 Cleaning up ports...")
    for name, port in ports.items():
        try:
            # Find process ID using lsof (macOS/Linux)
            # -t: terse output (PID only)
            # -i: select internet files
            cmd = f"lsof -t -i :{port}"
            pid_bytes = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
            pids = pid_bytes.decode().strip().split('\n')
            
            for pid in pids:
                if pid:
                    print(f"   - Killing process {pid} on port {port} ({name})")
                    os.kill(int(pid), signal.SIGKILL)
        except subprocess.CalledProcessError:
            # No process found on this port
            pass
        except Exception as e:
            print(f"   ⚠️ Failed to clean up port {port}: {e}")

# --- Main Execution ---

def main():
    processes = []
    
    # Clean up existing processes first
    cleanup_ports(PORTS)
    
    try:
        # 1. Start LightRAG API Server (Core Engine)
        # Provides API for Admin UI to manage knowledge base
        print("\n[1/5] Starting RAG Core API...")
        # 使用 0.0.0.0 监听所有 IPv4 地址 (macOS 上更可靠)
        # Vite 代理配置为 127.0.0.1:9621 连接
        rag_api_cmd = f"{ENV_PYTHON} -m lightrag.api.lightrag_server --host 0.0.0.0 --port {PORTS['rag_api']}"
        p_rag = run_service("RAG Core API", rag_api_cmd, cwd=os.path.join(ROOT_DIR, "rag-core"))
        processes.append(p_rag)
        
        # Wait for RAG Core to be fully ready (health check)
        print("   ⏳ Waiting for RAG Core to be ready...")
        import urllib.request
        
        # 关键修复：创建不使用代理的 opener，绕过系统 HTTP_PROXY 环境变量
        no_proxy_handler = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(no_proxy_handler)
        
        max_retries = 30  # 30 seconds max
        for i in range(max_retries):
            try:
                # 使用 127.0.0.1 直接连接 IPv4，避免 IPv6 问题
                req = opener.open(f"http://127.0.0.1:{PORTS['rag_api']}/health", timeout=2)
                if req.status == 200:
                    print("   ✅ RAG Core is ready!")
                    break
            except Exception:
                pass
            time.sleep(1)
            if i % 5 == 4:
                print(f"   ⏳ Still waiting... ({i+1}s)")
        else:
            print("   ⚠️ RAG Core may not be fully ready, continuing anyway...")
        
        # 2. Start MCP Server (Tool Provider)
        # Provides tools for the Agent
        print("\n[2/5] Starting MCP Server...")
            
        # Run server.py directly to use its built-in SSE support and argument parsing
        mcp_script_path = os.path.join(ROOT_DIR, "mcp-server", "src", "mcp_server_rag_anything", "server.py")
        # We need to set PYTHONPATH explicitly to include the src dir so it can find its own modules
        mcp_env = os.environ.copy()
        mcp_env["PYTHONPATH"] = f"{ROOT_DIR}/rag-core:{ROOT_DIR}/mcp-server/src:{mcp_env.get('PYTHONPATH', '')}"
        
        mcp_cmd = f"{ENV_PYTHON} {mcp_script_path} --sse --port {PORTS['mcp']}"
        p_mcp = run_service("MCP Server", mcp_cmd, cwd=os.path.join(ROOT_DIR, "mcp-server"), env=mcp_env)
        processes.append(p_mcp)
        
        # 等待 MCP Server 准备好 (关键！Agent Service 需要连接 MCP 获取工具)
        print("   ⏳ Waiting for MCP Server to be ready...")
        mcp_ready = False
        for i in range(15):  # 最多等待 15 秒
            try:
                req = opener.open(f"http://127.0.0.1:{PORTS['mcp']}/sse", timeout=2)
                if req.status == 200:
                    print("   ✅ MCP Server is ready!")
                    mcp_ready = True
                    break
            except Exception:
                pass
            time.sleep(1)
        if not mcp_ready:
            print("   ⚠️ MCP Server may not be fully ready, Agent may lack RAG tools!")

        # 3. Start Agent Service (The Brain)
        # LangGraph logic that coordinates Chat and Tools
        print("\n[3/5] Starting Agent Service...")
        agent_cmd = f"{ENV_PYTHON} start_server.py"
        p_agent = run_service("Agent Service", agent_cmd, cwd=os.path.join(ROOT_DIR, "agent-service"))
        processes.append(p_agent)
        time.sleep(2)

        # 4. Start Chat UI (User Interface)
        # Next.js Frontend for users
        print("\n[4/5] Starting Chat UI...")
        chat_ui_cmd = "npm run dev"
        p_chat = run_service("Chat UI", chat_ui_cmd, cwd=os.path.join(ROOT_DIR, "chat-ui"))
        processes.append(p_chat)

        # 5. Start Admin UI (Management Interface)
        # Vite Frontend for admins
        print("\n[5/5] Starting Admin UI...")
        # 使用 npm 而不是 bun，因为 Bun 1.2.x 与 Vite WebSocket 存在兼容性问题
        # 错误: TypeError: undefined is not an object (evaluating 'http') at abortHandshake (ws:477:14)
        admin_ui_cmd = "npm run dev"
        
        # 关键修复：清除代理环境变量，防止 Vite http-proxy 通过系统代理连接本地服务
        # 这是导致 503/500 代理错误的根本原因
        admin_env = os.environ.copy()
        admin_env["HTTP_PROXY"] = ""
        admin_env["HTTPS_PROXY"] = ""
        admin_env["http_proxy"] = ""
        admin_env["https_proxy"] = ""
        
        p_admin = run_service("Admin UI", admin_ui_cmd, cwd=os.path.join(ROOT_DIR, "admin-ui"), env=admin_env)
        processes.append(p_admin)

        print("\n" + "="*60)
        print("✨ All systems operational! Service endpoints:")
        print(f"   - � User Chat:     http://localhost:{PORTS['chat_ui']}")
        print(f"   - ⚙️  Admin Panel:   http://localhost:{PORTS['admin_ui']}")
        print(f"   - 🧠 Agent API:     http://localhost:{PORTS['agent']}")
        print(f"   - 🔌 MCP Server:    http://localhost:{PORTS['mcp']}/sse")
        print(f"   - � RAG Core API:  http://localhost:{PORTS['rag_api']}/docs")
        print("="*60)
        print("Press Ctrl+C to stop all services.")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
    finally:
        for p in processes:
            kill_process_group(p)
        print("✅ Shutdown complete.")

if __name__ == "__main__":
    main()