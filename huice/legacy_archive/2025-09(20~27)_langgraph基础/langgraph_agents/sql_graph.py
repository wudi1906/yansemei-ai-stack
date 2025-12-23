import asyncio
from typing import Literal
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import END, START, MessagesState, StateGraph
from langchain.agents.tool_node import ToolNode

import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from langgraph.checkpoint.memory import MemorySaver
os.environ["DEEPSEEK_API_KEY"] = "sk-20d48ecc2ac84432963afc08a0e34b8b"
llm = init_chat_model("deepseek:deepseek-chat")


db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# print(f"Dialect: {db.dialect}")
# print(f"Available tables: {db.get_usable_table_names()}")
# print(f'Sample output: {db.run("SELECT * FROM Artist LIMIT 5;")}')

from langchain_community.agent_toolkits import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")
# 获取表结构节点
get_schema_node = ToolNode([get_schema_tool], name="get_schema_node")

run_query_tool = next(tool for tool in tools if tool.name == "sql_db_query")
# 执行查询sql节点
run_query_node = ToolNode([run_query_tool], name="run_query_node")

client = MultiServerMCPClient(
    {
        "mcp-server-chart": {
            "command": "npx",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["-y", "@antv/mcp-server-chart"],
            "transport": "stdio",
        }
    }
)
chart_tools = asyncio.run(client.get_tools())


def generate_chart(state: MessagesState):
    agent = create_agent(llm, tools=chart_tools, prompt="根据数据的特点生成合适的图表")
    response = asyncio.run(agent.ainvoke({"messages":state["messages"]}, print_mode="updates"))
    return response


# 获取数据库所有的表名信息
def list_tables(state: MessagesState):
    tool_call = {
        "name": "sql_db_list_tables",
        "args": {},
        "id": "abc123",
        "type": "tool_call",
    }
    # 需要调用的工具说明
    tool_call_message = AIMessage(content="", tool_calls=[tool_call])

    list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")
    tool_message = list_tables_tool.invoke(tool_call)
    # 调用工具的结果
    response = AIMessage(f"Available tables: {tool_message.content}")

    return {"messages": [tool_call_message, tool_message, response]}

# 获取与问题相关的表结构
def get_relative_schema(state: MessagesState):
    llm_with_tools = llm.bind_tools([get_schema_tool], tool_choice="any")

    # llm_with_tools 可能会根据上下文信息生成工具调用信息，也可能直接返回结果
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


def generate_query(state: MessagesState):
    generate_query_system_prompt = """
    您是一个专用于与SQL数据库交互的智能体。
    根据输入的问题，请生成语法正确的 {dialect} 查询语句，
    随后查看查询结果并返回答案。除非用户明确指定要获取的示例数量，
    否则请始终将查询结果限制在最多 {top_k} 条。

    您可以通过相关列对结果进行排序，以返回数据库中最有价值的示例。
    切勿查询特定表的所有列，仅获取问题相关的必要列。

    禁止对数据库执行任何数据操作语言语句（INSERT、UPDATE、DELETE、DROP等）。
    """.format(
        dialect=db.dialect,
        top_k=10,
    )
    system_message = {
        "role": "system",
        "content": generate_query_system_prompt,
    }
    # We do not force a tool call here, to allow the model to
    # respond naturally when it obtains the solution.
    llm_with_tools = llm.bind_tools([run_query_tool])
    response = llm_with_tools.invoke([system_message] + state["messages"])
    return {"messages": [response]}


def check_query(state: MessagesState):
    check_query_system_prompt = """
    您是一位注重细节的SQL专家。  
    请仔细检查 {dialect} 查询中的常见错误，包括：  
    - 在NOT IN子句中使用NULL值  
    - 应当使用UNION ALL时却使用了UNION  
    - 使用BETWEEN处理不包含边界的情况  
    - 谓词中的数据类型不匹配  
    - 正确引用标识符  
    - 为函数使用正确数量的参数  
    - 转换为正确的数据类型  
    - 使用合适的列进行连接  

    如果存在上述任何错误，请重写查询。如果没有错误，请直接返回原始查询。  

    完成检查后，您将调用相应的工具来执行查询。
    """.format(dialect=db.dialect)

    system_message = {
        "role": "system",
        "content": check_query_system_prompt,
    }

    # Generate an artificial user message to check
    tool_call = state["messages"][-1].tool_calls[0]
    user_message = {"role": "user", "content": tool_call["args"]["query"]}
    llm_with_tools = llm.bind_tools([run_query_tool], tool_choice="any")
    response = llm_with_tools.invoke([system_message, user_message])
    response.id = state["messages"][-1].id

    return {"messages": [response]}

def should_continue(state: MessagesState) -> Literal[END, "check_query"]:
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return END
    else:
        return "check_query"

builder = StateGraph(MessagesState)
builder.add_node(list_tables)
builder.add_node(get_relative_schema)
builder.add_node(get_schema_node, "get_schema_node")
builder.add_node(generate_query)
builder.add_node(check_query)
builder.add_node(run_query_node, "run_query_node")
builder.add_node(generate_chart)

builder.add_edge(START, "list_tables")
builder.add_edge("list_tables", "get_relative_schema")
builder.add_edge("get_relative_schema", "get_schema_node")
builder.add_edge("get_schema_node", "generate_query")
builder.add_edge("generate_query", "check_query")

# 作业
# 条件边，加入接收用户反馈的中断

# builder.add_conditional_edges(
#     "generate_query",
#     should_continue,
# )
builder.add_edge("check_query", "run_query_node")
builder.add_edge("run_query_node", "generate_chart")

builder.add_edge("generate_chart", END)
# builder.add_edge("generate_chart", END)


checkpointer = MemorySaver()
graph = builder.compile()

if __name__ == "__main__":
    question = "哪种音乐类型的曲目平均时长最长？"

    for step in graph.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()