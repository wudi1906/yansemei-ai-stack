"""
基础使用示例

演示测试记忆体功能的基本使用方法
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .. import (
    TestingMemoryManager,
    TestExperienceEpisode,
    TestExecutionMemory,
    ErrorHandlingMemory,
    TestContextMemory,
    TestType,
    TestResult,
    ErrorType
)

def basic_experience_usage():
    """基础测试经验使用示例"""
    print("🧠 基础测试经验使用示例")
    print("-" * 40)
    
    # 初始化记忆体管理器
    memory_manager = TestingMemoryManager()
    
    # 创建测试经验记录
    experience = TestExperienceEpisode(
        observation="对用户注册功能进行单元测试",
        thoughts="需要验证邮箱格式、密码强度、用户名唯一性等多个方面",
        action="设计了15个测试用例，包括正常流程和异常情况",
        result="发现了2个验证逻辑bug，测试覆盖率达到92%",
        test_type=TestType.UNIT,
        test_result=TestResult.PASSED,
        execution_time=65.3,
        confidence_score=0.91,
        tags=["用户注册", "单元测试", "验证逻辑"]
    )
    
    # 存储经验
    memory_id = memory_manager.store_experience(experience)
    print(f"✅ 存储测试经验: {memory_id[:8]}...")
    
    # 搜索相关经验
    print("\n🔍 搜索相关经验:")
    related_experiences = memory_manager.search_experiences(
        query="用户注册测试验证",
        limit=3
    )
    
    for i, exp in enumerate(related_experiences, 1):
        content = exp.get('content', {})
        print(f"  {i}. {content.get('observation', 'N/A')[:50]}...")
        print(f"     结果: {content.get('result', 'N/A')[:40]}...")

def basic_execution_usage():
    """基础测试执行记录使用示例"""
    print("\n🚀 基础测试执行记录使用示例")
    print("-" * 40)
    
    memory_manager = TestingMemoryManager()
    
    # 创建测试执行记录
    execution = TestExecutionMemory(
        test_case_id="TC_API_001",
        test_name="用户API接口测试",
        execution_context="在测试环境中对用户相关API进行功能和性能测试",
        test_strategy="采用边界值测试和等价类划分方法，重点验证参数验证和错误处理",
        discovered_issues="发现API在处理空参数时返回500错误而非400错误",
        optimization_insights="建议增加参数验证中间件，统一处理参数验证逻辑",
        test_type=TestType.INTEGRATION,
        test_result=TestResult.FAILED,
        execution_time=120.5,
        resource_usage={
            "cpu_usage": 25.3,
            "memory_usage": 256.7,
            "api_calls": 45
        },
        environment="testing",
        version="v1.3.2"
    )
    
    # 存储执行记录
    memory_id = memory_manager.store_execution(execution)
    print(f"✅ 存储执行记录: {memory_id[:8]}...")
    
    # 搜索相关执行记录
    print("\n🔍 搜索相关执行记录:")
    related_executions = memory_manager.search_executions(
        query="API测试接口",
        limit=2
    )
    
    for i, exec_record in enumerate(related_executions, 1):
        content = exec_record.get('content', {})
        print(f"  {i}. {content.get('test_name', 'N/A')}")
        print(f"     结果: {content.get('test_result', 'N/A')}")
        print(f"     执行时间: {content.get('execution_time', 0):.1f}秒")

def basic_error_usage():
    """基础错误处理记录使用示例"""
    print("\n🚨 基础错误处理记录使用示例")
    print("-" * 40)
    
    memory_manager = TestingMemoryManager()
    
    # 创建错误处理记录
    error = ErrorHandlingMemory(
        error_type=ErrorType.DATABASE_ERROR,
        error_message="Connection pool exhausted - Unable to acquire connection",
        context="在并发测试中，当并发用户数达到200时出现数据库连接池耗尽",
        solution_approach="增加数据库连接池大小从10调整到30，并添加连接池监控",
        effectiveness="解决方案有效，系统现在可以支持500并发用户",
        reproduction_steps=[
            "1. 设置并发用户数为200",
            "2. 执行用户登录压力测试",
            "3. 观察数据库连接池使用情况",
            "4. 等待连接池耗尽错误出现"
        ],
        resolution_time=90.0,
        success_rate=0.95,
        severity="high",
        frequency=3
    )
    
    # 存储错误记录
    memory_id = memory_manager.store_error(error)
    print(f"✅ 存储错误记录: {memory_id[:8]}...")
    
    # 搜索相关错误
    print("\n🔍 搜索相关错误:")
    related_errors = memory_manager.search_errors(
        query="数据库连接池",
        limit=2
    )
    
    for i, error_record in enumerate(related_errors, 1):
        content = error_record.get('content', {})
        print(f"  {i}. 错误类型: {content.get('error_type', 'N/A')}")
        print(f"     解决成功率: {content.get('success_rate', 0):.1%}")
        print(f"     解决时间: {content.get('resolution_time', 0):.0f}分钟")

def basic_context_usage():
    """基础上下文记录使用示例"""
    print("\n🗂️ 基础上下文记录使用示例")
    print("-" * 40)
    
    memory_manager = TestingMemoryManager()
    
    # 创建上下文记录
    context = TestContextMemory(
        context_type="project_config",
        context_data={
            "database": {
                "host": "test-db.company.com",
                "port": 5432,
                "database": "test_app"
            },
            "api_base_url": "https://api-test.company.com",
            "test_users": ["test_user_1", "test_user_2", "admin_user"]
        },
        description="电商项目的测试环境配置信息",
        project_name="E-commerce Platform",
        module_name="user_management",
        test_environment={
            "os": "Ubuntu 20.04",
            "python_version": "3.9.7",
            "test_framework": "pytest"
        },
        tags=["电商", "用户管理", "测试环境"]
    )
    
    # 存储上下文
    memory_id = memory_manager.store_context(context)
    print(f"✅ 存储上下文记录: {memory_id[:8]}...")
    
    # 搜索相关上下文
    print("\n🔍 搜索相关上下文:")
    related_contexts = memory_manager.search_contexts(
        query="项目配置测试环境",
        limit=2
    )
    
    for i, ctx_record in enumerate(related_contexts, 1):
        content = ctx_record.get('content', {})
        print(f"  {i}. 项目: {content.get('project_name', 'N/A')}")
        print(f"     类型: {content.get('context_type', 'N/A')}")
        print(f"     描述: {content.get('description', 'N/A')[:40]}...")

def memory_statistics_example():
    """记忆体统计示例"""
    print("\n📊 记忆体统计示例")
    print("-" * 40)
    
    memory_manager = TestingMemoryManager()
    
    # 获取统计信息
    stats = memory_manager.get_memory_stats()
    
    print("📈 记忆体统计信息:")
    total_memories = 0
    for memory_type, count in stats.items():
        print(f"  📁 {memory_type}: {count} 条记录")
        total_memories += count
    
    print(f"\n📊 总记忆体数量: {total_memories}")
    
    # 导出记忆体数据示例
    print("\n💾 导出记忆体数据示例:")
    exported_data = memory_manager.export_memories("test_experiences")
    if exported_data:
        print(f"  📤 导出经验数据: {exported_data.get('count', 0)} 条记录")
    else:
        print("  📤 暂无经验数据可导出")

def search_optimization_example():
    """搜索优化示例"""
    print("\n🔍 搜索优化示例")
    print("-" * 40)
    
    memory_manager = TestingMemoryManager()
    
    # 不同类型的搜索示例
    search_examples = [
        {
            "query": "用户登录测试",
            "description": "搜索用户登录相关的测试经验"
        },
        {
            "query": "性能测试 API 响应时间",
            "description": "搜索API性能测试相关记录"
        },
        {
            "query": "数据库连接错误",
            "description": "搜索数据库连接相关的错误处理经验"
        },
        {
            "query": "项目配置 测试环境",
            "description": "搜索项目配置和测试环境相关的上下文"
        }
    ]
    
    for example in search_examples:
        print(f"\n🎯 {example['description']}:")
        print(f"   查询: '{example['query']}'")
        
        # 搜索经验
        experiences = memory_manager.search_experiences(example['query'], limit=1)
        if experiences:
            content = experiences[0].get('content', {})
            print(f"   结果: {content.get('observation', 'N/A')[:50]}...")
        else:
            print("   结果: 暂无相关记录")

def main():
    """主函数"""
    print("🎯 测试记忆体功能基础使用示例")
    print("=" * 60)
    
    try:
        # 运行各种基础使用示例
        basic_experience_usage()
        basic_execution_usage()
        basic_error_usage()
        basic_context_usage()
        memory_statistics_example()
        search_optimization_example()
        
        print("\n✅ 所有基础使用示例运行完成！")
        print("\n💡 提示:")
        print("  - 这些示例展示了记忆体功能的基本用法")
        print("  - 实际使用中可以根据需要调整参数和配置")
        print("  - 建议查看完整的演示脚本了解更多高级功能")
        
    except Exception as e:
        print(f"\n❌ 示例运行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()