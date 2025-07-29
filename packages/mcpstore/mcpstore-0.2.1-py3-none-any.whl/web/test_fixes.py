#!/usr/bin/env python3
"""
测试修复结果
"""

import sys
import os
import re

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_button_keys():
    """测试按钮key是否唯一"""
    print("🧪 测试按钮key唯一性...")
    
    files_to_check = [
        'app.py',
        'pages/service_management.py',
        'pages/tool_management.py',
        'pages/agent_management.py',
        'pages/monitoring.py',
        'pages/configuration.py'
    ]
    
    all_keys = []
    duplicate_keys = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 查找所有button的key参数
                key_pattern = r'st\.button\([^)]*key\s*=\s*["\']([^"\']+)["\']'
                keys = re.findall(key_pattern, content)
                
                for key in keys:
                    if key in all_keys:
                        duplicate_keys.append(key)
                    else:
                        all_keys.append(key)
                
                print(f"✅ {file_path}: 找到 {len(keys)} 个按钮key")
    
    if duplicate_keys:
        print(f"❌ 发现重复的key: {duplicate_keys}")
        return False
    else:
        print(f"✅ 所有 {len(all_keys)} 个按钮key都是唯一的")
        return True

def test_navigation_structure():
    """测试导航结构"""
    print("\n🧪 测试导航结构...")
    
    try:
        import app
        
        # 检查是否有render_sidebar函数
        if hasattr(app, 'render_sidebar'):
            print("✅ render_sidebar 函数存在")
        else:
            print("❌ render_sidebar 函数缺失")
            return False
        
        # 检查是否有render_main_content函数
        if hasattr(app, 'render_main_content'):
            print("✅ render_main_content 函数存在")
        else:
            print("❌ render_main_content 函数缺失")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 导航结构测试失败: {e}")
        return False

def test_sidebar_navigation():
    """测试侧边栏导航代码"""
    print("\n🧪 测试侧边栏导航代码...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否移除了标签页
        if 'st.tabs(' in content:
            print("⚠️ 仍然存在标签页代码")
            return False
        else:
            print("✅ 标签页代码已移除")
        
        # 检查是否有侧边栏导航按钮
        if 'nav_' in content and 'current_page' in content:
            print("✅ 侧边栏导航代码存在")
        else:
            print("❌ 侧边栏导航代码缺失")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 侧边栏导航测试失败: {e}")
        return False

def test_modal_functions():
    """测试模态窗口函数"""
    print("\n🧪 测试模态窗口函数...")
    
    try:
        import app
        
        modal_functions = [
            'handle_modals',
            'show_add_service_modal',
            'show_test_tool_modal',
            'show_system_status_modal'
        ]
        
        for func_name in modal_functions:
            if hasattr(app, func_name):
                print(f"✅ {func_name} 函数存在")
            else:
                print(f"❌ {func_name} 函数缺失")
                return False
        
        return True
    except Exception as e:
        print(f"❌ 模态窗口函数测试失败: {e}")
        return False

def test_imports():
    """测试导入"""
    print("\n🧪 测试导入...")
    
    try:
        import app
        print("✅ app.py 导入成功")
        
        from style import apply_custom_styles
        print("✅ style.py 导入成功")
        
        from components.modal_components import ServiceModal
        print("✅ modal_components.py 导入成功")
        
        return True
    except Exception as e:
        print(f"❌ 导入测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 MCPStore Web界面修复测试")
    print("=" * 50)
    
    tests = [
        ("导入测试", test_imports),
        ("按钮key唯一性", test_button_keys),
        ("导航结构", test_navigation_structure),
        ("侧边栏导航", test_sidebar_navigation),
        ("模态窗口函数", test_modal_functions)
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
        print("🎉 所有修复测试通过！")
        print("\n✨ 修复内容:")
        print("  1. ✅ 修复了按钮ID重复问题")
        print("  2. ✅ 移除了标签页导航")
        print("  3. ✅ 实现了侧边栏菜单导航")
        print("  4. ✅ 优化了导航按钮样式")
        print("  5. ✅ 保持了模态窗口功能")
        print("\n🚀 启动命令:")
        print("  python start_simple.py")
    else:
        print("⚠️ 部分测试失败，请检查相关模块。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
