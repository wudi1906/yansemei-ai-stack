"""
测试记忆体管理器

统一管理各种类型的测试记忆体，提供存储、检索、更新等功能
"""

import uuid
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from langgraph.store.memory import InMemoryStore
from langmem import create_memory_store_manager

from .config import TestingMemoryConfig, DEFAULT_CONFIG
from .models import (
    TestExperienceEpisode,
    TestExecutionMemory,
    ErrorHandlingMemory,
    TestContextMemory,
    TestRecommendation,
    TestStrategy
)

class TestingMemoryManager:
    """测试记忆体管理器"""
    
    def __init__(self, config: TestingMemoryConfig = None):
        """初始化记忆体管理器"""
        self.config = config or DEFAULT_CONFIG
        
        # 初始化模型和嵌入
        self.model = init_chat_model(self.config.model_name)
        self.embeddings = init_embeddings(
            self.config.embedding_model, 
            base_url=self.config.ollama_host
        )
        
        # 初始化存储
        self.store = InMemoryStore(
            index={
                "embed": self.embeddings,
                "dims": self.config.embedding_dims,
            }
        )
        
        # 初始化各类型的记忆管理器
        self._init_memory_managers()
    
    def _init_memory_managers(self):
        """初始化各种类型的记忆管理器"""
        
        # 测试经验管理器
        self.experience_manager = create_memory_store_manager(
            self.model,
            namespace=self.config.get_namespace("test_experiences"),
            schemas=[TestExperienceEpisode],
            instructions="记录测试经验和学习成果，捕捉成功的测试策略和失败的教训",
            enable_inserts=True,
            store=self.store
        )
        
        # 测试执行管理器
        self.execution_manager = create_memory_store_manager(
            self.model,
            namespace=self.config.get_namespace("test_executions"),
            schemas=[TestExecutionMemory],
            instructions="记录测试用例执行过程，包括策略、结果和优化建议",
            enable_inserts=True,
            store=self.store
        )
        
        # 错误处理管理器
        self.error_manager = create_memory_store_manager(
            self.model,
            namespace=self.config.get_namespace("error_handling"),
            schemas=[ErrorHandlingMemory],
            instructions="记录错误处理经验，包括错误类型、解决方案和效果评估",
            enable_inserts=True,
            store=self.store
        )
        
        # 上下文管理器
        self.context_manager = create_memory_store_manager(
            self.model,
            namespace=self.config.get_namespace("test_contexts"),
            schemas=[TestContextMemory],
            instructions="记录测试上下文信息，包括环境配置、用户偏好和历史数据",
            enable_inserts=True,
            store=self.store
        )
    
    def store_experience(self, experience: TestExperienceEpisode) -> str:
        """存储测试经验"""
        memory_id = str(uuid.uuid4())
        namespace = self.config.get_namespace("test_experiences")
        
        self.store.put(namespace, memory_id, {
            "content": experience.dict(),
            "type": "experience",
            "timestamp": datetime.now().isoformat()
        })
        
        return memory_id
    
    def store_execution(self, execution: TestExecutionMemory) -> str:
        """存储测试执行记录"""
        memory_id = str(uuid.uuid4())
        namespace = self.config.get_namespace("test_executions")
        
        self.store.put(namespace, memory_id, {
            "content": execution.dict(),
            "type": "execution",
            "timestamp": datetime.now().isoformat()
        })
        
        return memory_id
    
    def store_error(self, error: ErrorHandlingMemory) -> str:
        """存储错误处理记录"""
        memory_id = str(uuid.uuid4())
        namespace = self.config.get_namespace("error_handling")
        
        self.store.put(namespace, memory_id, {
            "content": error.dict(),
            "type": "error",
            "timestamp": datetime.now().isoformat()
        })
        
        return memory_id
    
    def store_context(self, context: TestContextMemory) -> str:
        """存储测试上下文"""
        memory_id = str(uuid.uuid4())
        namespace = self.config.get_namespace("test_contexts")
        
        self.store.put(namespace, memory_id, {
            "content": context.dict(),
            "type": "context",
            "timestamp": datetime.now().isoformat()
        })
        
        return memory_id
    
    def search_experiences(self, query: str, limit: int = None) -> List[Dict[str, Any]]:
        """搜索相关的测试经验"""
        limit = limit or self.config.memory_search_limit
        namespace = self.config.get_namespace("test_experiences")
        
        results = self.store.search(namespace, query=query, limit=limit)
        return [item.value for item in results]
    
    def search_executions(self, query: str, limit: int = None) -> List[Dict[str, Any]]:
        """搜索相关的测试执行记录"""
        limit = limit or self.config.memory_search_limit
        namespace = self.config.get_namespace("test_executions")
        
        results = self.store.search(namespace, query=query, limit=limit)
        return [item.value for item in results]
    
    def search_errors(self, query: str, limit: int = None) -> List[Dict[str, Any]]:
        """搜索相关的错误处理记录"""
        limit = limit or self.config.memory_search_limit
        namespace = self.config.get_namespace("error_handling")
        
        results = self.store.search(namespace, query=query, limit=limit)
        return [item.value for item in results]
    
    def search_contexts(self, query: str, limit: int = None) -> List[Dict[str, Any]]:
        """搜索相关的测试上下文"""
        limit = limit or self.config.memory_search_limit
        namespace = self.config.get_namespace("test_contexts")
        
        results = self.store.search(namespace, query=query, limit=limit)
        return [item.value for item in results]
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆体统计信息"""
        stats = {}
        
        for memory_type, namespace in self.config.memory_namespaces.items():
            # 这里简化统计，实际实现可能需要更复杂的查询
            try:
                results = self.store.search(namespace, query="", limit=1000)
                stats[memory_type] = len(results)
            except:
                stats[memory_type] = 0
        
        return stats
    
    def clear_memory(self, memory_type: str = None):
        """清除指定类型的记忆体"""
        if memory_type:
            # 清除特定类型的记忆
            namespace = self.config.get_namespace(memory_type)
            # 注意：InMemoryStore 可能没有直接的清除方法，这里是概念性实现
            print(f"清除 {memory_type} 类型的记忆体")
        else:
            # 清除所有记忆
            print("清除所有记忆体")
    
    def export_memories(self, memory_type: str = None) -> Dict[str, Any]:
        """导出记忆体数据"""
        if memory_type:
            namespace = self.config.get_namespace(memory_type)
            results = self.store.search(namespace, query="", limit=1000)
            return {
                "type": memory_type,
                "count": len(results),
                "data": [item.value for item in results]
            }
        else:
            # 导出所有类型的记忆
            all_memories = {}
            for mem_type in self.config.memory_namespaces.keys():
                all_memories[mem_type] = self.export_memories(mem_type)
            return all_memories