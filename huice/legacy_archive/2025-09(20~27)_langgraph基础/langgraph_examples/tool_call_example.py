from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langchain_tavily import TavilySearch
import os
from typing import Annotated, Union

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
import json

from langchain_core.messages import ToolMessage

os.environ["DEEPSEEK_API_KEY"] = "sk-20d48ecc2ac84432963afc08a0e34b8b"
llm = ChatDeepSeek(model="deepseek-chat")
class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

graph_builder = StateGraph(State)

# Modification: tell the LLM which tools it can call
llm_with_tools = llm.bind_tools([get_weather])


# 通过大模型推理确定需要执行 的后续操作（确定调用哪个工具、参数等信息，也可能不需要调用工具）
def chatbot(state: State):
    output = {"messages": [llm_with_tools.invoke(state["messages"])]}
    return output


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}




def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

graph_builder.add_node("chatbot", chatbot)

tool_node = BasicToolNode(tools=[get_weather])
graph_builder.add_node("tools", tool_node)


graph_builder.add_edge(START, "chatbot")

# 判断 chatbot输出的内容中是否包含工具调用，如果有则调用工具，如果没有工具调用，则直接结束
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # 以下字典允许您将条件输出指定为特定节点
    # 默认情况下使用恒等函数，但若您希望使用
    # 除"tools"之外的其他节点名称，
    # 可将字典值更新为其他名称
    # 例如："tools": "my_tools"
    # {"tools": "tools", END: END},
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

if __name__ == "__main__":
    stream_graph_updates("北京的天气如何")