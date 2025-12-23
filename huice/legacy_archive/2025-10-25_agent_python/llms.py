"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import os
# from langchain.chat_models import init_chat_model
from langchain_deepseek.chat_models import ChatDeepSeek
os.environ["DEEPSEEK_API_KEY"] = "sk-a9b7f2341c6844a3896fd3e606620c17"

def get_default_model():
    return ChatDeepSeek(model="deepseek-chat")

# llm = get_default_model()
# response = llm.invoke("你好")
# print(response)
# for text in llm.stream("你好"):
#     print(text.content, end="", flush=True)