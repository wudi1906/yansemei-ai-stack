"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import os
from langchain_deepseek import ChatDeepSeek
os.environ["DEEPSEEK_API_KEY"] = "sk-305a73c02df94c13b2fb61006dd73718"

def get_default_model():
    return ChatDeepSeek(model="deepseek-chat", max_tokens=8192, temperature=0.2)