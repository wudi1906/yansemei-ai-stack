"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import asyncio
import os
# noqa  MC8yOmFIVnBZMlhsa0xUb3Y2bzZkVmxhTXc9PToyOTc3Y2QzNw==

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
            {
                "mcp-server-rag": {
                    "url": "http://127.0.0.1:8001/sse",
                    "transport": "sse",
                }
            }
        )
tools = asyncio.run(client.get_tools())
os.environ["DEEPSEEK_API_KEY"] = "sk-0828827353434c24b51dd30edcfa7f32"
model = init_chat_model("deepseek:deepseek-chat")
# noqa  MS8yOmFIVnBZMlhsa0xUb3Y2bzZkVmxhTXc9PToyOTc3Y2QzNw==

# 实现跨库查询（集合），集合名称及描述信息通过动态提示词函数获取（自行完成）
agent = create_agent(model=model, tools=tools,
                     system_prompt="根据用户的问题从合适的集合中查询相关知识。"
                                   "关于课程相关问题的集合名称：course_collection；关于智能体相关问题的集合名称：LangChainCollection"
                                   "需要调用的工具中需要 collection_name，则输入合适的集合名称，根据用户的问题无法判断集合名称时，请使用默认集合名称。"
                     )