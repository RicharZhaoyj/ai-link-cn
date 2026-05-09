#!/usr/bin/env python3
"""
基本测试用例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_import_modules():
    """测试能否导入主要模块"""
    try:
        import multi_market_analysis_system
        import market_data_collector
        import market_monitor
        import portfolio_optimizer
        print("✅ 主要模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_python_version():
    """测试Python版本"""
    import sys
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    return version.major == 3 and version.minor >= 8

def test_requirements():
    """测试基本依赖"""
    try:
        import pandas
        import numpy
        import yfinance
        import ccxt
        import requests
        print("✅ 基础依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 依赖缺失: {e}")
        return False

def test_api_endpoints():
    """测试API端点基本功能"""
    try:
        import requests
        # 测试基础API
        response = requests.get("https://ai.link.cn/api/hello", timeout=5)
        if response.status_code == 200:
            print("✅ API端点响应正常")
            return True
        else:
            print(f"❌ API端点响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("运行基本测试")
    print("=" * 50)
    
    results = []
    
    results.append(("Python版本检查", test_python_version()))
    results.append(("模块导入测试", test_import_modules()))
    results.append(("依赖检查", test_requirements()))
    results.append(("API端点测试", test_api_endpoints()))
    
    print("=" * 50)
    print("测试结果汇总:")
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(passed for _, passed in results)
    if all_passed:
        print("🎉 所有测试通过!")
        sys.exit(0)
    else:
        print("⚠️  部分测试失败")
        sys.exit(1)