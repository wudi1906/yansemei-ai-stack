"""
测试记忆体数据模型定义

定义了各种测试场景中使用的记忆体数据结构
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

class TestResult(str, Enum):
    """测试结果枚举"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

class TestType(str, Enum):
    """测试类型枚举"""
    UNIT = "unit"
    INTEGRATION = "integration"
    SYSTEM = "system"
    PERFORMANCE = "performance"
    SECURITY = "security"
    UI = "ui"

class ErrorType(str, Enum):
    """错误类型枚举"""
    NETWORK_TIMEOUT = "network_timeout"
    DATABASE_ERROR = "database_error"
    AUTHENTICATION_FAILED = "authentication_failed"
    VALIDATION_ERROR = "validation_error"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    UNKNOWN_ERROR = "unknown_error"

class TestExperienceEpisode(BaseModel):
    """测试经验记录模型 - 基于Episode模式"""
    
    observation: str = Field(
        ..., 
        description="测试场景的观察和背景 - 发生了什么"
    )
    thoughts: str = Field(
        ...,
        description="内部推理过程与智能体在测试中的观察，使其得出正确的行动与结果"
    )
    action: str = Field(
        ...,
        description="采取的测试行动、如何执行的、以何种格式呈现"
    )
    result: str = Field(
        ...,
        description="测试结果与回顾。哪些地方做得好？下次可以在哪些方面改进？"
    )
    
    # 额外的测试相关字段
    test_type: TestType = Field(default=TestType.UNIT, description="测试类型")
    test_result: TestResult = Field(default=TestResult.PASSED, description="测试结果")
    execution_time: float = Field(default=0.0, description="执行时间（秒）")
    confidence_score: float = Field(default=1.0, description="置信度分数")
    tags: List[str] = Field(default_factory=list, description="标签")
    timestamp: datetime = Field(default_factory=datetime.now, description="记录时间")

class TestExecutionMemory(BaseModel):
    """测试用例执行记忆模型"""
    
    test_case_id: str = Field(..., description="测试用例ID")
    test_name: str = Field(..., description="测试用例名称")
    execution_context: str = Field(..., description="测试执行的环境和条件")
    test_strategy: str = Field(..., description="采用的测试策略和方法")
    discovered_issues: str = Field(..., description="发现的问题和异常")
    optimization_insights: str = Field(..., description="可以改进的地方")
    
    # 执行详情
    test_type: TestType = Field(default=TestType.UNIT, description="测试类型")
    test_result: TestResult = Field(..., description="测试结果")
    execution_time: float = Field(..., description="执行时间（秒）")
    resource_usage: Dict[str, Any] = Field(default_factory=dict, description="资源使用情况")
    
    # 元数据
    environment: str = Field(default="development", description="测试环境")
    version: str = Field(default="1.0.0", description="被测试版本")
    tester: str = Field(default="AI Agent", description="测试执行者")
    timestamp: datetime = Field(default_factory=datetime.now, description="执行时间")

class ErrorHandlingMemory(BaseModel):
    """错误处理经验记忆模型"""
    
    error_type: ErrorType = Field(..., description="错误类型")
    error_message: str = Field(..., description="错误消息")
    context: str = Field(..., description="错误发生的上下文")
    solution_approach: str = Field(..., description="采用的解决方案")
    effectiveness: str = Field(..., description="解决方案的效果评估")
    
    # 错误详情
    stack_trace: Optional[str] = Field(default=None, description="堆栈跟踪")
    reproduction_steps: List[str] = Field(default_factory=list, description="重现步骤")
    workaround: Optional[str] = Field(default=None, description="临时解决方案")
    
    # 解决信息
    resolution_time: float = Field(default=0.0, description="解决时间（分钟）")
    retry_count: int = Field(default=0, description="重试次数")
    success_rate: float = Field(default=0.0, description="解决成功率")
    
    # 元数据
    severity: str = Field(default="medium", description="严重程度")
    frequency: int = Field(default=1, description="出现频率")
    timestamp: datetime = Field(default_factory=datetime.now, description="记录时间")

class TestContextMemory(BaseModel):
    """测试上下文记忆模型"""

    context_type: str = Field(..., description="上下文类型")
    context_data: Dict[str, Any] = Field(..., description="上下文数据")
    description: str = Field(..., description="上下文描述")

    # 项目信息
    project_name: str = Field(default="unknown", description="项目名称")
    module_name: str = Field(default="unknown", description="模块名称")

    # 配置信息
    test_environment: Dict[str, Any] = Field(default_factory=dict, description="测试环境配置")
    user_preferences: Dict[str, Any] = Field(default_factory=dict, description="用户偏好设置")

    # 历史信息
    usage_count: int = Field(default=1, description="使用次数")
    last_used: datetime = Field(default_factory=datetime.now, description="最后使用时间")
    effectiveness_score: float = Field(default=1.0, description="有效性评分")

    # 元数据
    tags: List[str] = Field(default_factory=list, description="标签")
    timestamp: datetime = Field(default_factory=datetime.now, description="创建时间")

class TestRecommendation(BaseModel):
    """测试推荐模型"""

    recommendation_id: str = Field(..., description="推荐ID")
    test_case_suggestion: str = Field(..., description="推荐的测试用例")
    reasoning: str = Field(..., description="推荐理由")
    confidence: float = Field(..., description="推荐置信度")

    # 推荐基础
    based_on_memories: List[str] = Field(default_factory=list, description="基于的记忆ID")
    similarity_score: float = Field(default=0.0, description="相似度分数")

    # 预期效果
    expected_coverage: float = Field(default=0.0, description="预期覆盖率")
    expected_issues: int = Field(default=0, description="预期发现问题数")

    # 元数据
    priority: str = Field(default="medium", description="优先级")
    estimated_time: float = Field(default=0.0, description="预估执行时间")
    timestamp: datetime = Field(default_factory=datetime.now, description="推荐时间")

class TestStrategy(BaseModel):
    """测试策略模型"""

    strategy_id: str = Field(..., description="策略ID")
    strategy_name: str = Field(..., description="策略名称")
    strategy_description: str = Field(..., description="策略描述")

    # 策略参数
    parameters: Dict[str, Any] = Field(default_factory=dict, description="策略参数")
    conditions: List[str] = Field(default_factory=list, description="适用条件")

    # 历史表现
    success_rate: float = Field(default=0.0, description="成功率")
    average_execution_time: float = Field(default=0.0, description="平均执行时间")
    issue_detection_rate: float = Field(default=0.0, description="问题检测率")

    # 使用统计
    usage_count: int = Field(default=0, description="使用次数")
    last_used: datetime = Field(default_factory=datetime.now, description="最后使用时间")

    # 元数据
    created_by: str = Field(default="AI Agent", description="创建者")
    version: str = Field(default="1.0.0", description="策略版本")
    timestamp: datetime = Field(default_factory=datetime.now, description="创建时间")