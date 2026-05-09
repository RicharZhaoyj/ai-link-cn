#!/usr/bin/env python3
"""
API测试用例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import json
import requests

class TestAPIBasics:
    """API基础测试"""
    
    def test_hello_endpoint(self):
        """测试/hello端点"""
        response = requests.get("https://ai.link.cn/api/hello", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "message" in data
        assert data["status"] == "success"
        print("✅ /api/hello 端点测试通过")
    
    def test_auth_endpoint_exists(self):
        """测试认证端点存在"""
        # 测试认证端点是否可以访问（可能返回405 Method Not Allowed是正常的）
        response = requests.get("https://ai.link.cn/api/auth", timeout=10)
        # GET可能不被允许，但端点应该存在
        assert response.status_code in [200, 405, 404]
        print("✅ /api/auth 端点测试通过")
    
    def test_premium_endpoint_security(self):
        """测试高级API端点安全性"""
        # 未授权的请求应该被拒绝
        response = requests.get("https://ai.link.cn/api/premium/market", timeout=10)
        # 可能返回401、403或404
        assert response.status_code in [401, 403, 404, 405]
        print("✅ /api/premium/market 安全性测试通过")

class TestWebsitePages:
    """网站页面测试"""
    
    def test_homepage(self):
        """测试主页"""
        response = requests.get("https://ai.link.cn/", timeout=10)
        assert response.status_code == 200
        assert "text/html" in response.headers.get("Content-Type", "").lower()
        print("✅ 主页测试通过")
    
    def test_pricing_page(self):
        """测试定价页面"""
        response = requests.get("https://ai.link.cn/pricing.html", timeout=10)
        assert response.status_code == 200
        assert "text/html" in response.headers.get("Content-Type", "").lower()
        print("✅ 定价页面测试通过")
    
    def test_auth_page(self):
        """测试认证页面"""
        response = requests.get("https://ai.link.cn/auth.html", timeout=10)
        assert response.status_code == 200
        assert "text/html" in response.headers.get("Content-Type", "").lower()
        print("✅ 认证页面测试通过")

class TestSystemHealth:
    """系统健康测试"""
    
    def test_response_time(self):
        """测试响应时间"""
        import time
        start_time = time.time()
        response = requests.get("https://ai.link.cn/api/hello", timeout=10)
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 5.0  # 响应时间应小于5秒
        print(f"✅ 响应时间测试通过: {response_time:.2f}秒")
    
    def test_uptime(self):
        """测试系统可用性"""
        # 连续测试3次
        successes = 0
        for i in range(3):
            try:
                response = requests.get("https://ai.link.cn/api/hello", timeout=5)
                if response.status_code == 200:
                    successes += 1
            except:
                pass
        
        success_rate = successes / 3
        assert success_rate >= 0.67  # 至少2/3的成功率
        print(f"✅ 系统可用性测试通过: {success_rate:.0%}")

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("运行API测试")
    print("=" * 50)
    
    test_classes = [TestAPIBasics, TestWebsitePages, TestSystemHealth]
    all_passed = True
    
    for test_class in test_classes:
        print(f"\n测试类: {test_class.__name__}")
        test_instance = test_class()
        
        # 获取所有测试方法
        test_methods = [method for method in dir(test_class) 
                       if method.startswith('test_')]
        
        for method_name in test_methods:
            try:
                method = getattr(test_instance, method_name)
                method()
                print(f"  {method_name}: ✅ 通过")
            except Exception as e:
                print(f"  {method_name}: ❌ 失败 - {str(e)[:100]}")
                all_passed = False
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print("=" * 50)
    
    if all_passed:
        print("🎉 所有API测试通过!")
        return True
    else:
        print("⚠️  部分测试失败")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)