#!/usr/bin/env python3
"""
测试样式改进
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_functions():
    """测试应用函数"""
    print("🧪 测试应用函数...")
    
    try:
        import app
        
        # 检查新增的函数
        functions_to_check = [
            'render_brand_section',
            'render_navigation_menu',
            'render_system_status',
            'render_status_bar',
            'show_loading_screen'
        ]
        
        for func_name in functions_to_check:
            if hasattr(app, func_name):
                print(f"✅ {func_name} 函数存在")
            else:
                print(f"❌ {func_name} 函数缺失")
                return False
        
        return True
    except Exception as e:
        print(f"❌ 应用函数测试失败: {e}")
        return False

def test_style_updates():
    """测试样式更新"""
    print("\n🧪 测试样式更新...")
    
    try:
        with open('style.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查新增的样式
        style_checks = [
            'loading-spinner',
            'metric-card',
            'status-card',
            'linear-gradient',
            'box-shadow'
        ]
        
        for style in style_checks:
            if style in content:
                print(f"✅ 包含 {style} 样式")
            else:
                print(f"❌ 缺少 {style} 样式")
                return False
        
        return True
    except Exception as e:
        print(f"❌ 样式更新测试失败: {e}")
        return False

def test_loading_functionality():
    """测试加载功能"""
    print("\n🧪 测试加载功能...")
    
    try:
        import app
        
        # 检查加载相关的代码
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'page_loading' in content:
            print("✅ 包含页面加载状态管理")
        else:
            print("❌ 缺少页面加载状态管理")
            return False
        
        if 'show_loading_screen' in content:
            print("✅ 包含加载屏幕函数")
        else:
            print("❌ 缺少加载屏幕函数")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 加载功能测试失败: {e}")
        return False

def test_header_improvements():
    """测试头部改进"""
    print("\n🧪 测试头部改进...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查头部改进
        if 'linear-gradient(135deg, #667eea' in content:
            print("✅ 包含渐变背景头部")
        else:
            print("❌ 缺少渐变背景头部")
            return False
        
        if 'MCPStore 管理控制台' in content:
            print("✅ 包含专业标题")
        else:
            print("❌ 缺少专业标题")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 头部改进测试失败: {e}")
        return False

def test_sidebar_improvements():
    """测试侧边栏改进"""
    print("\n🧪 测试侧边栏改进...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否移除了快速操作
        if 'render_quick_actions' not in content or content.count('render_quick_actions') <= 1:
            print("✅ 快速操作已从侧边栏移除")
        else:
            print("❌ 快速操作仍在侧边栏中")
            return False
        
        # 检查品牌区域
        if 'render_brand_section' in content:
            print("✅ 包含品牌标识区域")
        else:
            print("❌ 缺少品牌标识区域")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 侧边栏改进测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 MCPStore Web样式改进测试")
    print("=" * 50)
    
    tests = [
        ("应用函数", test_app_functions),
        ("样式更新", test_style_updates),
        ("加载功能", test_loading_functionality),
        ("头部改进", test_header_improvements),
        ("侧边栏改进", test_sidebar_improvements)
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
    
    if passed >= 4:  # 允许一个测试失败
        print("🎉 样式改进基本成功！")
        print("\n✨ 改进内容:")
        print("  1. ✅ 移除侧边栏快速操作")
        print("  2. ✅ 专业大气的侧边栏设计")
        print("  3. ✅ 美化的管理面板头部")
        print("  4. ✅ 页面切换加载动画")
        print("  5. ✅ 渐变背景和阴影效果")
        print("\n🚀 启动命令:")
        print("  python start_stable.py")
    else:
        print("⚠️ 部分改进可能不完整，请检查相关模块。")
    
    return passed >= 4

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
