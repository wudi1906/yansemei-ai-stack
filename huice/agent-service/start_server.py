#!/usr/bin/env python3
"""
AuroraAI Agent Service - Full Version with SSE Support
Compatible with LangGraph Chat UI

Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import os
import sys
import json
import uuid
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Request, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


def setup_environment():
    """Setup required environment variables"""
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    config_path = Path(__file__).parent / "graph.json"
    graphs = {}
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            graphs = config.get("graphs", {})
    
    os.environ.update({
        "DATABASE_URI": ":memory:",
        "REDIS_URI": "fake",
        "MIGRATIONS_PATH": "__inmem",
        "ALLOW_PRIVATE_NETWORK": "true",
        "LANGGRAPH_API_URL": "http://localhost:2025",
        "LANGSERVE_GRAPHS": json.dumps(graphs) if graphs else "{}",
    })
    
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print("✅ Loaded environment from .env")
        except ImportError:
            pass


setup_environment()
from rag.chat.agent_rag_anything import agent

app = FastAPI(title="AuroraAI Agent Service")

# API Key 认证
API_KEY = os.getenv("API_KEY", "")
API_KEY_WHITELIST = ["/", "/ok", "/info", "/health", "/docs", "/openapi.json"]


async def verify_api_key(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    authorization: Optional[str] = Header(None),
):
    """验证 API Key"""
    # 如果没有配置 API_KEY，跳过验证
    if not API_KEY:
        return None
    
    # 白名单路径不需要验证
    if request.url.path in API_KEY_WHITELIST:
        return None
    
    # 从 Header 获取 API Key
    provided_key = x_api_key
    if not provided_key and authorization:
        # 支持 Bearer token 格式
        if authorization.startswith("Bearer "):
            provided_key = authorization[7:]
    
    if provided_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return provided_key
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str


@app.get("/")
def root():
    """Root endpoint"""
    return {"status": "ok", "service": "AuroraAI Agent Service"}


@app.get("/ok")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/info")
def info():
    """Service info endpoint for Chat UI health checks"""
    return {
        "status": "ok",
        "provider": os.getenv("LLM_PROVIDER", "siliconflow"),
        "graphs": json.loads(os.getenv("LANGSERVE_GRAPHS", "{}") or "{}"),
    }


@app.post("/chat", dependencies=[Depends(verify_api_key)])
def chat(req: ChatRequest):
    """Simple chat endpoint"""
    result = agent.invoke({"messages": [("user", req.query)]})
    return {"result": result}


@app.post("/threads", dependencies=[Depends(verify_api_key)])
def create_thread():
    """Create a new thread"""
    return {"thread_id": str(uuid.uuid4())}


def extract_user_message(data: dict) -> Optional[str]:
    """Extract user message from various request formats"""
    # Format 1: input.messages array (LangGraph Chat UI format)
    if "input" in data and isinstance(data["input"], dict):
        messages = data["input"].get("messages", [])
        for msg in messages:
            if isinstance(msg, dict):
                content = msg.get("content")
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    for part in content:
                        if isinstance(part, dict) and part.get("type") == "text":
                            return part.get("text")
    
    # Format 2: direct messages array
    if "messages" in data:
        for msg in data["messages"]:
            if isinstance(msg, dict):
                content = msg.get("content")
                if isinstance(content, str):
                    return content
    
    # Format 3: direct input string
    if "input" in data and isinstance(data["input"], str):
        return data["input"]
    
    # Format 4: query field
    if "query" in data:
        return data["query"]
    
    return None


def create_sse_event(event_type: str, data: dict) -> str:
    """Create SSE formatted event"""
    return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def generate_sse_response(thread_id: str, user_msg: str):
    """Generate SSE stream response for Chat UI"""
    try:
        # Send metadata event
        yield create_sse_event("metadata", {"run_id": str(uuid.uuid4())})
        
        # Invoke agent
        print(f"💬 Processing: {user_msg[:100]}")
        result = agent.invoke({"messages": [("user", user_msg)]})
        
        # Extract AI response
        ai_content = ""
        if "messages" in result:
            for msg in result["messages"]:
                if hasattr(msg, "type") and msg.type == "ai":
                    ai_content = msg.content
                    break
                elif isinstance(msg, dict) and msg.get("type") == "ai":
                    ai_content = msg.get("content", "")
                    break
        
        if not ai_content:
            ai_content = str(result)
        
        # Send values event with the response
        values_data = {
            "messages": [
                {"type": "human", "content": user_msg},
                {"type": "ai", "content": ai_content, "id": str(uuid.uuid4())}
            ]
        }
        yield create_sse_event("values", values_data)
        
        # Send end event
        yield create_sse_event("end", {})
        
        print(f"✅ Response sent: {ai_content[:100]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        yield create_sse_event("error", {"message": str(e)})


@app.post("/threads/{thread_id}/runs/stream", dependencies=[Depends(verify_api_key)])
async def run_thread_stream(thread_id: str, request: Request):
    """Handle stream requests from Chat UI with SSE"""
    body = await request.json()
    print(f"📥 Request: {json.dumps(body, ensure_ascii=False)[:300]}")
    
    user_msg = extract_user_message(body)
    if not user_msg:
        print(f"⚠️ No message found in: {body}")
        raise HTTPException(status_code=400, detail="No user message provided")
    
    return StreamingResponse(
        generate_sse_response(thread_id, user_msg),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@app.post("/threads/{thread_id}/messages", dependencies=[Depends(verify_api_key)])
async def post_thread_message(thread_id: str, request: Request):
    """Post message to thread"""
    body = await request.json()
    user_msg = extract_user_message(body)
    if not user_msg:
        return {"thread_id": thread_id, "messages": []}
    result = agent.invoke({"messages": [("user", user_msg)]})
    return {"thread_id": thread_id, "messages": [{"role": "assistant", "content": result}]}


@app.post("/threads/{thread_id}/history")
@app.get("/threads/{thread_id}/history")
def thread_history(thread_id: str):
    """Get thread history"""
    return []


@app.post("/threads/search")
@app.get("/threads/search")
def search_threads():
    """Search threads"""
    return []


def main():
    """Start the server"""
    print("🚀 Starting AuroraAI Agent Service (SSE Enabled)...")
    print("=" * 60)
    print("📍 Server URL: http://localhost:2025")
    print("📚 API Docs: http://localhost:2025/docs")
    print("=" * 60)
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2025, reload=False, access_log=True)


if __name__ == "__main__":
    main()
