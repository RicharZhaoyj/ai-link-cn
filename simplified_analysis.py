#!/usr/bin/env python3
"""
简化版多市场分析系统 - 使用模拟数据
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import json

class SimplifiedMarketDataCollector:
    """简化版数据收集器 - 使用模拟数据"""
    
    def __init__(self):
        # 市场配置
        self.markets = {
            'hk_stocks': ['00700.HK', '00939.HK', '00005.HK'],
            'us_stocks': ['AAPL', 'MSFT', 'GOOGL'],
            'sg_stocks': ['D05.SI', 'U11.SI', 'O39.SI'],
            'etfs': ['SPY', 'QQQ', 'VTI'],
            'futures': ['GC=F', 'CL=F'],
            'funds': ['VOO', 'VGK', 'VWO'],
            'crypto': ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
        }
        
        # 设置中文显示
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_simulated_data(self, symbol, market_type):
        """生成模拟数据"""
        
        # 根据市场类型生成不同的数据
        if market_type == 'hk_stocks':
            # 港股波动较小
            base_price = np.random.uniform(100, 500)
            volatility = 0.02
        elif market_type == 'us_stocks':
            # 美股波动中等
            base_price = np.random.uniform(150, 350)
            volatility = 0.03
        elif market_type == 'sg_stocks':
            # 新加坡股市波动较小
            base_price = np.random.uniform(10, 50)
            volatility = 0.01
        elif market_type == 'etfs':
            # ETF波动较小
            base_price = np.random.uniform(400, 500)
            volatility = 0.01
        elif market_type == 'futures':
            # 期货波动较大
            base_price = np.random.uniform(50, 200)
            volatility = 0.05
        elif market_type == 'funds':
            # 基金波动较小
            base_price = np.random.uniform(80, 150)
            volatility = 0.01
        elif market_type == 'crypto':
            # 数字货币波动最大
            base_price = np.random.uniform(30000, 70000)
            volatility = 0.10
        else:
            base_price = np.random.uniform(100, 200)
            volatility = 0.03
        
        # 生成30天数据
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        
        # 生成随机价格序列
        prices = []
        for i in range(len(dates)):
            if i == 0:
                price = base_price
            else:
                change = np.random.normal(0, volatility)
                price = prices[-1] * (1 + change)
            prices.append(price)
        
        # 生成成交量
        volumes = np.random.uniform(1000000, 5000000, len(dates))
        
        df = pd.DataFrame({
            'date': dates,
            'Close': prices,
            'Volume': volumes
        })
        
        # 添加技术指标
        df['MA7'] = df['Close'].rolling(window=7).mean()
        df['MA30'] = df['Close'].rolling(window=30).mean()
        
        # RSI计算
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD计算
        ema12 = df['Close'].ewm(span=12).mean()
        ema26 = df['Close'].ewm(span=26).mean()
        df['MACD'] = ema12 - ema26
        df['MACD_signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_hist'] = df['MACD'] - df['MACD_signal']
        
        return {
            'symbol': symbol,
            'data': df,
            'last_price': df['Close'].iloc[-1],
            'volume': df['Volume'].iloc[-1],
            'change_percent': ((df['Close'].iloc[-1] - df['Close'].iloc[-7]) / df['Close'].iloc[-7]) * 100 if len(df) >= 7 else 0
        }
    
    def analyze_trend(self, data):
        """分析趋势"""
        df = data['data']
        prices = df['Close']
        
        ma7 = prices.rolling(window=7).mean()
        ma30 = prices.rolling(window=30).mean()
        
        trend = ''
        if ma7.iloc[-1] > ma30.iloc[-1]:
            trend = '上涨趋势'
        elif ma7.iloc[-1] < ma30.iloc[-1]:
            trend = '下跌趋势'
        else:
            trend = '横盘整理'
        
        return {
            'trend': trend,
            'ma7': ma7.iloc[-1],
            'ma30': ma30.iloc[-1],
            'trend_angle': ((ma7.iloc[-1] - ma7.iloc[-30]) / ma7.iloc[-30]) * 100 if len(ma7) >= 30 else None
        }
    
    def analyze_technical(self, data):
        """技术分析"""
        df = data['data']
        prices = df['Close']
        
        rsi = df['RSI'].iloc[-1]
        macd_hist = df['MACD_hist'].iloc[-1]
        
        # 布林带计算
        bb_middle = prices.rolling(window=20).mean()
        std = prices.rolling(window=20).std()
        bb_upper = bb_middle + 2 * std
        bb_lower = bb_middle - 2 * std
        
        return {
            'rsi': rsi,
            'macd_hist': macd_hist,
            'bb_upper': bb_upper.iloc[-1],
            'bb_lower': bb_lower.iloc[-1],
            'bb_middle': bb_middle.iloc[-1],
            'current_price': prices.iloc[-1],
            'price_position': ((prices.iloc[-1] - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])) * 100 if bb_upper.iloc[-1] > bb_lower.iloc[-1] else None
        }
    
    def get_all_market_data(self):
        """获取所有市场数据"""
        all_data = {
            'hk_stocks': [],
            'us_stocks': [],
            'sg_stocks': [],
            'etfs': [],
            'futures': [],
            'funds': [],
            'crypto': []
        }
        
        print("生成港股模拟数据...")
        for symbol in self.markets['hk_stocks']:
            all_data['hk_stocks'].append(self.generate_simulated_data(symbol, 'hk_stocks'))
        
        print("生成美股模拟数据...")
        for symbol in self.markets['us_stocks']:
            all_data['us_stocks'].append(self.generate_simulated_data(symbol, 'us_stocks'))
        
        print("生成新加坡股票模拟数据...")
        for symbol in self.markets['sg_stocks']:
            all_data['sg_stocks'].append(self.generate_simulated_data(symbol, 'sg_stocks'))
        
        print("生成ETF模拟数据...")
        for symbol in self.markets['etfs']:
            all_data['etfs'].append(self.generate_simulated_data(symbol, 'etfs'))
        
        print("生成期货模拟数据...")
        for symbol in self.markets['futures']:
            all_data['futures'].append(self.generate_simulated_data(symbol, 'futures'))
        
        print("生成基金模拟数据...")
        for symbol in self.markets['funds']:
            all_data['funds'].append(self.generate_simulated_data(symbol, 'funds'))
        
        print("生成数字货币模拟数据...")
        for symbol in self.markets['crypto']:
            all_data['crypto'].append(self.generate_simulated_data(symbol, 'crypto'))
        
        return all_data
    
    def generate_market_summary(self, all_data):
        """生成市场概况"""
        summary = {}
        
        for market_type, data_list in all_data.items():
            if data_list:
                prices = [d['last_price'] for d in data_list]
                changes = [d['change_percent'] for d in data_list]
                volumes = [d['volume'] for d in data_list]
                
                avg_price = sum(prices) / len(prices)
                avg_change = sum(changes) / len(changes)
                avg_volume = sum(volumes) / len(volumes)
                
                # 排序涨跌幅
                sorted_by_change = sorted(data_list, key=lambda x: x['change_percent'], reverse=True)
                top_gainers = sorted_by_change[:3]
                top_losers = sorted_by_change[-3:]
                
                summary[market_type] = {
                    'count': len(data_list),
                    'avg_price': avg_price,
                    'avg_change': avg_change,
                    'avg_volume': avg_volume,
                    'top_gainers': top_gainers,
                    'top_losers': top_losers
                }
        
        return summary
    
    def generate_portfolio_optimization(self, all_data):
        """生成投资组合优化"""
        portfolio = {}
        total_investment = 1000000
        
        # 市场权重配置
        market_weights = {
            'hk_stocks': 0.30,
            'us_stocks': 0.35,
            'sg_stocks': 0.10,
            'etfs': 0.15,
            'futures': 0.05,
            'funds': 0.10,
            'crypto': 0.20
        }
        
        print("生成投资组合优化...")
        
        for market_type, data_list in all_data.items():
            market_weight = market_weights[market_type]
            market_total = market_weight * total_investment
            
            # 为每个品种分配权重
            for i, data in enumerate(data_list):
                weight = market_weight / len(data_list)
                investment_amount = weight * total_investment
                
                # 技术分析评分
                tech_analysis = self.analyze_technical(data)
                trend_analysis = self.analyze_trend(data)
                
                score = 0
                if tech_analysis['rsi'] < 30:
                    score += 20
                elif tech_analysis['rsi'] > 70:
                    score -= 10
                
                if tech_analysis['macd_hist'] > 0:
                    score += 15
                
                if trend_analysis['trend'] == '上涨趋势':
                    score += 20
                
                portfolio[data['symbol']] = {
                    'weight': weight,
                    'market_type': market_type,
                    'score': score,
                    'investment_amount': investment_amount,
                    'current_price': tech_analysis['current_price'],
                    'change_percent': data['change_percent'],
                    'rsi': tech_analysis['rsi'],
                    'macd_hist': tech_analysis['macd_hist'],
                    'trend': trend_analysis['trend']
                }
        
        return portfolio
    
    def generate_report(self, all_data, summary, portfolio):
        """生成报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"simplified_report_{timestamp}.txt"
        
        report_content = f"""
=== 模拟市场分析报告 ===
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

注意：此报告使用模拟数据，用于测试系统功能

一、市场概况:
"""
        
        for market_type, market_summary in summary.items():
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
- 分析数量: {market_summary['count']}
- 平均价格: ${market_summary['avg_price']:.2f}
- 平均涨跌幅: {market_summary['avg_change']:.2f}%
"""
            
            if market_summary['top_gainers']:
                report_content += f"""
涨幅前三:
"""
                for gainer in market_summary['top_gainers']:
                    report_content += f"  {gainer['symbol']}: {gainer['change_percent']:.2f}% (价格: ${gainer['last_price']:.2f})\n"
            
            if market_summary['top_losers']:
                report_content += f"""
跌幅前三:
"""
                for loser in market_summary['top_losers']:
                    report_content += f"  {loser['symbol']}: {loser['change_percent']:.2f}% (价格: ${loser['last_price']:.2f})\n"
        
        report_content += f"""
二、投资组合优化:
总投资额: $1,000,000

各市场分配:
"""
        
        total_amount = sum([d['investment_amount'] for d in portfolio.values()])
        
        # 市场权重配置（复制generate_portfolio_optimization中的定义）
        market_weights_config = {
            'hk_stocks': 0.30,
            'us_stocks': 0.35,
            'sg_stocks': 0.10,
            'etfs': 0.15,
            'futures': 0.05,
            'funds': 0.10,
            'crypto': 0.20
        }
        
        for market_type, market_weight in market_weights_config.items():
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(market_type, market_type)
            
            market_symbols = [symbol for symbol, details in portfolio.items() if details['market_type'] == market_type]
            market_investment = sum([portfolio[symbol]['investment_amount'] for symbol in market_symbols])
            
            report_content += f"""
{market_name}:
- 权重: {market_weight * 100:.1f}%
- 投资金额: ${market_investment:.2f}
- 品种数量: {len(market_symbols)}
"""
            
            for symbol in market_symbols:
                details = portfolio[symbol]
                report_content += f"""
{symbol}:
  - 权重: {details['weight'] * 100:.1f}%
  - 投资金额: ${details['investment_amount']:.2f}
  - 评分: {details['score']:.1f}
  - 当前价格: ${details['current_price']:.2f}
  - 涨跌幅: {details['change_percent']:.2f}%
  - RSI: {details['rsi']:.1f}
  - MACD柱状图: {details['macd_hist']:.4f}
  - 趋势: {details['trend']}
"""
        
        report_content += f"""
三、投资建议:
1. 根据评分排序的投资建议：
"""
        
        sorted_portfolio = sorted(portfolio.items(), key=lambda x: x[1]['score'], reverse=True)
        
        for symbol, details in sorted_portfolio[:5]:
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(details['market_type'], details['market_type'])
            
            if details['score'] > 30:
                advice = "买入"
            elif details['score'] > 15:
                advice = "谨慎买入"
            elif details['score'] > 0:
                advice = "观望"
            else:
                advice = "卖出"
            
            report_content += f"""
{market_name} - {symbol}: {advice} (评分: {details['score']})
   - 投资金额: ${details['investment_amount']:.2f}
   - 当前价格: ${details['current_price']:.2f}
   - 技术指标: RSI {details['rsi']:.1f}, MACD {details['macd_hist']:.4f}
"""
        
        report_content += f"""
四、风险管理:
1. 止损位设置:
   - 港股/美股: 10%
   - ETF/基金: 8%
   - 期货: 15%
   - 数字货币: 20%

2. 仓位管理:
   - 单个品种不超过总投资额15%
   - 高风险品种不超过总投资额20%
   - 保持20%现金仓位以备紧急情况

3. 分批建仓建议:
   - 评分>30的品种: 立即买入
   - 评分15-30的品种: 分批买入
   - 评分<0的品种: 考虑卖出

=== 报告结束 ===
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"报告保存: {report_file}")
        
        return report_file
    
    def plot_portfolio_composition(self, portfolio):
        """绘制投资组合构成图"""
        # 按市场分组
        market_weights = {}
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
            
            if market_name not in market_weights:
                market_weights[market_name] = details['weight']
            else:
                market_weights[market_name] += details['weight']
        
        # 绘制饼图
        labels = list(market_weights.keys())
        weights = list(market_weights.values())
        
        plt.figure(figsize=(10, 6))
        plt.pie(weights, labels=labels, autopct='%1.1f%%')
        plt.title('投资组合市场分配')
        
        timestamp = datetime.now().strftime("%Y%m%d")
        chart_file = f"portfolio_composition_{timestamp}.png"
        plt.savefig(chart_file)
        plt.close()
        
        print(f"投资组合构成图保存: {chart_file}")
        
        return chart_file
    
    def run(self):
        """运行分析"""
        print("=== 模拟市场分析系统启动 ===")
        
        # 获取模拟数据
        all_data = self.get_all_market_data()
        
        # 生成市场概况
        summary = self.generate_market_summary(all_data)
        
        # 生成投资组合优化
        portfolio = self.generate_portfolio_optimization(all_data)
        
        # 生成报告
        report_file = self.generate_report(all_data, summary, portfolio)
        
        # 绘制图表
        chart_file = self.plot_portfolio_composition(portfolio)
        
        # 打印简要结果
        print("\n=== 分析结果摘要 ===")
        
        for market_type, market_summary in summary.items():
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(market_type, market_type)
            
            print(f"{market_name}: {market_summary['count']}个品种，平均涨跌幅: {market_summary['avg_change']:.2f}%")
        
        print(f"\n投资组合总结:")
        print(f"总投资额: $1,000,000")
        print(f"品种数量: {len(portfolio)}")
        
        # 计算总投资金额
        total_amount = sum([d['investment_amount'] for d in portfolio.values()])
        print(f"实际投资额: ${total_amount:.2f}")
        
        print(f"\n报告保存: {report_file}")
        print(f"图表保存: {chart_file}")
        
        print("\n=== 分析完成 ===")
        
        return all_data, portfolio

if __name__ == "__main__":
    analyzer = SimplifiedMarketDataCollector()
    analyzer.run()