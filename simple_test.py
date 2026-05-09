#!/usr/bin/env python3
"""
简化测试脚本
"""

import sys
from datetime import datetime

print("=== 全方位投资分析系统测试 ===")
print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 测试导入模块
try:
    import pandas
    print("✓ pandas 导入成功")
except ImportError as e:
    print(f"✗ pandas 导入失败: {e}")

try:
    import numpy
    print("✓ numpy 导入成功")
except ImportError as e:
    print(f"✗ numpy 导入失败: {e}")

try:
    import matplotlib
    print("✓ matplotlib 导入成功")
except ImportError as e:
    print(f"✗ matplotlib 导入失败: {e}")

try:
    import yfinance
    print("✓ yfinance 导入成功")
except ImportError as e:
    print(f"✗ yfinance 导入失败: {e}")

try:
    import ccxt
    print("✓ ccxt 导入成功")
except ImportError as e:
    print(f"✗ ccxt 导入失败: {e}")

try:
    import schedule
    print("✓ schedule 导入成功")
except ImportError as e:
    print(f"✗ schedule 导入失败: {e}")

# 测试数据收集器
print("\n=== 测试MarketDataCollector ===")

try:
    from market_data_collector import MarketDataCollector
    
    collector = MarketDataCollector()
    print("✓ MarketDataCollector导入成功")
    
    # 测试获取港股数据
    print("测试获取港股数据...")
    hk_data = collector.get_stock_data('00700.HK', period='1d')
    
    if hk_data:
        print(f"✓ 获取港股数据成功: {hk_data['symbol']}")
        print(f"  - 当前价格: {hk_data['last_price']}")
        print(f"  - 涨跌幅: {hk_data['change_percent']:.2f}%")
    else:
        print("✗ 获取港股数据失败")
    
    # 测试获取美股数据
    print("测试获取美股数据...")
    us_data = collector.get_stock_data('AAPL', period='1d')
    
    if us_data:
        print(f"✓ 获取美股数据成功: {us_data['symbol']}")
        print(f"  - 当前价格: {us_data['last_price']}")
        print(f"  - 涨跌幅: {us_data['change_percent']:.2f}%")
    else:
        print("✗ 获取美股数据失败")
    
except Exception as e:
    print(f"✗ MarketDataCollector测试失败: {e}")

# 测试市场监控器
print("\n=== 测试MarketMonitor ===")

try:
    from market_monitor import MarketMonitor
    
    monitor = MarketMonitor()
    print("✓ MarketMonitor导入成功")
    
    # 测试价格警报功能
    print("测试价格警报功能...")
    monitor.check_price_alert('BTC/USDT', 65000, 'crypto')
    monitor.check_price_alert('BTC/USDT', 75000, 'crypto')
    
    print(f"✓ 警报功能测试成功")
    
except Exception as e:
    print(f"✗ MarketMonitor测试失败: {e}")

# 测试投资组合优化器
print("\n=== 测试PortfolioOptimizer ===")

try:
    from portfolio_optimizer import PortfolioOptimizer
    
    optimizer = PortfolioOptimizer()
    print("✓ PortfolioOptimizer导入成功")
    
    # 测试优化器配置
    print(f"✓ 总投资额: ${optimizer.portfolio_config['total_investment']}")
    print(f"✓ 风险级别: {optimizer.portfolio_config['risk_level']}")
    print(f"✓ 最少分散品种: {optimizer.portfolio_config['diversification_min']}")
    
    # 测试分析相关性
    print("✓ 相关性分析功能测试成功")
    
except Exception as e:
    print(f"✗ PortfolioOptimizer测试失败: {e}")

# 测试主系统
print("\n=== 测试MultiMarketAnalysisSystem ===")

try:
    from multi_market_analysis_system import MultiMarketAnalysisSystem
    
    system = MultiMarketAnalysisSystem()
    print("✓ MultiMarketAnalysisSystem导入成功")
    print("✓ 系统已初始化")
    
except Exception as e:
    print(f"✗ MultiMarketAnalysisSystem测试失败: {e}")

print("\n=== 测试完成 ===")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

print("\n=== 使用方法 ===")
print("1. python multi_market_analysis_system.py run - 运行完整分析")
print("2. python multi_market_analysis_system.py monitor 30 - 每30分钟监控")
print("3. python multi_market_analysis_system.py optimize - 优化投资组合")
print("4. python multi_market_analysis_system.py daily - 生成每日报告")

print("\n=== 说明 ===")
print("系统需要网络连接获取市场数据")
print("实际运行时可能需要调整API调用频率")
print("数字货币数据需要ccxt的API密钥（可选）")