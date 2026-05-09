#!/usr/bin/env python3
"""
全方位投资分析系统
整合港股、美股、新加坡股市、基金、ETF、期货和数字货币分析
"""

import sys
import os
import time
import json
from datetime import datetime
import argparse

from market_data_collector import MarketDataCollector
from market_monitor import MarketMonitor
from portfolio_optimizer import PortfolioOptimizer

class MultiMarketAnalysisSystem:
    """全方位投资分析系统"""
    
    def __init__(self):
        self.collector = MarketDataCollector()
        self.monitor = MarketMonitor()
        self.optimizer = PortfolioOptimizer()
        
        print("=== 全方位投资分析系统启动 ===")
        print("支持市场: 港股、美股、新加坡股市、基金、ETF、期货、数字货币")
    
    def run_analysis(self):
        """运行完整分析"""
        print("\n1. 收集市场数据...")
        all_data = self.collector.get_all_market_data()
        
        print("\n2. 监控市场状态...")
        self.monitor.monitor_once()
        
        print("\n3. 优化投资组合...")
        portfolio = self.optimizer.run_optimization()
        
        print("\n4. 生成综合报告...")
        self.generate_comprehensive_report(all_data, portfolio)
        
        print("\n=== 分析完成 ===")
        print("分析报告已生成，请查看:")
        print("- market_report_{timestamp}.txt")
        print("- monitor_results_{timestamp}.json")
        print("- portfolio_optimization_{timestamp}.txt")
        print("- portfolio_composition_{timestamp}.png")
        print("- portfolio_weights_{timestamp}.png")
    
    def generate_comprehensive_report(self, all_data, portfolio):
        """生成综合报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"comprehensive_report_{timestamp}.txt"
        
        report_content = f"""
=== 全方位投资分析报告 ===
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

一、市场状态分析:
"""
        
        market_summary = self.collector.generate_market_summary(all_data)
        
        for market_type, summary in market_summary.items():
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(market_type, market_type)
            
            report_content += f"""
{market_name}市场:
- 分析品种: {summary['count']}
- 平均价格: ${summary['avg_price']:.2f}
- 平均涨跌幅: {summary['avg_change']:.2f}%
"""
            
            # 涨幅前三
            report_content += f"""
涨幅前三品种:
"""
            for gainer in summary['top_gainers']:
                report_content += f"  {gainer['symbol']}: {gainer['change_percent']:.2f}% (价格: ${gainer['last_price']:.2f})\n"
            
            # 跌幅前三
            report_content += f"""
跌幅前三品种:
"""
            for loser in summary['top_losers']:
                report_content += f"  {loser['symbol']}: {loser['change_percent']:.2f}% (价格: ${loser['last_price']:.2f})\n"
        
        report_content += f"""
二、投资组合优化结果:
"""
        
        total_amount = sum([d['investment_amount'] for d in portfolio.values()])
        
        report_content += f"""
投资配置:
- 总投资额: ${self.optimizer.portfolio_config['total_investment']}
- 实际投资额: ${total_amount:.2f}
- 风险级别: {self.optimizer.portfolio_config['risk_level']}
"""
        
        # 按市场分组
        market_groups = {}
        for symbol, details in portfolio.items():
            market_type = details['market_type']
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(market_type, market_type)
            
            if market_name not in market_groups:
                market_groups[market_name] = []
            
            market_groups[market_name].append({
                'symbol': symbol,
                'weight': details['weight'],
                'investment_amount': details['investment_amount'],
                'score': details['score']
            })
        
        for market_name, items in market_groups.items():
            report_content += f"""
{market_name}投资:
"""
            
            market_total = sum([item['investment_amount'] for item in items])
            
            report_content += f"总投资额: ${market_total:.2f}\n"
            report_content += f"总权重: {(market_total / total_amount) * 100:.1f}%\n"
            report_content += f"""
品种详情:
"""
            
            for item in items:
                report_content += f"""
{item['symbol']}:
  - 权重: {item['weight'] * 100:.1f}%
  - 投资金额: ${item['investment_amount']:.2f}
  - 评分: {item['score']:.1f}
"""
        
        report_content += f"""
三、监控警报状态:
"""
        
        if self.monitor.alerts:
            report_content += f"""
当前警报:
"""
            for alert in self.monitor.alerts[:10]:
                report_content += f"""
[{alert['timestamp']}] {alert['type']}
品种: {alert['symbol']}
信息: {alert['message']}
"""
        else:
            report_content += f"""
当前无警报
"""
        
        report_content += f"""
四、投资建议:
"""
        
        # 技术分析建议
        technical_advice = []
        for market_type, data_list in all_data.items():
            if data_list:
                for data in data_list[:5]:
                    symbol = data['symbol']
                    tech = self.collector.analyze_technical(data)
                    trend = self.collector.analyze_trend(data)
                    
                    if tech and trend:
                        advice = ""
                        
                        if tech['rsi'] < 30:
                            advice += "RSI超卖，建议买入"
                        elif tech['rsi'] > 70:
                            advice += "RSI超买，建议卖出"
                        
                        if tech['macd_hist'] > 0:
                            advice += " MACD买入信号"
                        elif tech['macd_hist'] < 0:
                            advice += " MACD卖出信号"
                        
                        if trend['trend'] == '上涨趋势':
                            advice += " 处于上涨趋势"
                        elif trend['trend'] == '下跌趋势':
                            advice += " 处于下跌趋势"
                        
                        if advice:
                            technical_advice.append(f"{symbol}: {advice}")
        
        if technical_advice:
            report_content += f"""
技术分析建议:
"""
            for advice in technical_advice[:10]:
                report_content += f"- {advice}\n"
        
        # 投资组合建议
        portfolio_advice = """
投资组合建议:
1. 按优化权重配置投资
2. 关注高风险品种：期货和数字货币仓位不超过20%
3. 设置止损位：港股/美股 10%，ETF/基金 8%，期货/数字货币 15%
4. 定期再平衡：每周检查投资组合
"""
        
        report_content += portfolio_advice
        
        report_content += f"""
五、风险管理:
"""
        
        risk_management = """
风险控制措施:
1. 止损策略：
   - 港股/美股: 10%
   - ETF/基金: 8%
   - 期货: 15%
   - 数字货币: 20%

2. 仓位管理：
   - 单个品种不超过总投资额15%
   - 高风险品种不超过总投资额20%
   - 保持至少8个不同品种分散风险

3. 定期检查：
   - 每日监控市场警报
   - 每周重新优化投资组合
   - 每月检查技术指标变化

4. 市场切换：
   - 当某个市场整体下跌超过15%时，减少该市场仓位
   - 当某个市场整体上涨超过30%时，逐步减持
   - 保持20%现金仓位以备紧急情况
"""
        
        report_content += risk_management
        
        report_content += f"""
六、后续操作计划:
"""
        
        next_actions = """
操作计划:
1. 今天：
   - 按照优化投资组合开始分批买入
   - 设置价格和技术指标警报
   - 启动实时监控系统

2. 本周：
   - 每天检查市场警报
   - 跟踪技术指标变化
   - 关注市场新闻和政策变化

3. 本月：
   - 每周重新优化投资组合
   - 每月总结投资表现
   - 调整风险配置参数

4. 注意事项：
   - 不要一次性买入所有品种
   - 分批建仓降低风险
   - 设置止损位，严格执行
   - 关注全球宏观经济变化
"""
        
        report_content += next_actions
        
        report_content += f"""
=== 报告结束 ===
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"综合报告保存: {report_file}")
        
        return report_file
    
    def start_real_time_monitoring(self, interval_minutes=30):
        """启动实时监控"""
        print(f"启动实时监控系统，每{interval_minutes}分钟监控一次")
        
        # 启动监控系统
        self.monitor.start_monitoring(interval_minutes)
        
        print("监控系统已启动")
        print("按Ctrl+C停止监控")
    
    def update_config(self, total_investment=None, risk_level=None):
        """更新系统配置"""
        if total_investment:
            self.optimizer.portfolio_config['total_investment'] = total_investment
            print(f"总投资额更新为: ${total_investment}")
        
        if risk_level:
            if risk_level in ['conservative', 'moderate', 'aggressive']:
                self.optimizer.portfolio_config['risk_level'] = risk_level
                print(f"风险级别更新为: {risk_level}")
            else:
                print(f"无效的风险级别: {risk_level}")
                return
        
        # 更新monitor的价格警报
        if total_investment:
            # 可以根据总投资额调整警报阈值
            price_threshold_percent = 0.5
            threshold = total_investment * price_threshold_percent / 100000
            
            for market_type in ['hk_stocks', 'us_stocks', 'crypto']:
                for symbol in self.monitor.price_alerts_config[market_type]:
                    current_threshold = self.monitor.price_alerts_config[market_type][symbol]
                    updated_threshold = {
                        'buy': current_threshold['buy'] * threshold,
                        'sell': current_threshold['sell'] * threshold
                    }
                    self.monitor.price_alerts_config[market_type][symbol] = updated_threshold
        
        print("配置已更新")
    
    def generate_daily_report(self):
        """生成每日报告"""
        report_file = self.monitor.generate_daily_report()
        print(f"每日报告生成: {report_file}")
        
        return report_file
    
    def help(self):
        """显示帮助信息"""
        help_text = """
全方位投资分析系统使用说明:

命令:
1. python multi_market_analysis_system.py run
   - 运行完整分析

2. python multi_market_analysis_system.py monitor [interval]
   - 启动实时监控，interval为分钟数（默认30）

3. python multi_market_analysis_system.py optimize
   - 仅运行投资组合优化

4. python multi_market_analysis_system.py daily
   - 生成每日报告

5. python multi_market_analysis_system.py config total_investment risk_level
   - 更新系统配置

示例:
python multi_market_analysis_system.py run
python multi_market_analysis_system.py monitor 60
python multi_market_analysis_system.py optimize
python multi_market_analysis_system.py daily
python multi_market_analysis_system.py config 1000000 moderate

系统包含:
- MarketDataCollector: 数据收集
- MarketMonitor: 实时监控
- PortfolioOptimizer: 投资组合优化
"""
        
        print(help_text)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='全方位投资分析系统')
    parser.add_argument('command', choices=['run', 'monitor', 'optimize', 'daily', 'config', 'help'], help='执行命令')
    parser.add_argument('--interval', type=int, default=30, help='监控间隔（分钟）')
    parser.add_argument('--investment', type=int, help='总投资额')
    parser.add_argument('--risk', choices=['conservative', 'moderate', 'aggressive'], help='风险级别')
    
    args = parser.parse_args()
    
    system = MultiMarketAnalysisSystem()
    
    if args.command == 'run':
        system.run_analysis()
    
    elif args.command == 'monitor':
        system.start_real_time_monitoring(args.interval)
    
    elif args.command == 'optimize':
        portfolio = system.optimizer.run_optimization()
    
    elif args.command == 'daily':
        system.generate_daily_report()
    
    elif args.command == 'config':
        system.update_config(args.investment, args.risk)
    
    elif args.command == 'help':
        system.help()
    
    else:
        print("无效命令")
        system.help()

if __name__ == "__main__":
    main()