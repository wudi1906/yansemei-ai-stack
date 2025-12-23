"""
RAG Anything 框架的 MCP 服务器

本模块为 RAG Anything 框架提供模型上下文协议（MCP）服务器实现，
通过 MCP 工具和资源暴露其多模态文档处理和查询功能。
"""
"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""


import argparse
import os
import json
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Optional, List, Dict
from dotenv import load_dotenv
from pathlib import Path

from fastmcp import FastMCP, Context
from raganything import RAGAnything, RAGAnythingConfig
from lightrag import LightRAG
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.llm.ollama import ollama_embed
from lightrag.utils import EmbeddingFunc, logger


class RAGAnythingConnector:
    """
    RAG Anything 框架的连接器类

    管理 RAGAnything 实例的生命周期，并为 MCP 工具提供清晰的接口
    以便与框架进行交互。
    """

    def __init__(
        self,
        working_dir: str,
        llm_api_key: Optional[str] = None,
        llm_base_url: Optional[str] = None,
        llm_model: str = "deepseek-chat",
        vision_api_key: Optional[str] = None,
        vision_base_url: Optional[str] = None,
        vision_model: Optional[str] = None,
        embedding_host: Optional[str] = None,
        embedding_model: str = "qwen3-embedding:0.6b",
        embedding_dim: int = 1024,
        use_ollama_embedding: bool = True,
        parser: str = "docling",
        parse_method: str = "auto",
        enable_image_processing: bool = True,
        enable_table_processing: bool = True,
        enable_equation_processing: bool = True,
        load_existing: bool = True,
    ):
        """
        初始化 RAG Anything 连接器

        参数:
            working_dir: RAG 存储目录
            llm_api_key: LLM 的 API 密钥
            llm_base_url: LLM API 的基础 URL
            llm_model: LLM 模型名称（默认: deepseek-chat）
            vision_api_key: 视觉模型的 API 密钥
            vision_base_url: 视觉 API 的基础 URL
            vision_model: 视觉模型名称
            embedding_host: Ollama 嵌入服务器地址（默认: http://35.235.113.151:11434）
            embedding_model: 嵌入模型名称（默认: qwen3-embedding:0.6b）
            embedding_dim: 嵌入维度（默认: 1024）
            use_ollama_embedding: 是否使用 Ollama 嵌入（默认: True）
            parser: 使用的解析器 (mineru 或 docling)（默认: docling）
            parse_method: 解析方法 (auto, ocr, txt)（默认: auto）
            enable_image_processing: 启用图像处理
            enable_table_processing: 启用表格处理
            enable_equation_processing: 启用公式处理
            load_existing: 是否加载已存在的知识库（默认: True）
        """
        self.working_dir = working_dir
        self.llm_api_key = llm_api_key
        self.llm_base_url = llm_base_url
        self.llm_model = llm_model
        self.vision_api_key = vision_api_key or llm_api_key
        self.vision_base_url = vision_base_url or llm_base_url
        self.vision_model = vision_model
        self.embedding_host = embedding_host or "http://35.235.113.151:11434"
        self.embedding_model = embedding_model
        self.embedding_dim = embedding_dim
        self.use_ollama_embedding = use_ollama_embedding
        self.load_existing = load_existing

        # 创建配置
        self.config = RAGAnythingConfig(
            working_dir=working_dir,
            parser=parser,
            parse_method=parse_method,
            enable_image_processing=enable_image_processing,
            enable_table_processing=enable_table_processing,
            enable_equation_processing=enable_equation_processing,
            display_content_stats=True,
        )

        # 创建模型函数
        self.llm_model_func = self._create_llm_func()
        self.vision_model_func = self._create_vision_func() if vision_model else None
        self.embedding_func = self._create_embedding_func()

        # RAGAnything 实例（延迟初始化）
        self.rag: Optional[RAGAnything] = None
        self.lightrag_instance: Optional[LightRAG] = None
        self._initialized = False

    async def initialize(self):
        """
        初始化 RAGAnything 实例

        如果 load_existing=True 且存在已有知识库，则加载已有的 LightRAG 实例；
        否则创建新的 RAGAnything 实例。
        """
        if self._initialized:
            logger.info("RAGAnything 已经初始化，跳过")
            return

        # 检查是否存在已有的知识库
        if self.load_existing and os.path.exists(self.working_dir) and os.listdir(self.working_dir):
            logger.info(f"✅ 发现已存在的知识库: {self.working_dir}")
            logger.info("正在加载已有知识库...")

            # 创建 LightRAG 实例并加载已有数据
            self.lightrag_instance = LightRAG(
                working_dir=self.working_dir,
                llm_model_func=self.llm_model_func,
                embedding_func=self.embedding_func,
            )

            # 初始化存储（加载已有数据）
            await self.lightrag_instance.initialize_storages()
            await initialize_pipeline_status()
            logger.info("✅ 已有知识库加载完成")

            # 使用已有的 LightRAG 实例创建 RAGAnything
            self.rag = RAGAnything(
                lightrag=self.lightrag_instance,
                vision_model_func=self.vision_model_func,
            )
            logger.info("✅ RAGAnything 已使用现有知识库初始化")
        else:
            # 创建新的 RAGAnything 实例
            if not os.path.exists(self.working_dir):
                logger.info(f"创建新的工作目录: {self.working_dir}")
                os.makedirs(self.working_dir, exist_ok=True)

            logger.info("正在创建新的 RAGAnything 实例...")
            self.rag = RAGAnything(
                config=self.config,
                llm_model_func=self.llm_model_func,
                vision_model_func=self.vision_model_func,
                embedding_func=self.embedding_func,
            )
            logger.info("✅ RAGAnything 新实例创建完成")

        self._initialized = True
# noqa  MC80OmFIVnBZMlhsa0xUb3Y2bzZNalJxY1E9PTo0Nzk0MDQyYQ==

    def _create_llm_func(self):
        """创建 LLM 模型函数"""
        def llm_func(prompt, system_prompt=None, history_messages=[], **kwargs):
            return openai_complete_if_cache(
                self.llm_model,
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                api_key=self.llm_api_key,
                base_url=self.llm_base_url,
                **kwargs,
            )
        return llm_func

    def _create_vision_func(self):
        """创建视觉模型函数"""
        def vision_func(
            prompt,
            system_prompt=None,
            history_messages=[],
            image_data=None,
            messages=None,
            **kwargs
        ):
            # 处理消息格式（用于 VLM 增强查询）
            if messages:
                return openai_complete_if_cache(
                    self.vision_model,
                    "",
                    system_prompt=None,
                    history_messages=[],
                    messages=messages,
                    api_key=self.vision_api_key,
                    base_url=self.vision_base_url,
                    **kwargs,
                )
            # 处理单图像格式
            elif image_data:
                return openai_complete_if_cache(
                    self.vision_model,
                    "",
                    system_prompt=None,
                    history_messages=[],
                    messages=[
                        {"role": "system", "content": system_prompt} if system_prompt else None,
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                                },
                            ],
                        } if image_data else {"role": "user", "content": prompt},
                    ],
                    api_key=self.vision_api_key,
                    base_url=self.vision_base_url,
                    **kwargs,
                )
            # 回退到纯文本
            else:
                return self.llm_model_func(prompt, system_prompt, history_messages, **kwargs)

        return vision_func

    def _create_embedding_func(self):
        """创建嵌入函数"""
        if self.use_ollama_embedding:
            # 使用 Ollama 嵌入
            return EmbeddingFunc(
                embedding_dim=self.embedding_dim,
                max_token_size=32000,
                func=lambda texts: ollama_embed(
                    texts,
                    embed_model=self.embedding_model,
                    api_key="",
                    host=self.embedding_host,
                ),
            )
        else:
            # 使用 OpenAI 兼容的嵌入
            return EmbeddingFunc(
                embedding_dim=self.embedding_dim,
                max_token_size=8192,
                func=lambda texts: openai_embed(
                    texts,
                    model=self.embedding_model,
                    api_key=self.llm_api_key,
                    base_url=self.llm_base_url,
                ),
            )

    async def process_document(
        self,
        file_path: str,
        output_dir: Optional[str] = None,
        parse_method: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        处理单个文档

        参数:
            file_path: 文档路径
            output_dir: 解析内容的输出目录
            parse_method: 使用的解析方法
            **kwargs: 额外参数

        返回:
            处理结果字典
        """
        try:
            await self.rag.process_document_complete(
                file_path=file_path,
                output_dir=output_dir,
                parse_method=parse_method,
                **kwargs
            )
            return {
                "success": True,
                "file_path": file_path,
                "message": f"成功处理文档: {file_path}"
            }
        except Exception as e:
            raise ValueError(f"处理文档失败: {str(e)}")

    async def process_folder(
        self,
        folder_path: str,
        output_dir: Optional[str] = None,
        parse_method: Optional[str] = None,
        recursive: bool = True,
        max_workers: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        处理文件夹中的所有文档

        参数:
            folder_path: 文件夹路径
            output_dir: 解析内容的输出目录
            parse_method: 使用的解析方法
            recursive: 递归处理子文件夹
            max_workers: 最大并发工作线程数
            **kwargs: 额外参数

        返回:
            处理结果字典
        """
        try:
            await self.rag.process_folder_complete(
                folder_path=folder_path,
                output_dir=output_dir,
                parse_method=parse_method,
                recursive=recursive,
                max_workers=max_workers,
                **kwargs
            )
            return {
                "success": True,
                "folder_path": folder_path,
                "message": f"成功处理文件夹: {folder_path}"
            }
        except Exception as e:
            raise ValueError(f"处理文件夹失败: {str(e)}")

    async def query(
        self,
        query: str,
        mode: str = "hybrid",
        **kwargs
    ) -> str:
        """
        使用文本查询 RAG 系统

        参数:
            query: 查询文本
            mode: 查询模式 (local, global, hybrid, naive, mix, bypass)
            **kwargs: 额外查询参数

        返回:
            查询结果
        """
        try:
            result = await self.rag.aquery(query=query, mode=mode, **kwargs)
            return result
        except Exception as e:
            raise ValueError(f"执行查询失败: {str(e)}")

    async def query_with_multimodal(
        self,
        query: str,
        multimodal_content: List[Dict[str, Any]],
        mode: str = "hybrid",
        **kwargs
    ) -> str:
        """
        使用多模态内容查询

        参数:
            query: 查询文本
            multimodal_content: 多模态内容项列表
            mode: 查询模式
            **kwargs: 额外查询参数

        返回:
            查询结果
        """
        try:
            result = await self.rag.aquery_with_multimodal(
                query=query,
                multimodal_content=multimodal_content,
                mode=mode,
                **kwargs
            )
            return result
        except Exception as e:
            raise ValueError(f"执行多模态查询失败: {str(e)}")

    async def get_config_info(self) -> Dict[str, Any]:
        """
        获取配置信息

        返回:
            配置字典
        """
        try:
            return self.rag.get_config_info()
        except Exception as e:
            raise ValueError(f"获取配置信息失败: {str(e)}")

    async def get_processor_info(self) -> Dict[str, Any]:
        """
        获取处理器信息

        返回:
            处理器信息字典
        """
        try:
            return self.rag.get_processor_info()
        except Exception as e:
            raise ValueError(f"获取处理器信息失败: {str(e)}")

    async def finalize(self):
        """完成并清理资源"""
        if not self._initialized or not self.rag:
            return
# noqa  MS80OmFIVnBZMlhsa0xUb3Y2bzZNalJxY1E9PTo0Nzk0MDQyYQ==

        try:
            logger.info("正在清理 RAGAnything 资源...")
            await self.rag.finalize_storages()
            logger.info("✅ 资源清理完成")
        except Exception as e:
            logger.error(f"完成存储清理失败: {str(e)}")
            raise ValueError(f"完成存储清理失败: {str(e)}")

    async def parse_document_only(
        self,
        file_path: str,
        output_dir: Optional[str] = None,
        parse_method: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        仅解析文档而不插入到 RAG

        参数:
            file_path: 文档路径
            output_dir: 解析内容的输出目录
            parse_method: 使用的解析方法
            **kwargs: 额外参数

        返回:
            解析的内容列表
        """
        try:
            content_list, doc_id = await self.rag.parse_document(
                file_path=file_path,
                output_dir=output_dir,
                parse_method=parse_method,
                **kwargs
            )
            return {
                "success": True,
                "file_path": file_path,
                "doc_id": doc_id,
                "content_count": len(content_list),
                "content_list": content_list,
            }
        except Exception as e:
            raise ValueError(f"解析文档失败: {str(e)}")

    async def insert_content(
        self,
        content_list: List[Dict[str, Any]],
        file_path: str = "unknown_document",
        **kwargs
    ) -> Dict[str, Any]:
        """
        将预解析的内容插入到 RAG

        参数:
            content_list: 内容项列表
            file_path: 源文件路径（用于参考）
            **kwargs: 额外参数

        返回:
            插入结果字典
        """
        try:
            await self.rag.insert_content_list(
                content_list=content_list,
                file_path=file_path,
                **kwargs
            )
            return {
                "success": True,
                "file_path": file_path,
                "message": f"成功插入 {len(content_list)} 个内容项"
            }
        except Exception as e:
            raise ValueError(f"插入内容失败: {str(e)}")


class RAGAnythingContext:
    """RAG Anything MCP 服务器的上下文对象"""

    def __init__(self, connector: RAGAnythingConnector):
        self.connector = connector


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[RAGAnythingContext]:
    """
    管理 RAG Anything 连接器的应用程序生命周期

    参数:
        server: FastMCP 服务器实例

    生成:
        包含已初始化连接器的 RAGAnythingContext
    """
    config = server.config

    # 从环境变量或配置获取配置
    working_dir = config.get("working_dir", os.getenv("RAG_WORKING_DIR", "./rag_storage"))

    # LLM 配置
    llm_api_key = config.get("llm_api_key", os.getenv("LLM_API_KEY"))
    llm_base_url = config.get("llm_base_url", os.getenv("LLM_BASE_URL"))
    llm_model = config.get("llm_model", os.getenv("LLM_MODEL", "deepseek-chat"))

    # 视觉模型配置
    vision_api_key = config.get("vision_api_key", os.getenv("VISION_API_KEY"))
    vision_base_url = config.get("vision_base_url", os.getenv("VISION_BASE_URL"))
    vision_model = config.get("vision_model", os.getenv("VISION_MODEL"))

    # 嵌入配置
    embedding_host = config.get("embedding_host", os.getenv("EMBEDDING_HOST", "http://35.235.113.151:11434"))
    embedding_model = config.get("embedding_model", os.getenv("EMBEDDING_MODEL", "qwen3-embedding:0.6b"))
    embedding_dim = int(config.get("embedding_dim", os.getenv("EMBEDDING_DIM", "1024")))
    use_ollama_embedding = config.get("use_ollama_embedding", os.getenv("USE_OLLAMA_EMBEDDING", "true").lower() == "true")

    # 解析器配置
    parser = config.get("parser", os.getenv("RAG_PARSER", "docling"))
    parse_method = config.get("parse_method", os.getenv("RAG_PARSE_METHOD", "auto"))

    # 功能标志
    enable_image = config.get("enable_image_processing", os.getenv("RAG_ENABLE_IMAGE", "true").lower() == "true")
    enable_table = config.get("enable_table_processing", os.getenv("RAG_ENABLE_TABLE", "true").lower() == "true")
    enable_equation = config.get("enable_equation_processing", os.getenv("RAG_ENABLE_EQUATION", "true").lower() == "true")
# pragma: no cover  Mi80OmFIVnBZMlhsa0xUb3Y2bzZNalJxY1E9PTo0Nzk0MDQyYQ==

    # 是否加载已有知识库
    load_existing = config.get("load_existing", os.getenv("LOAD_EXISTING", "true").lower() == "true")

    # 创建连接器
    logger.info("正在创建 RAGAnything 连接器...")
    connector = RAGAnythingConnector(
        working_dir=working_dir,
        llm_api_key=llm_api_key,
        llm_base_url=llm_base_url,
        llm_model=llm_model,
        vision_api_key=vision_api_key,
        vision_base_url=vision_base_url,
        vision_model=vision_model,
        embedding_host=embedding_host,
        embedding_model=embedding_model,
        embedding_dim=embedding_dim,
        use_ollama_embedding=use_ollama_embedding,
        parser=parser,
        parse_method=parse_method,
        enable_image_processing=enable_image,
        enable_table_processing=enable_table,
        enable_equation_processing=enable_equation,
        load_existing=load_existing,
    )

    # 初始化连接器（加载已有知识库或创建新实例）
    await connector.initialize()

    try:
        yield RAGAnythingContext(connector)
    finally:
        # 清理资源
        await connector.finalize()


# 创建 FastMCP 服务器实例
mcp = FastMCP(name="RAG Anything", lifespan=server_lifespan)


# ==========================================
# MCP 工具
# ==========================================

@mcp.tool()
async def process_document(
    ctx: Context,
    file_path: str,
    output_dir: str = None,
    parse_method: str = None,
) -> str:
    """
    处理单个文档并将其添加到 RAG 系统

    此工具解析文档（PDF、图像、Office 文件等）并将其内容插入到 RAG 知识库中。
    文档将被解析以提取文本和多模态内容（图像、表格、公式）。

    参数:
        file_path: 要处理的文档文件路径
        output_dir: 解析内容的可选输出目录（默认使用配置）
        parse_method: 可选的解析方法 (auto, ocr, txt)（默认使用配置）

    返回:
        包含处理详情的成功消息
    """
    connector = ctx.request_context.lifespan_context.connector

    # 验证文件路径
    if not os.path.exists(file_path):
        return f"错误: 文件未找到: {file_path}"

    try:
        result = await connector.process_document(
            file_path=file_path,
            output_dir=output_dir,
            parse_method=parse_method,
        )
        return f"✅ 成功处理文档: {file_path}\n\n文档已被解析并添加到 RAG 知识库。"
    except Exception as e:
        return f"❌ 处理文档时出错: {str(e)}"


@mcp.tool()
async def process_folder(
    ctx: Context,
    folder_path: str,
    output_dir: str = None,
    parse_method: str = None,
    recursive: bool = True,
    max_workers: int = None,
) -> str:
    """
    处理文件夹中的所有文档并将其添加到 RAG 系统

    此工具处理文件夹中的多个文档，解析每个文档并将其内容插入到 RAG 知识库中。

    参数:
        folder_path: 包含文档的文件夹路径
        output_dir: 解析内容的可选输出目录（默认使用配置）
        parse_method: 可选的解析方法 (auto, ocr, txt)（默认使用配置）
        recursive: 是否递归处理子文件夹（默认: True）
        max_workers: 最大并发工作线程数（默认使用配置）

    返回:
        包含处理详情的成功消息
    """
    connector = ctx.request_context.lifespan_context.connector
# noqa  My80OmFIVnBZMlhsa0xUb3Y2bzZNalJxY1E9PTo0Nzk0MDQyYQ==

    # 验证文件夹路径
    if not os.path.exists(folder_path):
        return f"错误: 文件夹未找到: {folder_path}"

    if not os.path.isdir(folder_path):
        return f"错误: 路径不是目录: {folder_path}"

    try:
        result = await connector.process_folder(
            folder_path=folder_path,
            output_dir=output_dir,
            parse_method=parse_method,
            recursive=recursive,
            max_workers=max_workers,
        )
        return f"✅ 成功处理文件夹: {folder_path}\n\n文件夹中的所有文档已被解析并添加到 RAG 知识库。"
    except Exception as e:
        return f"❌ 处理文件夹时出错: {str(e)}"


@mcp.tool()
async def query(
    ctx: Context,
    query: str,
    mode: str = "hybrid",
) -> str:
    """
    使用文本查询 RAG 系统

    此工具使用提供的查询文本搜索 RAG 知识库并返回相关信息。

    参数:
        query: 要搜索的查询文本
        mode: 查询模式 - 以下之一:
            - "local": 搜索特定实体和关系
            - "global": 搜索广泛主题和摘要
            - "hybrid": 结合本地和全局搜索（默认）
            - "naive": 简单的向量相似度搜索
            - "mix": 混合不同的搜索策略
            - "bypass": 直接 LLM 查询，不使用 RAG

    返回:
        包含知识库相关信息的查询结果
    """
    connector = ctx.request_context.lifespan_context.connector

    # 验证模式
    valid_modes = ["local", "global", "hybrid", "naive", "mix", "bypass"]
    if mode not in valid_modes:
        return f"错误: 无效的模式 '{mode}'。必须是以下之一: {', '.join(valid_modes)}"

    try:
        result = await connector.query(query=query, mode=mode)
        return result
    except Exception as e:
        return f"❌ 执行查询时出错: {str(e)}"


@mcp.tool()
async def query_with_images(
    ctx: Context,
    query: str,
    image_paths: List[str],
    mode: str = "hybrid",
) -> str:
    """
    使用文本和图像查询 RAG 系统

    此工具执行结合文本和图像的多模态查询，适用于关于文档中视觉内容的问题。

    参数:
        query: 查询文本
        image_paths: 要包含在查询中的图像文件路径列表
        mode: 查询模式 (local, global, hybrid, naive, mix, bypass)

    返回:
        结合文本和图像分析的查询结果
    """
    connector = ctx.request_context.lifespan_context.connector

    # 验证模式
    valid_modes = ["local", "global", "hybrid", "naive", "mix", "bypass"]
    if mode not in valid_modes:
        return f"错误: 无效的模式 '{mode}'。必须是以下之一: {', '.join(valid_modes)}"

    # 验证图像路径
    for img_path in image_paths:
        if not os.path.exists(img_path):
            return f"错误: 图像文件未找到: {img_path}"

    # 构建多模态内容
    multimodal_content = [
        {"type": "image", "img_path": img_path}
        for img_path in image_paths
    ]

    try:
        result = await connector.query_with_multimodal(
            query=query,
            multimodal_content=multimodal_content,
            mode=mode,
        )
        return result
    except Exception as e:
        return f"❌ 执行多模态查询时出错: {str(e)}"


@mcp.tool()
async def get_config(ctx: Context) -> str:
    """
    获取当前 RAG Anything 配置

    返回当前配置的详细信息，包括:
    - 工作目录
    - 解析器设置
    - 多模态处理设置
    - 批处理设置
    - 上下文提取设置

    返回:
        包含配置详情的 JSON 字符串
    """
    connector = ctx.request_context.lifespan_context.connector

    try:
        config_info = await connector.get_config_info()
        return json.dumps(config_info, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"❌ 获取配置时出错: {str(e)}"


@mcp.tool()
async def get_processor_status(ctx: Context) -> str:
    """
    获取处理器状态信息

    返回处理器当前状态的信息，包括:
    - 可用的处理器
    - 处理器配置
    - 处理能力

    返回:
        包含处理器状态详情的 JSON 字符串
    """
    connector = ctx.request_context.lifespan_context.connector

    try:
        processor_info = await connector.get_processor_info()
        return json.dumps(processor_info, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"❌ 获取处理器状态时出错: {str(e)}"


@mcp.tool()
async def list_supported_formats(ctx: Context) -> str:
    """
    列出所有支持的文件格式

    返回 RAG 系统可以处理的文件扩展名列表。

    返回:
        格式化的支持文件格式列表
    """
    connector = ctx.request_context.lifespan_context.connector

    try:
        extensions = connector.rag.get_supported_file_extensions()

        result = "📄 支持的文件格式:\n\n"
        result += "文档:\n"
        result += "  - PDF: .pdf\n"
        result += "  - Office: .doc, .docx, .ppt, .pptx, .xls, .xlsx\n"
        result += "  - 文本: .txt, .md\n"
        result += "  - HTML: .html, .htm\n\n"
        result += "图像:\n"
        result += "  - .png, .jpg, .jpeg, .bmp, .tiff, .gif, .webp\n\n"
        result += f"支持的扩展名总数: {len(extensions)}\n"
        result += f"扩展名: {', '.join(sorted(extensions))}"

        return result
    except Exception as e:
        return f"❌ 列出支持格式时出错: {str(e)}"


@mcp.tool()
async def parse_document_only(
    ctx: Context,
    file_path: str,
    output_dir: str = None,
    parse_method: str = None,
) -> str:
    """
    仅解析文档而不将其插入到 RAG 系统

    此工具仅解析文档并返回解析的内容结构，而不将其添加到知识库。
    适用于预览文档结构或在插入前处理内容。

    参数:
        file_path: 要解析的文档文件路径
        output_dir: 解析内容的可选输出目录（默认使用配置）
        parse_method: 可选的解析方法 (auto, ocr, txt)（默认使用配置）

    返回:
        包含解析内容信息的 JSON 字符串
    """
    connector = ctx.request_context.lifespan_context.connector

    # 验证文件路径
    if not os.path.exists(file_path):
        return f"错误: 文件未找到: {file_path}"

    try:
        result = await connector.parse_document_only(
            file_path=file_path,
            output_dir=output_dir,
            parse_method=parse_method,
        )

        # 格式化响应
        response = f"✅ 成功解析文档: {file_path}\n\n"
        response += f"文档 ID: {result['doc_id']}\n"
        response += f"内容项数量: {result['content_count']}\n\n"
        response += "内容结构:\n"

        # 统计内容类型
        content_types = {}
        for item in result['content_list']:
            content_type = item.get('type', 'unknown')
            content_types[content_type] = content_types.get(content_type, 0) + 1

        for content_type, count in sorted(content_types.items()):
            response += f"  - {content_type}: {count}\n"

        return response
    except Exception as e:
        return f"❌ 解析文档时出错: {str(e)}"


@mcp.tool()
async def insert_parsed_content(
    ctx: Context,
    content_json: str,
    file_path: str = "unknown_document",
) -> str:
    """
    将预解析的内容插入到 RAG 系统

    此工具允许您插入先前解析或手动构建的内容，而无需重新解析原始文档。

    参数:
        content_json: 包含内容列表的 JSON 字符串
        file_path: 源文件路径（用于参考）（默认: "unknown_document"）

    返回:
        包含插入详情的成功消息
    """
    connector = ctx.request_context.lifespan_context.connector

    try:
        # 解析 JSON 内容
        content_list = json.loads(content_json)

        if not isinstance(content_list, list):
            return "错误: content_json 必须是 JSON 数组"

        result = await connector.insert_content(
            content_list=content_list,
            file_path=file_path,
        )

        return f"✅ 成功从 {file_path} 插入 {len(content_list)} 个内容项"
    except json.JSONDecodeError as e:
        return f"❌ 解析 JSON 时出错: {str(e)}"
    except Exception as e:
        return f"❌ 插入内容时出错: {str(e)}"


# ==========================================
# 主入口点
# ==========================================

def main():
    """MCP 服务器的主入口点"""
    # 加载环境变量
    load_dotenv()

    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="RAG Anything MCP 服务器 - 多模态文档处理和查询"
    )
    parser.add_argument(
        "--working-dir",
        type=str,
        default=os.getenv("RAG_WORKING_DIR", "./rag_storage"),
        help="RAG 存储的工作目录 (默认: ./rag_storage)",
    )
    parser.add_argument(
        "--llm-api-key",
        type=str,
        default=os.getenv("LLM_API_KEY"),
        help="LLM 的 API 密钥",
    )
    parser.add_argument(
        "--llm-base-url",
        type=str,
        default=os.getenv("LLM_BASE_URL"),
        help="LLM API 的基础 URL",
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        default=os.getenv("LLM_MODEL", "deepseek-chat"),
        help="LLM 模型名称 (默认: deepseek-chat)",
    )
    parser.add_argument(
        "--vision-model",
        type=str,
        default=os.getenv("VISION_MODEL"),
        help="视觉模型名称 (可选)",
    )
    parser.add_argument(
        "--embedding-host",
        type=str,
        default=os.getenv("EMBEDDING_HOST", "http://35.235.113.151:11434"),
        help="Ollama 嵌入服务器地址 (默认: http://35.235.113.151:11434)",
    )
    parser.add_argument(
        "--embedding-model",
        type=str,
        default=os.getenv("EMBEDDING_MODEL", "qwen3-embedding:0.6b"),
        help="嵌入模型名称 (默认: qwen3-embedding:0.6b)",
    )
    parser.add_argument(
        "--embedding-dim",
        type=int,
        default=int(os.getenv("EMBEDDING_DIM", "1024")),
        help="嵌入维度 (默认: 1024)",
    )
    parser.add_argument(
        "--use-ollama-embedding",
        action="store_true",
        default=os.getenv("USE_OLLAMA_EMBEDDING", "true").lower() == "true",
        help="使用 Ollama 嵌入 (默认: True)",
    )
    parser.add_argument(
        "--parser",
        type=str,
        choices=["mineru", "docling"],
        default=os.getenv("RAG_PARSER", "docling"),
        help="使用的解析器 (默认: docling)",
    )
    parser.add_argument(
        "--parse-method",
        type=str,
        choices=["auto", "ocr", "txt"],
        default=os.getenv("RAG_PARSE_METHOD", "auto"),
        help="解析方法 (默认: auto)",
    )
    parser.add_argument(
        "--load-existing",
        action="store_true",
        default=os.getenv("LOAD_EXISTING", "true").lower() == "true",
        help="加载已存在的知识库 (默认: True)",
    )

    args = parser.parse_args()

    # 使用命令行参数更新服务器配置
    mcp.config = {
        "working_dir": args.working_dir,
        "llm_api_key": args.llm_api_key,
        "llm_base_url": args.llm_base_url,
        "llm_model": args.llm_model,
        "vision_model": args.vision_model,
        "embedding_host": args.embedding_host,
        "embedding_model": args.embedding_model,
        "embedding_dim": args.embedding_dim,
        "use_ollama_embedding": args.use_ollama_embedding,
        "parser": args.parser,
        "parse_method": args.parse_method,
        "load_existing": args.load_existing,
    }

    # 运行服务器
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
