import os

from anthropic import AsyncAnthropic
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from langchain_core.runnables import RunnableConfig
from langgraph.func import entrypoint
from langgraph.store.memory import InMemoryStore
from langmem import create_memory_manager
from pydantic import BaseModel, Field
from langmem import create_memory_store_manager

os.environ["DEEPSEEK_API_KEY"] = "sk-95a7b5cd98e34ba2ab07f00ca757b051"
os.environ["OLLAMA_HOST"] = "http://155.138.220.75:11434"
model = init_chat_model("deepseek:deepseek-chat")
embeddings = init_embeddings("ollama:qwen3-embedding:0.6b", base_url=os.environ["OLLAMA_HOST"])
store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1024,
    }
)


class Episode(BaseModel):
    """用智能体自己的话，把这次经历写下来。事后回想，把当时脑子里最重要的想法记下来，让它以后能学着长记性。"""
    observation: str = Field(..., description="The context and setup - what happened")
    thoughts: str = Field(
        ...,
        description="内部推理过程与智能体在本轮中的观察，使其得以得出正确的行动与结果。“我……”",
    )
    action: str = Field(
        ...,
        description="做了什么、如何做的、以何种格式呈现。（包含对行动成功至关重要的任何要素）。我……",
    )
    result: str = Field(
        ...,
        description="结果与回顾。哪些地方做得好？下次可以在哪些方面改进？我……",
    )
manager = create_memory_store_manager(
    model,
    namespace=("memories", "episodes"),
    schemas=[Episode],
    instructions="提取成功解释的示例，捕捉完整的推理链条。解释要简洁，推理逻辑要精确。",
    enable_inserts=True,
    store=store
)


# 构造对话数据
conversation = [
    {
        "role": "user",
        "content": "什么是二叉树？我从事家谱工作，如果这有帮助的话",
    },
    {
        "role": "assistant",
        "content": "二叉树就像家谱一样，但每个父节点最多有2个子节点。这里有个简单示例：\n   鲍勃\n  /  \\\n艾米  卡尔\n\n就像在家谱中一样，我们称鲍勃为'父节点'，艾米和卡尔为'子节点'。",
    },
    {
        "role": "user",
        "content": "哦，有道理！那么在二叉搜索树中，是不是就像按年龄来组织家庭成员？",
    },
]

print("开始更新记忆")
episodes = manager.invoke({"messages": conversation})
print(episodes)
print("记忆更新成功")

@entrypoint(store=store)
def app(messages: list):
    # Step 1: Find similar past episodes
    # memories = manager.search(
    #     query=messages[-1]["content"],
    #     limit=1,
    # )
    similar = store.search(
        ("memories", "episodes"),
        query=messages[-1]["content"],
        limit=1,
    )
    print("similar::", similar)
    # Step 2: Build system message with relevant experience
    system_message = "You are a helpful assistant."
    if similar:
        system_message += "\n\n### EPISODIC MEMORY:"
        for i, item in enumerate(similar, start=1):
            episode = item.value["content"]
            system_message += f"""

Episode {i}:
When: {episode['observation']}
Thought: {episode['thoughts']}
Did: {episode['action']}
Result: {episode['result']}
        """

    # Step 3: Generate response using past experience
    response = model.invoke([{"role": "system", "content": system_message}, *messages])

    # Step 4: Store this interaction if successful
    manager.invoke({"messages": messages})
    return response


result = app.invoke(
    [
        {
            "role": "user",
            "content": "什么是二叉树？通俗易懂的给我解释一下",
        },
    ],
)
print(result)
print(store.search(("memories", "episodes"), query="Trees"))