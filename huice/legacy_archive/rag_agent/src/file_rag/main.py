"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import asyncio

from file_rag.engines.file_chat_engine import FileChatEngineFactory
engine = asyncio.run(FileChatEngineFactory.create_engine())

graph = engine.graph
# engine = asyncio.run(FileChatEngineFactory.get_engine())
# graph = engine.graph

# pip install -U langgraph "langchain[openai]" langchain-community langchain-text-splitters
# pip install -U langmem
# pip install -U langchain-deepseek
# pip install -qU langchain-pymupdf4llm
# pip install langchain_ollama
# pip install -U "langgraph-cli[inmem]"