#!/usr/bin/env python3
"""
测试启动脚本
"""

import subprocess
import sys
import os

def main():
    """测试启动"""
    print("🧪 测试启动MCPStore Web界面...")
    
    # 检查文件
    if not os.path.exists('app.py'):
        print("❌ app.py 不存在")
        return
    
    # 简单启动命令
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8502",  # 使用不同端口避免冲突
        "--server.fileWatcherType", "none"
    ]
    
    print(f"🚀 启动命令: {' '.join(cmd)}")
    print("🌐 访问地址: http://localhost:8502")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")

if __name__ == "__main__":
    main()
