"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import os
from langchain_openai import ChatOpenAI
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_ollama import ChatOllama
except ImportError:
    ChatOllama = None

# pylint: disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZWbVJYTVE9PTo4MjBkNzBkZA==

def get_model():
    """
    Factory function to get the LLM based on environment variables.
    Supported providers: 'siliconflow', 'deepseek', 'google', 'ollama'
    """
    provider = os.getenv("LLM_PROVIDER", "siliconflow").lower()
    
    if provider == "ollama":
        if not ChatOllama:
            raise ImportError("langchain-ollama is not installed. Please run `pip install langchain-ollama`.")
        
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model_name = os.getenv("OLLAMA_MODEL", "llama3")
        print(f"🚀 Using LLM: {model_name} (Ollama @ {base_url})")
        return ChatOllama(
            model=model_name,
            base_url=base_url,
            temperature=0
        )
    
    elif provider == "google":
        if not ChatGoogleGenerativeAI:
            raise ImportError("langchain-google-genai is not installed. Please run `pip install langchain-google-genai`.")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # 从环境变量读取模型名称，默认使用 gemini-2.5-flash
        model_name = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
        print(f"🚀 Using LLM: {model_name} (Google)")
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0,
            convert_system_message_to_human=True
        )
        
    elif provider == "deepseek":
        # DeepSeek 官方 API
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
        model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        print(f"🚀 Using LLM: {model_name} (DeepSeek)")
        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=0
        )
    
    elif provider in ("siliconflow", "sf"):
        # SiliconFlow - 统一 DeepSeek / Qwen 访问的首选
        api_key = os.getenv("SILICONFLOW_API_KEY")
        if not api_key:
            raise ValueError("SILICONFLOW_API_KEY not found in environment variables")
        model_name = os.getenv("SILICONFLOW_MODEL", "deepseek-ai/DeepSeek-V3")
        base_url = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.com/v1")
        print(f"🚀 Using LLM: {model_name} (SiliconFlow)")
        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=0,
        )
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

# For backward compatibility if needed, though we should update call sites
def deepseek_model():
    return get_model()