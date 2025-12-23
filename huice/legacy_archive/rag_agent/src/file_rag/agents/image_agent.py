"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from langchain.agents import create_agent

from file_rag.core.llms import image_llm_model

def pre(state):
    print("图片 文件内容：",state)

agent = create_agent(
    model=image_llm_model,
    tools=[],
    system_prompt="你是AI智能助手，专门针对用户上传的图片，回答用户问题。请仔细分析图片内容并提供详细的回答。",
    name="image_chat_agent",
    # pre_model_hook=pre
)