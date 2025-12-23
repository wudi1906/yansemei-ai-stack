#!/usr/bin/env python3
"""
测试记忆体功能快速启动脚本

这个脚本提供了快速体验测试记忆体功能的入口，
包括环境检查、依赖安装、快速演示等功能。

使用方法:
    python quick_start.py
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        print(f"   当前版本: {sys.version}")
        return False
    else:
        print(f"✅ Python版本: {sys.version.split()[0]}")
        return True

def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    
    required_packages = [
        "langchain",
        "langgraph", 
        "langmem",
        "pydantic"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
            print(f"❌ 缺少依赖: {package}")
        else:
            print(f"✅ 已安装: {package}")
    
    return missing_packages

def install_dependencies(packages):
    """安装缺失的依赖包"""
    if not packages:
        return True
    
    print(f"\n🔧 安装缺失的依赖包: {', '.join(packages)}")
    
    try:
        # 尝试安装缺失的包
        for package in packages:
            print(f"   正在安装 {package}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"   ✅ {package} 安装成功")
            else:
                print(f"   ❌ {package} 安装失败: {result.stderr}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 安装依赖时出错: {e}")
        return False

def show_welcome():
    """显示欢迎信息"""
    print(f"\n{'='*60}")
    print("🧠 欢迎使用测试记忆体功能演示系统")
    print(f"{'='*60}")
    print()
    print("这个系统演示了如何在软件测试智能体中应用记忆体功能：")
    print()
    print("📚 测试经验积累与学习 - 记录和学习测试经验")
    print("🗂️ 测试上下文记忆     - 管理项目配置和用户偏好")
    print("🚀 测试用例执行记忆   - 优化测试执行策略")
    print("🚨 错误处理经验记忆   - 智能错误诊断和解决")
    print("🎯 智能测试用例推荐   - 基于历史数据的推荐")
    print("🧠 自适应测试策略     - 根据表现自动调整策略")
    print()

def show_menu():
    """显示主菜单"""
    print("📋 请选择要体验的功能:")
    print()
    print("1. 🎭 运行完整演示 (推荐)")
    print("2. 📚 测试经验积累与学习")
    print("3. 🗂️ 测试上下文记忆")
    print("4. 🚀 测试用例执行记忆")
    print("5. 🚨 错误处理经验记忆")
    print("6. 🎯 智能测试用例推荐")
    print("7. 🧠 自适应测试策略")
    print("8. 💡 基础使用示例")
    print("9. 📊 查看系统状态")
    print("0. 🚪 退出")
    print()

def run_demo_scenario(scenario_name):
    """运行指定的演示场景"""
    try:
        from demo import TestingMemoryDemo
        
        demo = TestingMemoryDemo()
        
        if scenario_name == "all":
            demo.run_all_scenarios()
        elif scenario_name == "basic":
            from examples.basic_usage import main as run_basic
            run_basic()
        elif scenario_name == "stats":
            demo._show_memory_stats()
        else:
            demo.run_single_scenario(scenario_name)
            
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保所有依赖都已正确安装")
    except Exception as e:
        print(f"❌ 运行演示时出错: {e}")

def check_system_status():
    """检查系统状态"""
    print("\n📊 系统状态检查:")
    print("-" * 40)
    
    # 检查Python版本
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    
    # 检查依赖包
    try:
        import langchain
        print(f"📦 LangChain: {langchain.__version__}")
    except:
        print("📦 LangChain: 未安装")
    
    try:
        import langgraph
        print(f"📦 LangGraph: 已安装")
    except:
        print("📦 LangGraph: 未安装")
    
    try:
        import pydantic
        print(f"📦 Pydantic: {pydantic.__version__}")
    except:
        print("📦 Pydantic: 未安装")
    
    # 检查记忆体管理器
    try:
        from memory_manager import TestingMemoryManager
        manager = TestingMemoryManager()
        stats = manager.get_memory_stats()
        total_memories = sum(stats.values())
        print(f"🧠 记忆体状态: 正常 ({total_memories} 条记录)")
    except Exception as e:
        print(f"🧠 记忆体状态: 异常 ({e})")
    
    print("-" * 40)

def main():
    """主函数"""
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查依赖
    missing_packages = check_dependencies()
    
    # 安装缺失的依赖
    if missing_packages:
        print(f"\n⚠️ 发现 {len(missing_packages)} 个缺失的依赖包")
        install_choice = input("是否自动安装? (y/n): ").lower().strip()
        
        if install_choice in ['y', 'yes', '是']:
            if not install_dependencies(missing_packages):
                print("❌ 依赖安装失败，请手动安装后重试")
                sys.exit(1)
        else:
            print("❌ 请手动安装依赖包后重试:")
            for package in missing_packages:
                print(f"   pip install {package}")
            sys.exit(1)
    
    # 显示欢迎信息
    show_welcome()
    
    # 主循环
    while True:
        show_menu()
        
        try:
            choice = input("请输入选项 (0-9): ").strip()
            
            if choice == "0":
                print("\n👋 感谢使用测试记忆体演示系统！")
                break
            elif choice == "1":
                run_demo_scenario("all")
            elif choice == "2":
                run_demo_scenario("experience")
            elif choice == "3":
                run_demo_scenario("context")
            elif choice == "4":
                run_demo_scenario("execution")
            elif choice == "5":
                run_demo_scenario("error")
            elif choice == "6":
                run_demo_scenario("recommendation")
            elif choice == "7":
                run_demo_scenario("adaptive")
            elif choice == "8":
                run_demo_scenario("basic")
            elif choice == "9":
                check_system_status()
            else:
                print("❌ 无效选项，请重新选择")
            
            if choice != "0" and choice != "9":
                input("\n按回车键继续...")
                
        except KeyboardInterrupt:
            print("\n\n👋 演示被用户中断，感谢使用！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            input("按回车键继续...")

if __name__ == "__main__":
    main()