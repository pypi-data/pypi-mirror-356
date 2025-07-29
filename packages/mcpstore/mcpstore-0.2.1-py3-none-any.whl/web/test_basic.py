#!/usr/bin/env python3
"""
MCPStore Web界面基本功能测试
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试基本导入"""
    print("🧪 测试基本导入...")
    
    try:
        # 测试核心依赖
        import streamlit as st
        print("✅ Streamlit 导入成功")
        
        import requests
        print("✅ Requests 导入成功")
        
        from typing import Dict, List, Optional, Any
        print("✅ Typing 导入成功")
        
        # 测试自定义模块
        from utils.api_client import MCPStoreAPI
        print("✅ API客户端导入成功")
        
        from utils.config_manager import SessionManager, WebConfigManager
        print("✅ 配置管理器导入成功")
        
        from components.ui_components import StatusIndicator, MetricCard
        print("✅ UI组件导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_api_client():
    """测试API客户端"""
    print("\n🧪 测试API客户端...")
    
    try:
        from utils.api_client import MCPStoreAPI
        
        # 测试HTTP后端
        api_client = MCPStoreAPI("http", "http://localhost:18611")
        print("✅ HTTP后端创建成功")
        
        # 测试Direct后端
        api_client = MCPStoreAPI("direct")
        print("✅ Direct后端创建成功")
        
        # 测试后端切换
        api_client.switch_backend("http", "http://localhost:18611")
        print("✅ 后端切换成功")
        
        # 测试后端信息
        info = api_client.get_backend_info()
        print(f"✅ 后端信息: {info}")
        
        return True
        
    except Exception as e:
        print(f"❌ API客户端测试失败: {e}")
        return False

def test_config_manager():
    """测试配置管理器"""
    print("\n🧪 测试配置管理器...")
    
    try:
        from utils.config_manager import WebConfigManager, SessionManager
        
        # 测试配置管理器
        config_manager = WebConfigManager()
        print("✅ 配置管理器创建成功")
        
        # 测试配置读写
        config_manager.set('test.key', 'test_value')
        value = config_manager.get('test.key')
        assert value == 'test_value'
        print("✅ 配置读写测试成功")
        
        # 测试预设服务
        presets = config_manager.get_preset_services()
        print(f"✅ 预设服务: {len(presets)} 个")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {e}")
        return False

def test_ui_components():
    """测试UI组件"""
    print("\n🧪 测试UI组件...")
    
    try:
        from components.ui_components import StatusIndicator, MetricCard
        
        # 测试状态指示器
        status_text = StatusIndicator.show("healthy", "测试状态")
        print(f"✅ 状态指示器: {status_text}")
        
        print("✅ UI组件测试成功")
        
        return True
        
    except Exception as e:
        print(f"❌ UI组件测试失败: {e}")
        return False

def test_config():
    """测试配置文件"""
    print("\n🧪 测试配置文件...")
    
    try:
        from config import WebConfig, config
        
        # 测试配置获取
        app_config = WebConfig.get_config('app')
        print(f"✅ 应用配置: {app_config}")
        
        # 测试功能开关
        wizard_enabled = WebConfig.is_feature_enabled('enable_service_wizard')
        print(f"✅ 服务向导功能: {'启用' if wizard_enabled else '禁用'}")
        
        # 测试预设服务
        featured_services = WebConfig.get_featured_services()
        print(f"✅ 推荐服务: {len(featured_services)} 个")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置文件测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 MCPStore Web界面基本功能测试")
    print("=" * 50)
    
    tests = [
        ("基本导入", test_imports),
        ("API客户端", test_api_client),
        ("配置管理器", test_config_manager),
        ("UI组件", test_ui_components),
        ("配置文件", test_config)
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
        print("🎉 所有测试通过！Web界面准备就绪。")
        print("\n🚀 启动命令:")
        print("  python start_simple.py")
        print("  或")
        print("  python run.py")
    else:
        print("⚠️ 部分测试失败，请检查相关模块。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
