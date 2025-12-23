# PDF 处理器
"""
PDF 文档处理器，支持文本提取和缓存
"""
"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# pip install -qU langchain-pymupdf4llm

import tempfile
import os
import logging
import hashlib
import time
from typing import Optional

from file_rag.core.config import settings

# 尝试导入 PDF 处理库
try:
    from langchain_community.document_loaders import PyPDFLoader
except ImportError:
    PyPDFLoader = None

try:
    from langchain_pymupdf4llm import PyMuPDF4LLMLoader
except ImportError:
    PyMuPDF4LLMLoader = None

logger = logging.getLogger(__name__)

# PDF 内容缓存，避免重复解析同一个文件
_pdf_cache = {}


def _safe_delete_temp_file(file_path: str, max_retries: int = 3, delay: float = 0.1):
    """
    安全删除临时文件，处理Windows文件锁定问题

    Args:
        file_path: 要删除的文件路径
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
    """
    if not os.path.exists(file_path):
        return

    for attempt in range(max_retries):
        try:
            os.unlink(file_path)
            logger.debug(f"临时文件已删除: {file_path}")
            return
        except PermissionError as e:
            if attempt < max_retries - 1:
                logger.debug(f"删除临时文件失败（尝试 {attempt + 1}/{max_retries}），等待后重试: {e}")
                time.sleep(delay)
            else:
                logger.warning(f"无法删除临时文件（已重试{max_retries}次），文件将由系统清理: {file_path}")
        except Exception as e:
            logger.warning(f"删除临时文件时发生异常: {e}")
            break


class PDFProcessor:
    """PDF 处理器类"""
    
    def __init__(self, enable_cache: bool = True):
        self.enable_cache = enable_cache
        self.cache = _pdf_cache if enable_cache else {}
    
    def extract_text(self, pdf_data: bytes, filename: str = "unknown.pdf") -> str:
        """从PDF字节数据中提取文本"""
        return extract_pdf_text(pdf_data, filename, self.cache if self.enable_cache else None)
    
    def clear_cache(self):
        """清空缓存"""
        if self.enable_cache:
            self.cache.clear()
    
    def get_cache_stats(self) -> dict:
        """获取缓存统计信息"""
        return {
            "cache_enabled": self.enable_cache,
            "cached_files": len(self.cache) if self.enable_cache else 0,
            "cache_keys": list(self.cache.keys()) if self.enable_cache else []
        }


def extract_pdf_text(pdf_data: bytes, filename: str = "unknown.pdf", cache: Optional[dict] = None) -> str:
    """
    从PDF字节数据中提取文本，使用缓存避免重复解析
    提取的方法：
    1、langchain pdf加载器：https://docs.langchain.com/oss/python/integrations/document_loaders/index#pdfs
        推荐 pip install -qU langchain-community langchain-pymupdf4llm，支持基于多模态大模型进行图片解析
    2、DeepSeek ocr大模型
    3、PaddleOCR VL 0.9B（推荐）--部署需要GPU
        推荐 https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PaddleOCR-VL.html

    """
    try:
        # 生成PDF数据的哈希值作为缓存键
        pdf_hash = hashlib.md5(pdf_data).hexdigest()
        cache_key = f"{filename}_{pdf_hash}"

        # 检查缓存
        if cache is not None and cache_key in cache:
            logger.info(f"从缓存中获取PDF内容: {filename}")
            return cache[cache_key]

        # 创建临时文件（Windows需要先关闭文件句柄才能被其他程序访问）
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        try:
            temp_file.write(pdf_data)
            temp_file.flush()  # 确保数据写入磁盘
            os.fsync(temp_file.fileno())  # 强制同步到磁盘
            temp_file_path = temp_file.name
        finally:
            temp_file.close()  # 显式关闭文件句柄，释放文件锁

        try:
            text_content = ""

            # 优先使用 PyMuPDF4LLM
            if PyMuPDF4LLMLoader is not None:
                try:
                    logger.info(f"使用 PyMuPDF4LLM 解析PDF: {filename}")
                    loader = PyMuPDF4LLMLoader(
                        temp_file_path,
                        mode="single",  # 作为单个文档处理
                        extract_images=settings.PDF_EXTRACT_IMAGES,  # 提取图片
                        table_strategy="lines"  # 提取表格
                    )
                    documents = loader.load()

                    if documents:
                        text_content = documents[0].page_content
                        logger.info(f"PyMuPDF4LLM 解析成功，内容长度: {len(text_content)} 字符")
                    else:
                        text_content = "PDF文件解析后内容为空"

                except Exception as e:
                    logger.warning(f"PyMuPDF4LLM 解析失败，尝试备用方法: {e}")
                    text_content = ""

            # 如果 PyMuPDF4LLM 失败，使用 PyPDFLoader 作为备用
            if not text_content and PyPDFLoader is not None:
                try:
                    logger.info(f"使用 PyPDFLoader 解析PDF: {filename}")
                    loader = PyPDFLoader(temp_file_path)
                    documents = loader.load()
                    text_content = "\n\n".join([doc.page_content for doc in documents])
                    logger.info(f"PyPDFLoader 解析成功，内容长度: {len(text_content)} 字符")
                except Exception as e:
                    logger.warning(f"PyPDFLoader 解析失败: {e}")
                    text_content = ""

            # 如果都失败，尝试使用 PyPDF2
            if not text_content:
                try:
                    import PyPDF2
                    logger.info(f"使用 PyPDF2 解析PDF: {filename}")
                    with open(temp_file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        text_content = ""
                        for page in pdf_reader.pages:
                            text_content += page.extract_text() + "\n\n"
                    logger.info(f"PyPDF2 解析成功，内容长度: {len(text_content)} 字符")
                except ImportError:
                    logger.warning("No PDF processing library available")
                    text_content = "PDF文件已接收，但无法提取文本内容（缺少PDF处理库）"
                except Exception as e:
                    logger.warning(f"PyPDF2 解析失败: {e}")
                    text_content = f"PDF文件处理出错: {str(e)}"

            # 如果仍然没有内容
            if not text_content:
                text_content = "PDF文件无法解析或内容为空"

            # 缓存结果
            if cache is not None:
                cache[cache_key] = text_content
                logger.info(f"PDF内容已缓存: {filename}")

            return text_content

        finally:
            # 清理临时文件（Windows上可能需要重试）
            _safe_delete_temp_file(temp_file_path)

    except Exception as e:
        logger.error(f"PDF文本提取失败: {e}")
        return f"PDF文件处理出错: {str(e)}"
