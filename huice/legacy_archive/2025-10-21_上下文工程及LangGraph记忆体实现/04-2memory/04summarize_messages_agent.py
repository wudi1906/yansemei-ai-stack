import asyncio
import os

from langchain.chat_models import init_chat_model
from langmem.short_term import SummarizationNode, RunningSummary
from langchain_core.messages.utils import count_tokens_approximately
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import InMemorySaver
from typing import Any

os.environ["DEEPSEEK_API_KEY"] = "sk-b68ccb70b0934c4c80cb58a95f9cee00"
model = init_chat_model("deepseek:deepseek-chat")

""""
参数含义
max_tokens

含义：这是最终输出中返回的最大标记数量。也就是说，经过所有处理（包括总结）后，最终返回的消息列表中，所有消息的标记总数不能超过这个值。
作用：它主要用于限制最终输出的大小，确保输出不会过于庞大，适合输入到后续的模型中。
max_tokens_before_summary

含义：这是在触发总结之前累积的最大标记数量。也就是说，当处理消息时，一旦累积的消息标记数量达到这个值，就会触发总结操作。
作用：它用于控制何时进行总结，避免一次性处理过多的消息，从而确保总结的效率和质量。
max_summary_tokens

含义：这是为总结预算的最大标记数量。也就是说，生成的总结消息本身的最大标记数量不能超过这个值。
作用：它用于控制总结的长度，确保总结不会过于冗长，同时也能保证总结的简洁性和信息密度。
参数之间的关系
假设我们有以下参数设置：

max_tokens=256
max_tokens_before_summary=256
max_summary_tokens=128
处理流程
消息累积：

从最旧到最新的顺序处理消息。
每处理一条消息，就将该消息的标记数量累加到一个计数器中。
一旦这个计数器的值达到max_tokens_before_summary（这里是256），就会触发总结操作。
总结操作：

对累积的这些消息进行总结，生成一个新的总结消息。
生成的总结消息的标记数量不能超过max_summary_tokens（这里是128）。
这个总结消息会替换掉累积的这些消息，从而减少消息的总数。
最终输出：

经过总结后，所有剩余的消息（包括新的总结消息）的标记总数不能超过max_tokens（这里是256）。
如果在总结后，剩余的消息标记总数仍然超过max_tokens，那么会进一步裁剪或调整，以确保最终输出的标记总数不超过max_tokens。
具体例子
假设我们有以下消息列表，每条消息的标记数量如下：

消息1：50标记
消息2：60标记
消息3：70标记
消息4：80标记
累积过程：

处理消息1，累积标记数：50
处理消息2，累积标记数：50 + 60 = 110
处理消息3，累积标记数：110 + 70 = 180
处理消息4，累积标记数：180 + 80 = 260
在处理消息4时，累积标记数达到了260，超过了max_tokens_before_summary（256），因此触发总结操作。

总结操作：

对消息1、消息2、消息3和消息4进行总结，生成一个新的总结消息。
假设总结消息的标记数量为120（不超过max_summary_tokens的128）。
这个总结消息会替换掉消息1、消息2、消息3和消息4。
最终输出：

剩余的消息列表现在只包含这个总结消息，标记数量为120。
由于120小于max_tokens（256），所以这个总结消息就是最终输出。
总结
max_tokens：控制最终输出的大小，确保输出不会超过这个限制。
max_tokens_before_summary：控制何时触发总结，避免一次性处理过多消息。
max_summary_tokens：控制总结消息的长度，确保总结不会过于冗长。
这三个参数共同作用，确保在处理大量消息时，既能有效地进行总结，又能保证最终输出的大小在可控范围内。

"""
summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=model,
    max_tokens=384,
    max_summary_tokens=128,
    output_messages_key="llm_input_messages",
)

class State(AgentState):
    # NOTE: we're adding this key to keep track of previous summary information
    # to make sure we're not summarizing on every LLM call
    context: dict[str, RunningSummary]


checkpointer = InMemorySaver()

agent = create_react_agent(
    model=model,
    tools=[],
    pre_model_hook=summarization_node,
    state_schema=State,
    checkpointer=checkpointer,
)


config = {"configurable": {"thread_id": "1"}}
async def main():
    # Stream the agent
    async for chunk in agent.astream(
            {"messages": [{"role": "user", "content": "写一首关于冬天的文言文"}]},
            stream_mode="values",
            config=config
    ):
        if "messages" in chunk:
            chunk["messages"][-1].pretty_print()
    async for chunk in agent.astream(
            {"messages": [{"role": "user", "content": "再一首夏天的"}]},
            stream_mode="values",
            config=config
    ):
        if "messages" in chunk:
            chunk["messages"][-1].pretty_print()
if __name__ == "__main__":
    asyncio.run(main())