"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from langgraph.prebuilt import create_react_agent
# type: ignore  MC8yOmFIVnBZMlhsa0xUb3Y2bzZaemQwUkE9PTpiZGU0YmQ2Yg==

from rag.chat.llms import get_model
from rag.chat.tools import get_mcp_rag_tools, get_available_collections
# pragma: no cover  MS8yOmFIVnBZMlhsa0xUb3Y2bzZaemQwUkE9PTpiZGU0YmQ2Yg==

tools = [get_available_collections] + get_mcp_rag_tools()

agent = create_react_agent(model=get_model(),
                     tools=tools,
                     prompt="根据用户的问题从合适的集合中查询相关知识。"
                                   "如果不确定当前使用的collection_name，可以使用 get_available_collections 工具获取所有可用的集合信息，"
                                   "然后根据集合的描述和用户的问题选择最合适的 collection_name。"
                     )