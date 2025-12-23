"""
测试上下文记忆场景演示

演示如何使用记忆体功能来保存和利用测试上下文信息，
包括项目配置、用户偏好、历史测试结果等。
"""

import time
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta

from ..memory_manager import TestingMemoryManager
from ..models import TestContextMemory
from ..config import DEFAULT_CONFIG

class TestContextScenario:
    """测试上下文记忆场景"""
    
    def __init__(self, memory_manager: TestingMemoryManager = None):
        """初始化场景"""
        self.memory_manager = memory_manager or TestingMemoryManager(DEFAULT_CONFIG)
        self.scenario_name = "测试上下文记忆"
        
    def run_demo(self):
        """运行完整的演示"""
        print(f"\n{'='*60}")
        print(f"🗂️ {self.scenario_name} 场景演示")
        print(f"{'='*60}")
        
        # 1. 保存项目配置上下文
        print("\n📁 第一阶段：保存项目配置上下文")
        self._save_project_contexts()
        
        # 2. 保存用户偏好上下文
        print("\n👤 第二阶段：保存用户偏好上下文")
        self._save_user_preferences()
        
        # 3. 保存历史测试结果上下文
        print("\n📊 第三阶段：保存历史测试结果上下文")
        self._save_historical_results()
        
        # 4. 智能上下文检索和应用
        print("\n🧠 第四阶段：智能上下文检索和应用")
        self._intelligent_context_usage()
        
        # 5. 上下文演化和优化
        print("\n🔄 第五阶段：上下文演化和优化")
        self._context_evolution()
        
        print(f"\n✅ {self.scenario_name} 演示完成！")
    
    def _save_project_contexts(self):
        """保存项目配置上下文"""
        
        # 项目A的测试环境配置
        project_a_config = TestContextMemory(
            context_type="project_config",
            context_data={
                "database": {
                    "host": "test-db-a.company.com",
                    "port": 5432,
                    "database": "test_app_a",
                    "connection_pool_size": 20
                },
                "api_endpoints": {
                    "base_url": "https://api-test-a.company.com",
                    "timeout": 30,
                    "retry_count": 3
                },
                "test_data": {
                    "user_accounts": ["test_user_1", "test_user_2", "admin_user"],
                    "test_products": ["product_001", "product_002"],
                    "payment_methods": ["credit_card", "paypal", "bank_transfer"]
                }
            },
            description="项目A的测试环境配置，包括数据库、API和测试数据设置",
            project_name="E-commerce Platform A",
            module_name="core_services",
            test_environment={
                "os": "Ubuntu 20.04",
                "python_version": "3.9.7",
                "browser": "Chrome 96.0",
                "test_framework": "pytest"
            },
            tags=["项目A", "电商平台", "核心服务", "测试环境"]
        )
        
        memory_id1 = self.memory_manager.store_context(project_a_config)
        print(f"✅ 保存项目A配置: {memory_id1[:8]}...")
        
        # 项目B的测试环境配置
        project_b_config = TestContextMemory(
            context_type="project_config",
            context_data={
                "microservices": {
                    "user_service": "http://user-service-test:8080",
                    "order_service": "http://order-service-test:8081",
                    "payment_service": "http://payment-service-test:8082"
                },
                "message_queue": {
                    "broker": "rabbitmq-test.company.com",
                    "port": 5672,
                    "virtual_host": "/test"
                },
                "monitoring": {
                    "prometheus": "http://prometheus-test:9090",
                    "grafana": "http://grafana-test:3000"
                }
            },
            description="项目B的微服务测试环境配置，包括服务地址和监控设置",
            project_name="Microservices Platform B",
            module_name="distributed_services",
            test_environment={
                "container_runtime": "Docker",
                "orchestration": "Kubernetes",
                "service_mesh": "Istio",
                "test_framework": "testcontainers"
            },
            tags=["项目B", "微服务", "分布式", "容器化"]
        )
        
        memory_id2 = self.memory_manager.store_context(project_b_config)
        print(f"✅ 保存项目B配置: {memory_id2[:8]}...")
        
        print(f"📁 已保存 2 个项目配置上下文")
    
    def _save_user_preferences(self):
        """保存用户偏好上下文"""
        
        # 测试工程师Alice的偏好
        alice_preferences = TestContextMemory(
            context_type="user_preferences",
            context_data={
                "testing_style": {
                    "preferred_test_types": ["unit", "integration"],
                    "test_coverage_threshold": 85,
                    "code_review_strictness": "high",
                    "documentation_level": "detailed"
                },
                "tools_preferences": {
                    "ide": "PyCharm",
                    "test_runner": "pytest",
                    "coverage_tool": "coverage.py",
                    "reporting_format": "html"
                },
                "notification_settings": {
                    "email_on_failure": True,
                    "slack_integration": True,
                    "daily_summary": True
                },
                "work_schedule": {
                    "timezone": "UTC+8",
                    "working_hours": "09:00-18:00",
                    "preferred_test_time": "morning"
                }
            },
            description="测试工程师Alice的个人偏好设置",
            project_name="multiple",
            user_preferences={
                "user_id": "alice_chen",
                "role": "senior_test_engineer",
                "experience_years": 5,
                "specialization": ["API测试", "性能测试", "自动化测试"]
            },
            tags=["Alice", "高级测试工程师", "API测试", "性能测试"]
        )
        
        memory_id1 = self.memory_manager.store_context(alice_preferences)
        print(f"✅ 保存Alice偏好设置: {memory_id1[:8]}...")
        
        # 测试工程师Bob的偏好
        bob_preferences = TestContextMemory(
            context_type="user_preferences",
            context_data={
                "testing_style": {
                    "preferred_test_types": ["ui", "e2e"],
                    "test_coverage_threshold": 75,
                    "automation_priority": "high",
                    "manual_testing_ratio": 20
                },
                "tools_preferences": {
                    "ide": "VS Code",
                    "test_framework": "Selenium",
                    "ci_cd_tool": "Jenkins",
                    "bug_tracking": "Jira"
                },
                "reporting_preferences": {
                    "screenshot_on_failure": True,
                    "video_recording": True,
                    "detailed_logs": True
                }
            },
            description="测试工程师Bob的个人偏好设置，专注于UI和端到端测试",
            project_name="multiple",
            user_preferences={
                "user_id": "bob_wang",
                "role": "ui_test_specialist",
                "experience_years": 3,
                "specialization": ["UI测试", "端到端测试", "移动端测试"]
            },
            tags=["Bob", "UI测试专家", "端到端测试", "移动端"]
        )
        
        memory_id2 = self.memory_manager.store_context(bob_preferences)
        print(f"✅ 保存Bob偏好设置: {memory_id2[:8]}...")
        
        print(f"👤 已保存 2 个用户偏好上下文")
    
    def _save_historical_results(self):
        """保存历史测试结果上下文"""
        
        # 上周的测试结果汇总
        last_week_results = TestContextMemory(
            context_type="historical_results",
            context_data={
                "test_summary": {
                    "total_tests": 1250,
                    "passed": 1180,
                    "failed": 45,
                    "skipped": 25,
                    "success_rate": 94.4
                },
                "performance_metrics": {
                    "average_execution_time": 125.5,
                    "slowest_test": "test_large_data_processing",
                    "fastest_test": "test_user_validation",
                    "timeout_count": 3
                },
                "failure_analysis": {
                    "network_issues": 15,
                    "database_timeouts": 12,
                    "ui_element_not_found": 8,
                    "assertion_errors": 10
                },
                "coverage_data": {
                    "line_coverage": 87.2,
                    "branch_coverage": 82.5,
                    "function_coverage": 91.8
                }
            },
            description="上周测试执行结果的详细汇总分析",
            project_name="E-commerce Platform A",
            test_environment={
                "test_period": "2024-01-08 to 2024-01-14",
                "environment": "staging",
                "build_version": "v2.3.1"
            },
            effectiveness_score=0.94,
            tags=["历史结果", "周报", "性能分析", "失败分析"]
        )
        
        memory_id1 = self.memory_manager.store_context(last_week_results)
        print(f"✅ 保存上周测试结果: {memory_id1[:8]}...")
        
        # 性能基线数据
        performance_baseline = TestContextMemory(
            context_type="performance_baseline",
            context_data={
                "api_response_times": {
                    "user_login": {"p50": 120, "p95": 250, "p99": 400},
                    "product_search": {"p50": 80, "p95": 180, "p99": 300},
                    "order_creation": {"p50": 200, "p95": 450, "p99": 800},
                    "payment_processing": {"p50": 300, "p95": 600, "p99": 1200}
                },
                "database_metrics": {
                    "connection_pool_usage": 65,
                    "query_execution_time": {"avg": 45, "max": 200},
                    "deadlock_count": 0,
                    "slow_query_count": 3
                },
                "system_resources": {
                    "cpu_usage": {"avg": 35, "peak": 78},
                    "memory_usage": {"avg": 2.1, "peak": 3.8},
                    "disk_io": {"read": 150, "write": 80}
                }
            },
            description="系统性能基线数据，用于性能回归测试对比",
            project_name="E-commerce Platform A",
            test_environment={
                "baseline_date": "2024-01-01",
                "load_level": "normal_traffic",
                "measurement_duration": "24_hours"
            },
            effectiveness_score=1.0,
            tags=["性能基线", "API响应时间", "数据库性能", "系统资源"]
        )
        
        memory_id2 = self.memory_manager.store_context(performance_baseline)
        print(f"✅ 保存性能基线数据: {memory_id2[:8]}...")
        
        print(f"📊 已保存 2 个历史结果上下文")
    
    def _intelligent_context_usage(self):
        """智能上下文检索和应用"""
        
        print("\n🎯 场景：为新项目设置测试环境")
        
        # 搜索相关的项目配置
        print("🔍 搜索相关项目配置...")
        project_contexts = self.memory_manager.search_contexts(
            query="项目 配置 数据库 API 测试环境",
            limit=3
        )
        
        print(f"📋 找到 {len(project_contexts)} 个相关配置:")
        for i, ctx in enumerate(project_contexts, 1):
            content = ctx.get('content', {})
            print(f"  {i}. {content.get('description', 'N/A')}")
            print(f"     项目: {content.get('project_name', 'N/A')}")
        
        # 搜索用户偏好
        print("\n🔍 搜索用户偏好设置...")
        user_contexts = self.memory_manager.search_contexts(
            query="用户 偏好 测试 工具",
            limit=2
        )
        
        print(f"👤 找到 {len(user_contexts)} 个用户偏好:")
        for i, ctx in enumerate(user_contexts, 1):
            content = ctx.get('content', {})
            user_prefs = content.get('user_preferences', {})
            print(f"  {i}. 用户: {user_prefs.get('user_id', 'N/A')}")
            print(f"     角色: {user_prefs.get('role', 'N/A')}")
            print(f"     专长: {user_prefs.get('specialization', [])}")
        
        # 基于上下文生成配置建议
        print("\n💡 基于历史上下文生成配置建议:")
        suggestions = self._generate_config_suggestions(project_contexts, user_contexts)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    
    def _generate_config_suggestions(self, project_contexts: List[Dict], user_contexts: List[Dict]) -> List[str]:
        """基于上下文生成配置建议"""
        suggestions = []
        
        # 基于项目配置历史
        if project_contexts:
            suggestions.append("🗄️ 建议使用PostgreSQL数据库，连接池大小设置为20")
            suggestions.append("🌐 API超时时间建议设置为30秒，重试次数3次")
            suggestions.append("🐳 考虑使用容器化部署，便于环境一致性")
        
        # 基于用户偏好
        if user_contexts:
            suggestions.append("🔧 推荐使用pytest作为测试框架")
            suggestions.append("📊 设置测试覆盖率阈值为80%以上")
            suggestions.append("📧 配置测试失败时的邮件通知")
        
        suggestions.extend([
            "📈 建立性能基线，定期进行回归测试",
            "🔄 设置CI/CD流水线自动执行测试",
            "📝 配置详细的测试报告和日志记录"
        ])
        
        return suggestions
    
    def _context_evolution(self):
        """上下文演化和优化"""
        
        print("\n🔄 上下文使用情况分析:")
        
        # 模拟上下文使用统计
        usage_stats = {
            "project_config": {"usage_count": 15, "effectiveness": 0.92},
            "user_preferences": {"usage_count": 8, "effectiveness": 0.88},
            "historical_results": {"usage_count": 12, "effectiveness": 0.95},
            "performance_baseline": {"usage_count": 6, "effectiveness": 0.90}
        }
        
        for context_type, stats in usage_stats.items():
            print(f"  📁 {context_type}:")
            print(f"     使用次数: {stats['usage_count']}")
            print(f"     有效性: {stats['effectiveness']:.2%}")
        
        print("\n🎯 上下文优化建议:")
        optimization_suggestions = [
            "📈 project_config 使用频率最高，建议增加更多项目模板",
            "🎯 historical_results 有效性最高，建议扩展历史数据收集",
            "👤 user_preferences 可以增加更多个性化选项",
            "⚡ performance_baseline 建议定期更新基线数据",
            "🔍 建议添加上下文自动推荐功能",
            "🗂️ 考虑实现上下文版本管理和回滚功能"
        ]
        
        for suggestion in optimization_suggestions:
            print(f"  {suggestion}")
        
        print("\n📊 上下文记忆体统计:")
        stats = self.memory_manager.get_memory_stats()
        context_count = stats.get('test_contexts', 0)
        print(f"  📁 总上下文数量: {context_count}")
        print(f"  🔄 平均使用频率: {sum(s['usage_count'] for s in usage_stats.values()) / len(usage_stats):.1f}")
        print(f"  ⭐ 平均有效性: {sum(s['effectiveness'] for s in usage_stats.values()) / len(usage_stats):.2%}")

def run_test_context_demo():
    """运行测试上下文场景演示"""
    scenario = TestContextScenario()
    scenario.run_demo()

if __name__ == "__main__":
    run_test_context_demo()