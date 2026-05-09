#!/usr/bin/env python3
"""
全方位投资分析系统安装和测试脚本
"""

import subprocess
import sys
import os
from datetime import datetime

def install_dependencies():
    """安装依赖包"""
    print("=== 安装系统依赖 ===")
    
    dependencies = [
        "pip install pandas numpy matplotlib yfinance ccxt schedule",
        "pip install scipy statsmodels"  # 可选依赖，用于更高级的分析
    ]
    
    for command in dependencies:
        print(f"执行: {command}")
        result = subprocess.run(command.split(), capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ {command} 安装成功")
        else:
            print(f"✗ {command} 安装失败")
            print(f"错误: {result.stderr}")
    
    print("所有依赖安装完成")

def test_market_data_collector():
    """测试MarketDataCollector"""
    print("=== 测试市场数据收集器 ===")
    
    # 导入模块测试
    try:
        from market_data_collector import MarketDataCollector
        
        collector = MarketDataCollector()
        print("✓ MarketDataCollector模块导入成功")
        
        # 测试获取数据
        all_data = collector.get_all_market_data()
        
        print("✓ 数据收集测试成功")
        print(f"港股数据: {len(all_data['hk_stocks'])}条")
        print(f"美股数据: {len(all_data['us_stocks'])}条")
        print(f"新加坡股票数据: {len(all_data['sg_stocks'])}条")
        print(f"ETF数据: {len(all_data['etfs'])}条")
        print(f"期货数据: {len(all_data['futures'])}条")
        print(f"基金数据: {len(all_data['funds'])}条")
        print(f"数字货币数据: {len(all_data['crypto'])}条")
        
        # 测试生成报告
        summary = collector.generate_market_summary(all_data)
        print("✓ 市场概况生成成功")
        
        # 测试保存数据
        data_file, report_file = collector.save_data(all_data, summary)
        print(f"✓ 数据保存成功: {data_file}, {report_file}")
        
        return True
    except Exception as e:
        print(f"✗ MarketDataCollector测试失败: {e}")
        return False

def test_market_monitor():
    """测试MarketMonitor"""
    print("=== 测试市场监控器 ===")
    
    try:
        from market_monitor import MarketMonitor
        
        monitor = MarketMonitor()
        print("✓ MarketMonitor模块导入成功")
        
        # 测试监控运行
        print("测试一次监控...")
        all_data = monitor.monitor_once()
        
        print("✓ 监控测试成功")
        print(f"警报数量: {len(monitor.alerts)}")
        
        # 测试每日报告
        report_file = monitor.generate_daily_report()
        print(f"✓ 每日报告生成成功: {report_file}")
        
        return True
    except Exception as e:
        print(f"✗ MarketMonitor测试失败: {e}")
        return False

def test_portfolio_optimizer():
    """测试PortfolioOptimizer"""
    print("=== 测试投资组合优化器 ===")
    
    try:
        from portfolio_optimizer import PortfolioOptimizer
        
        optimizer = PortfolioOptimizer()
        print("✓ PortfolioOptimizer模块导入成功")
        
        # 测试优化运行
        portfolio = optimizer.run_optimization()
        
        print("✓ 投资组合优化成功")
        print(f"优化品种数量: {len(portfolio)}")
        
        # 测试图表生成
        chart_files = optimizer.plot_portfolio_composition(portfolio)
        print(f"✓ 图表生成成功: {chart_files}")
        
        return True
    except Exception as e:
        print(f"✗ PortfolioOptimizer测试失败: {e}")
        return False

def test_complete_system():
    """测试完整系统"""
    print("=== 测试完整系统 ===")
    
    try:
        from multi_market_analysis_system import MultiMarketAnalysisSystem
        
        system = MultiMarketAnalysisSystem()
        print("✓ MultiMarketAnalysisSystem模块导入成功")
        
        # 测试完整分析
        print("运行完整分析...")
        system.run_analysis()
        
        print("✓ 完整系统测试成功")
        
        return True
    except Exception as e:
        print(f"✗ 完整系统测试失败: {e}")
        return False

def run_demo():
    """运行演示"""
    print("=== 系统演示 ===")
    
    # 展示系统功能
    print("1. 市场数据收集演示")
    print("2. 实时监控演示")
    print("3. 投资组合优化演示")
    print("4. 综合报告演示")
    
    # 运行演示
    from multi_market_analysis_system import MultiMarketAnalysisSystem
    system = MultiMarketAnalysisSystem()
    
    # 运行完整分析
    system.run_analysis()
    
    print("=== 演示完成 ===")
    print("所有功能测试完成")

def create_example_config():
    """创建示例配置文件"""
    print("=== 创建示例配置文件 ===")
    
    config_content = """
# 全方位投资分析系统配置文件

# 数据源配置
DATA_SOURCES = {
    "yfinance": {
        "timeout": 10,
        "retry": 3,
        "interval": "30d"
    },
    "ccxt": {
        "exchange": "binance",
        "symbols": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"]
    }
}

# 监控配置
MONITOR_CONFIG = {
    "interval": 30,  # 监控间隔（分钟）
    "alert_thresholds": {
        "price_change": 5.0,  # 价格变化超过5%触发警报
        "volume_change": 50.0,  # 成交量变化超过50%触发警报
        "technical": {
            "rsi_buy": 30,
            "rsi_sell": 70,
            "macd_threshold": 0.1
        }
    },
    "price_alerts": {
        "BTC/USDT": {"buy": 65000, "sell": 75000},
        "ETH/USDT": {"buy": 3500, "sell": 4500},
        "AAPL": {"buy": 150, "sell": 180},
        "00700.HK": {"buy": 300, "sell": 400}
    }
}

# 投资组合配置
PORTFOLIO_CONFIG = {
    "total_investment": 1000000,
    "risk_level": "moderate",  # conservative, moderate, aggressive
    "investment_horizon": "medium",
    "asset_classes": {
        "hk_stocks": {"max_weight": 0.30},
        "us_stocks": {"max_weight": 0.35},
        "sg_stocks": {"max_weight": 0.10},
        "etfs": {"max_weight": 0.15},
        "futures": {"max_weight": 0.05},
        "funds": {"max_weight": 0.10},
        "crypto": {"max_weight": 0.20}
    },
    "diversification_min": 8
}

# 其他配置
OTHER_CONFIG = {
    "report_frequency": "daily",  # 报告频率 daily/weekly/monthly
    "auto_save": True,
    "notify_enabled": False,
    "data_retention": 30  # 数据保留天数
}
"""
    
    config_file = "config_example.py"
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print(f"✓ 示例配置文件保存: {config_file}")

def main():
    """主函数"""
    print("=== 全方位投资分析系统安装和测试 ===")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or python_version.minor < 8:
        print("✗ Python版本过低，需要Python 3.8或更高版本")
        print(f"当前版本: Python {python_version.major}.{python_version.minor}")
        return
    
    print(f"✓ Python版本: Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 安装依赖
    install_dependencies()
    
    # 测试各个模块
    print("\n=== 模块测试 ===")
    
    modules = {
        "MarketDataCollector": test_market_data_collector,
        "MarketMonitor": test_market_monitor,
        "PortfolioOptimizer": test_portfolio_optimizer,
        "MultiMarketAnalysisSystem": test_complete_system
    }
    
    test_results = {}
    for module_name, test_function in modules.items():
        success = test_function()
        test_results[module_name] = success
    
    # 汇总测试结果
    print("\n=== 测试结果汇总 ===")
    all_success = True
    for module_name, success in test_results.items():
        if success:
            print(f"✓ {module_name} 测试成功")
        else:
            print(f"✗ {module_name} 测试失败")
            all_success = False
    
    if all_success:
        print("\n✓ 所有模块测试成功")
        
        # 创建示例配置文件
        create_example_config()
        
        # 运行演示
        run_demo()
        
        print("\n=== 系统安装完成 ===")
        print("使用方法:")
        print("1. python multi_market_analysis_system.py run - 运行完整分析")
        print("2. python multi_market_analysis_system.py monitor [interval] - 启动实时监控")
        print("3. python multi_market_analysis_system.py optimize - 优化投资组合")
        print("4. python multi_market_analysis_system.py daily - 生成每日报告")
        
        print("\n配置说明:")
        print("- 修改market_data_collector.py中的市场品种")
        print("- 修改market_monitor.py中的警报阈值")
        print("- 修改portfolio_optimizer.py中的投资参数")
        
        print("\n注意事项:")
        print("- 系统需要网络连接获取数据")
        print("- 建议在工作时间使用，避免夜间频繁监控")
        print("- 高风险品种需要谨慎操作")
        
    else:
        print("\n✗ 部分模块测试失败")
        print("请检查依赖包是否正确安装")
        print("如果yfinance获取数据失败，可能需要检查网络连接")

if __name__ == "__main__":
    main()