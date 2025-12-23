"""
测试记忆体配置文件

包含所有记忆体功能的配置参数和环境设置
"""

import os
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class TestingMemoryConfig:
    """测试记忆体配置类"""
    
    # 模型配置
    model_name: str = "deepseek:deepseek-chat"
    embedding_model: str = "ollama:nomic-embed-text"
    embedding_dims: int = 768
    
    # API配置
    deepseek_api_key: str = "sk-b68ccb70b0934c4c80cb58a95f9cee00"
    ollama_host: str = "http://155.138.220.75:11434"
    
    # 记忆体存储配置
    memory_namespaces: Dict[str, str] = None
    max_memory_items: int = 1000
    memory_search_limit: int = 5
    
    # 测试配置
    test_timeout: int = 300  # 5分钟
    max_retry_attempts: int = 3
    confidence_threshold: float = 0.8
    
    # 日志配置
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    def __post_init__(self):
        """初始化后处理"""
        if self.memory_namespaces is None:
            self.memory_namespaces = {
                "test_experiences": ("testing", "experiences"),
                "test_contexts": ("testing", "contexts"),
                "test_executions": ("testing", "executions"),
                "error_handling": ("testing", "errors"),
                "recommendations": ("testing", "recommendations"),
                "strategies": ("testing", "strategies")
            }
        
        # 设置环境变量
        os.environ["DEEPSEEK_API_KEY"] = self.deepseek_api_key
        os.environ["OLLAMA_HOST"] = self.ollama_host
    
    def get_namespace(self, memory_type: str) -> tuple:
        """获取指定类型的命名空间"""
        return self.memory_namespaces.get(memory_type, ("testing", "default"))
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "model_name": self.model_name,
            "embedding_model": self.embedding_model,
            "embedding_dims": self.embedding_dims,
            "memory_namespaces": self.memory_namespaces,
            "max_memory_items": self.max_memory_items,
            "memory_search_limit": self.memory_search_limit,
            "test_timeout": self.test_timeout,
            "max_retry_attempts": self.max_retry_attempts,
            "confidence_threshold": self.confidence_threshold,
            "log_level": self.log_level
        }

# 默认配置实例
DEFAULT_CONFIG = TestingMemoryConfig()

# 测试场景配置
TEST_SCENARIOS_CONFIG = {
    "basic_conversation": {
        "description": "基础对话测试场景",
        "memory_types": ["test_experiences", "test_contexts"],
        "expected_duration": 30
    },
    "complex_task": {
        "description": "复杂任务处理场景", 
        "memory_types": ["test_executions", "strategies"],
        "expected_duration": 120
    },
    "error_handling": {
        "description": "错误处理场景",
        "memory_types": ["error_handling", "strategies"],
        "expected_duration": 60
    },
    "boundary_testing": {
        "description": "边界值测试场景",
        "memory_types": ["test_executions", "recommendations"],
        "expected_duration": 90
    },
    "performance_testing": {
        "description": "性能测试场景",
        "memory_types": ["test_executions", "strategies"],
        "expected_duration": 180
    }
}

def get_scenario_config(scenario_name: str) -> Dict[str, Any]:
    """获取指定场景的配置"""
    return TEST_SCENARIOS_CONFIG.get(scenario_name, {})

def validate_config(config: TestingMemoryConfig) -> bool:
    """验证配置的有效性"""
    try:
        # 检查必要的配置项
        assert config.model_name, "模型名称不能为空"
        assert config.embedding_model, "嵌入模型不能为空"
        assert config.embedding_dims > 0, "嵌入维度必须大于0"
        assert config.max_memory_items > 0, "最大记忆项数必须大于0"
        assert 0 < config.confidence_threshold <= 1, "置信度阈值必须在0-1之间"
        
        return True
    except AssertionError as e:
        print(f"配置验证失败: {e}")
        return False