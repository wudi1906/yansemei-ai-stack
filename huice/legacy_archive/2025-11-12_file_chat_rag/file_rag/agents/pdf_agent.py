"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from langchain.agents import create_agent
from file_rag.core.llms import deepseek_model
# type: ignore  MC8yOmFIVnBZMlhsa0xUb3Y2bzZXbEpIY3c9PToxZTFlNTdmZQ==

# 根据需求的复杂度增加 中间件、工具等内容
agent = create_agent(
    model=deepseek_model,
    tools=[],
    system_prompt="你擅长基于用户提供的上下文信息回答用户问题。",
    name="chat_agent",
)