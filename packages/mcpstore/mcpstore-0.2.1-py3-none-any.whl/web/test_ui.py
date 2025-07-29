#!/usr/bin/env python3
"""
测试UI组件，验证修复是否成功
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_metric_card():
    """测试MetricCard组件"""
    print("🧪 测试MetricCard组件...")
    
    try:
        from components.ui_components import MetricCard
        
        # 模拟Streamlit环境
        class MockStreamlit:
            def container(self):
                return self
            
            def __enter__(self):
                return self
            
            def __exit__(self, *args):
                pass
            
            def markdown(self, text, **kwargs):
                print(f"Markdown: {text}")
            
            def metric(self, label, value, delta=None, **kwargs):
                print(f"Metric: label='{label}', value={value}, delta={delta}, kwargs={kwargs}")
                # 检查label是否为空
                if not label or label.strip() == "":
                    raise ValueError("Empty label detected!")
            
            def caption(self, text):
                print(f"Caption: {text}")
        
        # 替换streamlit模块
        import components.ui_components
        components.ui_components.st = MockStreamlit()
        
        # 测试MetricCard
        print("测试基本MetricCard...")
        MetricCard.show("测试指标", 100, help_text="这是一个测试")
        
        print("测试带颜色的MetricCard...")
        MetricCard.show("彩色指标", 200, color="green", icon="🟢")
        
        print("测试带delta的MetricCard...")
        MetricCard.show("变化指标", 300, delta=50)
        
        print("✅ MetricCard测试通过")
        return True
        
    except Exception as e:
        print(f"❌ MetricCard测试失败: {e}")
        return False

def test_status_indicator():
    """测试StatusIndicator组件"""
    print("\n🧪 测试StatusIndicator组件...")
    
    try:
        from components.ui_components import StatusIndicator
        
        # 测试各种状态
        statuses = ['healthy', 'unhealthy', 'warning', 'unknown', 'connecting', 'disconnected']
        
        for status in statuses:
            result = StatusIndicator.show(status)
            print(f"Status '{status}': {result}")
        
        print("✅ StatusIndicator测试通过")
        return True
        
    except Exception as e:
        print(f"❌ StatusIndicator测试失败: {e}")
        return False

def test_imports():
    """测试所有导入"""
    print("\n🧪 测试组件导入...")
    
    try:
        from components.ui_components import (
            StatusIndicator, MetricCard, ProgressBar, 
            NotificationSystem, DataTable, QuickActions
        )
        print("✅ UI组件导入成功")
        
        from components.service_components import (
            ServiceCard, ServiceWizard, ServiceMonitor
        )
        print("✅ 服务组件导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 组件导入失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 UI组件测试")
    print("=" * 40)
    
    tests = [
        ("组件导入", test_imports),
        ("StatusIndicator", test_status_indicator),
        ("MetricCard", test_metric_card)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
        
        print("-" * 30)
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有UI组件测试通过！")
        print("✅ MetricCard的空label问题已修复")
        print("\n🚀 现在可以安全启动Web界面:")
        print("  python start_simple.py")
    else:
        print("⚠️ 部分测试失败，请检查相关组件。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
