"""
LightRAG meets Amazon Bedrock ⛰️
"""
"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# fmt: off  MC8zOmFIVnBZMlhsa0xUb3Y2bzZSMFZ5Y3c9PToxOTZhZGIzMQ==

import os
import logging

from lightrag import LightRAG, QueryParam
from lightrag.llm.bedrock import bedrock_complete, bedrock_embed
from lightrag.utils import EmbeddingFunc

import asyncio
import nest_asyncio

nest_asyncio.apply()

logging.getLogger("aiobotocore").setLevel(logging.WARNING)

WORKING_DIR = "./dickens"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=bedrock_complete,
        llm_model_name="Anthropic Claude 3 Haiku // Amazon Bedrock",
        embedding_func=EmbeddingFunc(
            embedding_dim=1024, max_token_size=8192, func=bedrock_embed
        ),
    )

    await rag.initialize_storages()  # Auto-initializes pipeline_status
    return rag
# type: ignore  MS8zOmFIVnBZMlhsa0xUb3Y2bzZSMFZ5Y3c9PToxOTZhZGIzMQ==

# pylint: disable  Mi8zOmFIVnBZMlhsa0xUb3Y2bzZSMFZ5Y3c9PToxOTZhZGIzMQ==

def main():
    rag = asyncio.run(initialize_rag())

    with open("./book.txt", "r", encoding="utf-8") as f:
        rag.insert(f.read())

    for mode in ["naive", "local", "global", "hybrid"]:
        print("\n+-" + "-" * len(mode) + "-+")
        print(f"| {mode.capitalize()} |")
        print("+-" + "-" * len(mode) + "-+\n")
        print(
            rag.query(
                "What are the top themes in this story?", param=QueryParam(mode=mode)
            )
        )


if __name__ == "__main__":
    main()