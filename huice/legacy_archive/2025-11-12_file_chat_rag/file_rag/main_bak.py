"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# # 在该模块中梳理思路及突破技术难点
# from typing import Any
# import base64
# import tempfile
# import os
#
# from langchain.agents import create_agent, AgentState
# from langchain.agents
# from langgraph.runtime import Runtime
# from langchain_core.messages import HumanMessage
# from langchain_community.document_loaders.parsers import LLMImageBlobParser
#
# from file_rag.core.llms import get_default_model
# from file_rag.core.llms import get_doubao_seed_model
#
# # 尝试导入 PyMuPDF4LLM
# try:
#     from langchain_pymupdf4llm import PyMuPDF4LLMLoader
# except ImportError:
#     PyMuPDF4LLMLoader = None
#     print("警告: langchain-pymupdf4llm 未安装，请运行: pip install -qU langchain-pymupdf4llm")
#
# @before_model
# def log_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
#     """
#     在模型调用前处理消息，特别是处理PDF文件
#
#     处理流程：
#     1. 检测消息中是否包含PDF文件（base64格式）
#     2. 将base64数据解码为PDF文件
#     3. 使用PyMuPDF4LLM提取文本内容
#     4. 使用多模态模型（doubao-seed）提取图片内容
#     5. 将提取的内容替换原始PDF数据
#     """
#     print("哈哈：AuroraAI欢迎您")
#     print("原始消息:", state["messages"])
#
#     # 获取消息列表
#     messages = state.get("messages", [])
#     if not messages:
#         return None
#
#     # 处理每条消息
#     modified = False
#     new_messages = []
#
#     for message in messages:
#         # 只处理 HumanMessage
#         if not isinstance(message, HumanMessage):
#             new_messages.append(message)
#             continue
#
#         # 检查消息内容是否为列表格式（包含文件）
#         content = message.content
#         if not isinstance(content, list):
#             new_messages.append(message)
#             continue
#
#         # 处理内容中的每个部分
#         new_content = []
#         for item in content:
#             if not isinstance(item, dict):
#                 new_content.append(item)
#                 continue
#
#             # 检查是否为PDF文件
#             if item.get('type') == 'file' and item.get('mime_type') == 'application/pdf':
#                 try:
#                     # 提取PDF信息
#                     base64_data = item.get('data', '')
#                     filename = item.get('metadata', {}).get('filename', 'unknown.pdf')
#
#                     print(f"\n检测到PDF文件: {filename}")
#
#                     # 解码base64数据
#                     pdf_bytes = base64.b64decode(base64_data)
#                     print(f"PDF文件大小: {len(pdf_bytes)} 字节")
#
#                     # 处理PDF文件
#                     extracted_text = process_pdf_with_multimodal(pdf_bytes, filename)
#
#                     if extracted_text:
#                         # 将提取的文本作为新的文本内容添加
#                         new_content.append({
#                             'type': 'text',
#                             'text': f"\n\n📄 PDF文件 '{filename}' 的内容:\n\n{extracted_text}"
#                         })
#                         modified = True
#                         print(f"PDF处理成功，提取内容长度: {len(extracted_text)} 字符")
#                     else:
#                         # 如果提取失败，保留原始文本提示
#                         new_content.append({
#                             'type': 'text',
#                             'text': f"\n\n📄 PDF文件 '{filename}' 处理失败或内容为空"
#                         })
#                         modified = True
#
#                 except Exception as e:
#                     print(f"处理PDF文件时出错: {e}")
#                     import traceback
#                     traceback.print_exc()
#                     # 出错时添加错误提示
#                     new_content.append({
#                         'type': 'text',
#                         'text': f"\n\n📄 PDF文件处理出错: {str(e)}"
#                     })
#                     modified = True
#             else:
#                 # 非PDF内容，保持原样
#                 new_content.append(item)
#
#         # 创建新消息
#         if new_content:
#             new_message = HumanMessage(
#                 content=new_content,
#                 additional_kwargs=message.additional_kwargs,
#                 response_metadata=message.response_metadata,
#                 id=message.id
#             )
#             new_messages.append(new_message)
#         else:
#             new_messages.append(message)
#
#     # 如果有修改，更新state
#     if modified:
#         print("\n处理后的消息:", new_messages)
#         return {"messages": new_messages}
#
#     return None
#
#
# def process_pdf_with_multimodal(pdf_bytes: bytes, filename: str) -> str:
#     """
#     使用PyMuPDF4LLM和多模态模型处理PDF文件
#
#     Args:
#         pdf_bytes: PDF文件的字节数据
#         filename: PDF文件名
#
#     Returns:
#         提取的文本内容（包含文本和图片描述）
#     """
#     if PyMuPDF4LLMLoader is None:
#         return "错误: PyMuPDF4LLM未安装，无法处理PDF文件"
#
#     # 创建临时文件
#     temp_file = None
#     temp_file_path = None
#
#     try:
#         # 创建临时文件保存PDF
#         temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
#         temp_file.write(pdf_bytes)
#         temp_file.flush()
#         os.fsync(temp_file.fileno())
#         temp_file_path = temp_file.name
#         temp_file.close()
#
#         print(f"临时文件已创建: {temp_file_path}")
#
#         # 创建多模态图片解析器
#         image_parser = LLMImageBlobParser(
#             model=get_doubao_seed_model()
#         )
#
#         # 使用PyMuPDF4LLM加载PDF，启用图片提取和多模态解析
#         loader = PyMuPDF4LLMLoader(
#             temp_file_path,
#             mode="single",  # 作为单个文档处理
#             extract_images=True,  # 提取图片
#             images_parser=image_parser,  # 使用多模态模型解析图片
#             table_strategy="lines"  # 提取表格
#         )
#
#         print("开始解析PDF...")
#         documents = loader.load()
#
#         if documents and len(documents) > 0:
#             text_content = documents[0].page_content
#             print(f"PDF解析成功，内容长度: {len(text_content)} 字符")
#             return text_content
#         else:
#             return "PDF文件解析后内容为空"
#
#     except Exception as e:
#         print(f"PDF处理失败: {e}")
#         import traceback
#         traceback.print_exc()
#         return f"PDF处理出错: {str(e)}"
#
#     finally:
#         # 清理临时文件
#         if temp_file_path and os.path.exists(temp_file_path):
#             try:
#                 os.unlink(temp_file_path)
#                 print(f"临时文件已删除: {temp_file_path}")
#             except Exception as e:
#                 print(f"删除临时文件失败: {e}")
#
# image_agent = create_agent(
#     model=get_doubao_seed_model(),
#     middleware=[log_before_model],
#     tools=[],
# )
#
# agent = create_agent(
#     model=get_default_model(),
#     middleware=[log_before_model],
#     tools=[],
# )
#
# # 使用示例（已注释）:
# # pip install -qU langchain-pymupdf4llm
# #
# # 测试PDF处理:
# # test_message = HumanMessage(content=[
# #     {'type': 'text', 'text': '总结一下'},
# #     {'type': 'file', 'source_type': 'base64', 'mime_type': 'application/pdf',
# #      'data': 'base64_encoded_pdf_data_here...',
# #      'metadata': {'filename': 'test.pdf'}}
# # ])
# # result = agent.invoke({"messages": [test_message]})