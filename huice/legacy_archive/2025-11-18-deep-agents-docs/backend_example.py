import os

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langchain.agents.middleware import InterruptOnConfig
from langchain.chat_models import init_chat_model
from langgraph.store.memory import InMemoryStore

os.environ["DEEPSEEK_API_KEY"] = "sk-12fe20a839dc4a8f8f995c92cce35215"
model = init_chat_model("deepseek:deepseek-chat")

def make_backend(runtime):
    return CompositeBackend(
        default=StateBackend(runtime),  # Ephemeral storage
        routes={
            "/memories/": StoreBackend(runtime),  # Persistent storage
            "/temp/": StateBackend(runtime),
        }
    )

config = InterruptOnConfig(
            allowed_decisions=["approve", "edit", "reject"],
            description="写入文件"
        )
interrupt_on = {
    "write_file": config
}

# ✅ 直接创建 agent 实例，传入自定义的 store
agent = create_deep_agent(
    model=model,
    # store=InMemoryStore(),
    backend=make_backend,
    system_prompt="如果无法回答用户问题，可以尝试从/memories 目录下读取",
    interrupt_on=interrupt_on,
)
#
# config = {"configurable": {"thread_id": "session-1"}}
#
# result = agent.invoke({
#     "messages": [{
#         "role": "user",
#         "content": """
#             1. 在 /test.py 创建测试脚本（临时存储）
#             2. 在 /memories/user_prefs.json 保存用户偏好（持久存储）
#             3. 在 /cache/temp.txt 创建临时文件（临时存储）
#             """
#     }]
# }, config=config)