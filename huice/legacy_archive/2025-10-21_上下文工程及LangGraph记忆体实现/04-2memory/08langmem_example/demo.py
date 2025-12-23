"""
测试记忆体功能综合演示脚本

这个脚本演示了所有测试记忆体功能场景，包括：
1. 测试经验积累与学习
2. 测试上下文记忆
3. 测试用例执行记忆
4. 错误处理经验记忆
5. 智能测试用例推荐
6. 自适应测试策略

运行方式：
python demo.py [--scenario SCENARIO_NAME] [--all] [--interactive]
"""

import sys
import argparse
import time
from typing import Optional

from .memory_manager import TestingMemoryManager
from .config import DEFAULT_CONFIG, validate_config
from .scenarios import (
    TestExperienceScenario,
    TestContextScenario,
    TestExecutionScenario,
    ErrorHandlingScenario,
    SmartRecommendationScenario,
    AdaptiveStrategyScenario
)

class TestingMemoryDemo:
    """测试记忆体功能综合演示"""
    
    def __init__(self):
        """初始化演示"""
        print("🚀 初始化测试记忆体演示系统...")
        
        # 验证配置
        if not validate_config(DEFAULT_CONFIG):
            print("❌ 配置验证失败，请检查配置文件")
            sys.exit(1)
        
        # 初始化记忆体管理器
        self.memory_manager = TestingMemoryManager(DEFAULT_CONFIG)
        
        # 初始化所有场景
        self.scenarios = {
            "experience": TestExperienceScenario(self.memory_manager),
            "context": TestContextScenario(self.memory_manager),
            "execution": TestExecutionScenario(self.memory_manager),
            "error": ErrorHandlingScenario(self.memory_manager),
            "recommendation": SmartRecommendationScenario(self.memory_manager),
            "adaptive": AdaptiveStrategyScenario(self.memory_manager)
        }
        
        print("✅ 演示系统初始化完成！")
    
    def run_all_scenarios(self):
        """运行所有场景演示"""
        print(f"\n{'='*80}")
        print("🎭 测试记忆体功能全场景演示")
        print(f"{'='*80}")
        
        scenario_order = [
            ("experience", "测试经验积累与学习"),
            ("context", "测试上下文记忆"),
            ("execution", "测试用例执行记忆"),
            ("error", "错误处理经验记忆"),
            ("recommendation", "智能测试用例推荐"),
            ("adaptive", "自适应测试策略")
        ]
        
        total_scenarios = len(scenario_order)
        
        for i, (scenario_key, scenario_name) in enumerate(scenario_order, 1):
            print(f"\n🎬 [{i}/{total_scenarios}] 开始演示: {scenario_name}")
            print("-" * 60)
            
            try:
                self.scenarios[scenario_key].run_demo()
                print(f"✅ [{i}/{total_scenarios}] {scenario_name} 演示完成")
            except Exception as e:
                print(f"❌ [{i}/{total_scenarios}] {scenario_name} 演示失败: {e}")
            
            # 场景间暂停
            if i < total_scenarios:
                print("\n⏸️ 暂停3秒，准备下一个场景...")
                time.sleep(3)
        
        # 显示总结
        self._show_demo_summary()
    
    def run_single_scenario(self, scenario_name: str):
        """运行单个场景演示"""
        if scenario_name not in self.scenarios:
            print(f"❌ 未知场景: {scenario_name}")
            print(f"可用场景: {list(self.scenarios.keys())}")
            return
        
        print(f"\n🎬 开始单场景演示: {scenario_name}")
        print("-" * 60)
        
        try:
            self.scenarios[scenario_name].run_demo()
            print(f"✅ {scenario_name} 场景演示完成")
        except Exception as e:
            print(f"❌ {scenario_name} 场景演示失败: {e}")
    
    def run_interactive_demo(self):
        """运行交互式演示"""
        print(f"\n{'='*60}")
        print("🎮 交互式测试记忆体演示")
        print(f"{'='*60}")
        
        while True:
            print("\n📋 可用的演示场景:")
            scenarios_info = [
                ("1", "experience", "测试经验积累与学习"),
                ("2", "context", "测试上下文记忆"),
                ("3", "execution", "测试用例执行记忆"),
                ("4", "error", "错误处理经验记忆"),
                ("5", "recommendation", "智能测试用例推荐"),
                ("6", "adaptive", "自适应测试策略"),
                ("7", "all", "运行所有场景"),
                ("8", "stats", "查看记忆体统计"),
                ("0", "exit", "退出演示")
            ]
            
            for num, key, name in scenarios_info:
                print(f"  {num}. {name}")
            
            choice = input("\n请选择要演示的场景 (输入数字): ").strip()
            
            if choice == "0":
                print("👋 感谢使用测试记忆体演示系统！")
                break
            elif choice == "7":
                self.run_all_scenarios()
            elif choice == "8":
                self._show_memory_stats()
            elif choice in ["1", "2", "3", "4", "5", "6"]:
                scenario_map = {
                    "1": "experience",
                    "2": "context", 
                    "3": "execution",
                    "4": "error",
                    "5": "recommendation",
                    "6": "adaptive"
                }
                self.run_single_scenario(scenario_map[choice])
            else:
                print("❌ 无效选择，请重新输入")
            
            input("\n按回车键继续...")
    
    def _show_memory_stats(self):
        """显示记忆体统计信息"""
        print(f"\n{'='*50}")
        print("📊 记忆体统计信息")
        print(f"{'='*50}")
        
        stats = self.memory_manager.get_memory_stats()
        
        print("📈 各类型记忆体数量:")
        total_memories = 0
        for memory_type, count in stats.items():
            print(f"  📁 {memory_type}: {count} 条记录")
            total_memories += count
        
        print(f"\n📊 总记忆体数量: {total_memories}")
        
        # 显示配置信息
        print(f"\n⚙️ 系统配置:")
        config_dict = self.memory_manager.config.to_dict()
        key_configs = [
            "model_name",
            "embedding_model", 
            "max_memory_items",
            "memory_search_limit",
            "confidence_threshold"
        ]
        
        for key in key_configs:
            if key in config_dict:
                print(f"  🔧 {key}: {config_dict[key]}")
    
    def _show_demo_summary(self):
        """显示演示总结"""
        print(f"\n{'='*80}")
        print("🎉 测试记忆体功能演示总结")
        print(f"{'='*80}")
        
        summary_points = [
            "✅ 测试经验积累：演示了如何记录和学习测试经验，提高测试效率",
            "🗂️ 上下文记忆：展示了项目配置、用户偏好等上下文信息的智能管理",
            "🚀 执行记忆：演示了测试执行过程的记录和优化策略生成",
            "🚨 错误处理：展示了错误经验的积累和智能诊断推荐功能",
            "🎯 智能推荐：演示了基于历史数据的测试用例智能推荐系统",
            "🧠 自适应策略：展示了根据历史表现自动调整测试策略的能力"
        ]
        
        print("\n📋 演示内容回顾:")
        for point in summary_points:
            print(f"  {point}")
        
        print("\n💡 关键收获:")
        key_insights = [
            "🔄 记忆体功能能显著提高测试智能化水平",
            "📈 历史经验的积累和应用能减少重复性工作",
            "🎯 智能推荐系统能提高测试用例的针对性和有效性",
            "🧠 自适应机制能让测试策略持续优化和改进",
            "📊 数据驱动的测试决策比经验驱动更加可靠",
            "🚀 记忆体技术是测试智能体的核心能力之一"
        ]
        
        for insight in key_insights:
            print(f"  {insight}")
        
        print("\n🔗 相关资源:")
        resources = [
            "📚 详细文档: README.md",
            "🔧 配置说明: config.py",
            "📝 模型定义: models.py", 
            "🎭 场景代码: scenarios/",
            "💾 记忆管理: memory_manager.py"
        ]
        
        for resource in resources:
            print(f"  {resource}")
        
        # 显示最终统计
        final_stats = self.memory_manager.get_memory_stats()
        total_memories = sum(final_stats.values())
        print(f"\n📊 演示结束时记忆体总数: {total_memories} 条记录")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="测试记忆体功能演示系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python demo.py                    # 交互式演示
  python demo.py --all              # 运行所有场景
  python demo.py --scenario experience  # 运行单个场景
  python demo.py --interactive      # 强制交互模式
        """
    )
    
    parser.add_argument(
        "--scenario",
        choices=["experience", "context", "execution", "error", "recommendation", "adaptive"],
        help="运行指定的单个场景"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="运行所有场景演示"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="运行交互式演示"
    )
    
    args = parser.parse_args()
    
    try:
        demo = TestingMemoryDemo()
        
        if args.all:
            demo.run_all_scenarios()
        elif args.scenario:
            demo.run_single_scenario(args.scenario)
        elif args.interactive or len(sys.argv) == 1:
            demo.run_interactive_demo()
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n\n👋 演示被用户中断，感谢使用！")
    except Exception as e:
        print(f"\n❌ 演示系统发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()