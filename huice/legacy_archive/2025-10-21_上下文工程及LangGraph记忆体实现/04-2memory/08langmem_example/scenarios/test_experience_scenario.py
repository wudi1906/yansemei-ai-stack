"""
测试经验积累与学习场景演示

演示如何使用记忆体功能来积累测试经验并从中学习，
基于Episode模式记录测试过程中的观察、思考、行动和结果。
"""

import time
import random
from typing import List, Dict, Any
from datetime import datetime

from ..memory_manager import TestingMemoryManager
from ..models import TestExperienceEpisode, TestType, TestResult
from ..config import DEFAULT_CONFIG

class TestExperienceScenario:
    """测试经验积累与学习场景"""
    
    def __init__(self, memory_manager: TestingMemoryManager = None):
        """初始化场景"""
        self.memory_manager = memory_manager or TestingMemoryManager(DEFAULT_CONFIG)
        self.scenario_name = "测试经验积累与学习"
        
    def run_demo(self):
        """运行完整的演示"""
        print(f"\n{'='*60}")
        print(f"🧠 {self.scenario_name} 场景演示")
        print(f"{'='*60}")
        
        # 1. 模拟多个测试经验的积累
        print("\n📚 第一阶段：积累测试经验")
        self._accumulate_test_experiences()
        
        # 2. 基于历史经验进行新的测试
        print("\n🔍 第二阶段：基于经验进行智能测试")
        self._intelligent_testing_with_memory()
        
        # 3. 展示学习效果
        print("\n📊 第三阶段：展示学习效果")
        self._demonstrate_learning_effects()
        
        print(f"\n✅ {self.scenario_name} 演示完成！")
    
    def _accumulate_test_experiences(self):
        """积累测试经验"""
        
        # 经验1：单元测试经验
        experience1 = TestExperienceEpisode(
            observation="对用户登录功能进行单元测试，需要验证各种输入情况",
            thoughts="我需要考虑正常登录、错误密码、不存在用户、空输入等多种情况。"
                     "特别要注意边界条件和异常处理。",
            action="我设计了包含10个测试用例的测试套件，覆盖了正常流程、异常流程和边界条件。"
                  "使用了参数化测试来提高效率。",
            result="测试发现了3个bug：密码为空时系统崩溃、用户名过长时截断错误、"
                  "连续失败登录没有锁定机制。下次应该更早考虑安全性测试。",
            test_type=TestType.UNIT,
            test_result=TestResult.PASSED,
            execution_time=45.5,
            confidence_score=0.9,
            tags=["登录", "单元测试", "边界条件", "安全性"]
        )
        
        memory_id1 = self.memory_manager.store_experience(experience1)
        print(f"✅ 存储单元测试经验: {memory_id1[:8]}...")
        
        # 经验2：集成测试经验
        experience2 = TestExperienceEpisode(
            observation="测试用户注册流程的集成测试，涉及前端、后端、数据库的交互",
            thoughts="集成测试需要关注各个组件之间的数据流和状态同步。"
                     "我应该重点测试数据一致性和事务完整性。",
            action="我搭建了完整的测试环境，模拟了真实的用户操作流程，"
                  "包括表单提交、数据验证、邮件发送、数据库存储等步骤。",
            result="发现了数据库事务回滚机制有问题，邮件发送失败时用户数据仍然被保存。"
                  "学到了集成测试中事务边界的重要性。",
            test_type=TestType.INTEGRATION,
            test_result=TestResult.FAILED,
            execution_time=120.3,
            confidence_score=0.85,
            tags=["注册", "集成测试", "事务", "数据一致性"]
        )
        
        memory_id2 = self.memory_manager.store_experience(experience2)
        print(f"✅ 存储集成测试经验: {memory_id2[:8]}...")
        
        # 经验3：性能测试经验
        experience3 = TestExperienceEpisode(
            observation="对API接口进行性能测试，需要验证在高并发下的响应时间和稳定性",
            thoughts="性能测试不仅要看平均响应时间，还要关注99%分位数、错误率和资源使用情况。"
                     "需要逐步增加负载来找到系统的瓶颈点。",
            action="我使用了阶梯式加压策略，从10并发用户开始，每分钟增加10个用户，"
                  "直到系统响应时间超过2秒或错误率超过1%。同时监控CPU、内存、数据库连接数。",
            result="发现系统在150并发用户时开始出现性能瓶颈，主要是数据库连接池不足。"
                  "优化连接池配置后，可以支持300并发用户。学会了性能调优的重要性。",
            test_type=TestType.PERFORMANCE,
            test_result=TestResult.PASSED,
            execution_time=300.7,
            confidence_score=0.95,
            tags=["性能测试", "并发", "数据库", "连接池", "调优"]
        )
        
        memory_id3 = self.memory_manager.store_experience(experience3)
        print(f"✅ 存储性能测试经验: {memory_id3[:8]}...")
        
        # 经验4：UI测试经验
        experience4 = TestExperienceEpisode(
            observation="对购物车功能进行UI自动化测试，需要验证各种用户交互场景",
            thoughts="UI测试容易受到页面加载时间和元素定位的影响。"
                     "我需要添加合适的等待机制和稳定的元素定位策略。",
            action="我使用了Page Object模式组织测试代码，添加了显式等待和重试机制，"
                  "测试了添加商品、修改数量、删除商品、清空购物车等功能。",
            result="测试通过率达到95%，但发现在网络较慢时偶尔会超时失败。"
                  "学到了UI测试中稳定性比速度更重要，需要充分考虑网络延迟。",
            test_type=TestType.UI,
            test_result=TestResult.PASSED,
            execution_time=180.2,
            confidence_score=0.88,
            tags=["UI测试", "购物车", "自动化", "Page Object", "稳定性"]
        )
        
        memory_id4 = self.memory_manager.store_experience(experience4)
        print(f"✅ 存储UI测试经验: {memory_id4[:8]}...")
        
        print(f"\n📈 已积累 4 条测试经验记录")
    
    def _intelligent_testing_with_memory(self):
        """基于历史经验进行智能测试"""
        
        # 场景：需要测试一个新的支付功能
        test_scenario = "支付功能测试"
        print(f"\n🎯 当前测试场景: {test_scenario}")
        
        # 搜索相关的历史经验
        print("🔍 搜索相关历史经验...")
        related_experiences = self.memory_manager.search_experiences(
            query="用户 功能 测试 安全 事务",
            limit=3
        )
        
        print(f"📋 找到 {len(related_experiences)} 条相关经验:")
        for i, exp in enumerate(related_experiences, 1):
            content = exp.get('content', {})
            print(f"  {i}. {content.get('observation', 'N/A')[:50]}...")
            print(f"     关键学习: {content.get('result', 'N/A')[:60]}...")
        
        # 基于历史经验生成测试策略
        print("\n💡 基于历史经验生成测试策略:")
        strategy = self._generate_test_strategy(related_experiences)
        for i, point in enumerate(strategy, 1):
            print(f"  {i}. {point}")
        
        # 执行测试并记录新经验
        print("\n🚀 执行测试...")
        time.sleep(2)  # 模拟测试执行
        
        new_experience = TestExperienceEpisode(
            observation="对新的支付功能进行全面测试，包括多种支付方式和异常情况",
            thoughts="基于之前的经验，我特别关注了事务完整性、安全性验证和用户体验。"
                     "支付功能涉及金钱，安全性是最高优先级。",
            action="我设计了包含正常支付、支付失败、网络中断、重复支付等场景的测试用例。"
                  "特别加强了对事务回滚和数据一致性的验证。",
            result="发现了支付超时后的状态不一致问题，用户账户已扣款但订单状态未更新。"
                  "通过之前的经验，快速定位到事务边界问题并提出了解决方案。",
            test_type=TestType.INTEGRATION,
            test_result=TestResult.FAILED,
            execution_time=95.8,
            confidence_score=0.92,
            tags=["支付", "安全性", "事务", "数据一致性", "经验应用"]
        )
        
        memory_id = self.memory_manager.store_experience(new_experience)
        print(f"✅ 新经验已记录: {memory_id[:8]}...")
    
    def _generate_test_strategy(self, experiences: List[Dict[str, Any]]) -> List[str]:
        """基于历史经验生成测试策略"""
        strategy = [
            "🔒 重点关注安全性测试，特别是输入验证和权限控制",
            "🔄 加强事务完整性测试，确保数据一致性",
            "⚡ 进行性能测试，验证高并发下的稳定性",
            "🎯 设计边界条件测试用例，覆盖异常情况",
            "🔍 添加充分的等待和重试机制，提高测试稳定性"
        ]
        
        # 根据历史经验调整策略
        for exp in experiences:
            content = exp.get('content', {})
            result = content.get('result', '')
            if '事务' in result:
                strategy.append("📊 特别验证事务回滚机制")
            if '安全' in result:
                strategy.append("🛡️ 增加安全性测试用例")
            if '性能' in result:
                strategy.append("📈 监控系统资源使用情况")
        
        return strategy
    
    def _demonstrate_learning_effects(self):
        """展示学习效果"""
        
        print("\n📊 记忆体统计信息:")
        stats = self.memory_manager.get_memory_stats()
        for memory_type, count in stats.items():
            print(f"  📁 {memory_type}: {count} 条记录")
        
        print("\n🎯 学习效果分析:")
        
        # 分析测试类型分布
        all_experiences = self.memory_manager.search_experiences("", limit=100)
        test_types = {}
        avg_confidence = 0
        total_time = 0
        
        for exp in all_experiences:
            content = exp.get('content', {})
            test_type = content.get('test_type', 'unknown')
            test_types[test_type] = test_types.get(test_type, 0) + 1
            avg_confidence += content.get('confidence_score', 0)
            total_time += content.get('execution_time', 0)
        
        if all_experiences:
            avg_confidence /= len(all_experiences)
            
        print(f"  📈 测试类型分布: {test_types}")
        print(f"  🎯 平均置信度: {avg_confidence:.2f}")
        print(f"  ⏱️ 总执行时间: {total_time:.1f} 秒")
        
        print("\n💡 关键学习点:")
        learning_points = [
            "🔄 事务完整性在集成测试中至关重要",
            "🔒 安全性测试应该贯穿整个测试过程",
            "⚡ 性能测试需要关注资源瓶颈",
            "🎯 UI测试的稳定性比速度更重要",
            "📊 历史经验可以指导新的测试策略"
        ]
        
        for point in learning_points:
            print(f"  {point}")

def run_test_experience_demo():
    """运行测试经验场景演示"""
    scenario = TestExperienceScenario()
    scenario.run_demo()

if __name__ == "__main__":
    run_test_experience_demo()