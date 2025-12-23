"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from langchain.agents import create_agent
from rag.chat.llms import deepseek_model
from rag.chat.tools import get_mcp_rag_tools, get_available_collections
# fmt: off  MC8yOmFIVnBZMlhsa0xUb3Y2bzZaMFpZWlE9PTpjOTllNDZlYQ==

tools = [get_available_collections] + get_mcp_rag_tools()
agent = create_agent(model=deepseek_model(),
                     tools=tools,
                     system_prompt="根据用户的问题从合适的集合中查询相关知识。"
                                   "如果不确定当前使用的collection_name，可以使用 get_available_collections 工具获取所有可用的集合信息，"
                                   "然后根据集合的描述和用户的问题选择最合适的 collection_name。"
                     )