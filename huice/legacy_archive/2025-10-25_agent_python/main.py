"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from llms import get_default_model
from tools import get_weather, get_zhipu_search_mcp_tools
# from 父 import 儿子
model = get_default_model()

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)


web_agent = create_agent(
    model=model,
    tools=get_zhipu_search_mcp_tools(),
    system_prompt="You are a helpful assistant"
)