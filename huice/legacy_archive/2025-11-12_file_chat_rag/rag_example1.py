"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from langchain_pymupdf4llm import PyMuPDF4LLMLoader
# fmt: off  MC8yOmFIVnBZMlhsa0xUb3Y2bzZRM2hVUVE9PTo1ZGY5MTUwNA==

loader = PyMuPDF4LLMLoader(
    "../llm_course.pdf",
                mode="single",  # 作为单个文档处理
                table_strategy="lines"  # 提取表格
            )
documents = loader.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter
# pylint: disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZRM2hVUVE9PTo1ZGY5MTUwNA==

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_text(documents[0].page_content)
print(len(texts))