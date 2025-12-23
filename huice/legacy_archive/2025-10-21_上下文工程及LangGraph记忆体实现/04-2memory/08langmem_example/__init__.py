"""
测试记忆体功能演示包

这个包演示了如何在软件测试智能体中应用记忆体功能，包括：
1. 测试经验积累与学习
2. 测试上下文记忆
3. 测试用例执行记忆
4. 错误处理经验记忆
5. 智能测试用例推荐
6. 自适应测试策略

作者: AI Assistant
创建时间: 2024-01-15
"""

from .config import TestingMemoryConfig
from .models import (
    TestExecutionMemory,
    ErrorHandlingMemory,
    TestContextMemory,
    TestExperienceEpisode
)
from .memory_manager import TestingMemoryManager
from .scenarios import (
    TestExperienceScenario,
    TestContextScenario,
    TestExecutionScenario,
    ErrorHandlingScenario,
    SmartRecommendationScenario,
    AdaptiveStrategyScenario
)

__version__ = "1.0.0"
__all__ = [
    "TestingMemoryConfig",
    "TestExecutionMemory",
    "ErrorHandlingMemory", 
    "TestContextMemory",
    "TestExperienceEpisode",
    "TestingMemoryManager",
    "TestExperienceScenario",
    "TestContextScenario",
    "TestExecutionScenario",
    "ErrorHandlingScenario",
    "SmartRecommendationScenario",
    "AdaptiveStrategyScenario"
]