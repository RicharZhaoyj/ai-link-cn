#!/usr/bin/env python3
"""
投资组合优化器 - 构建和管理跨市场投资组合
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from market_data_collector import MarketDataCollector

class PortfolioOptimizer:
    """投资组合优化器"""
    
    def __init__(self):
        self.collector = MarketDataCollector()
        self.portfolio = {}  # 当前投资组合
        self.target_portfolio = {}  # 目标投资组合
        
        # 投资组合配置
        self.portfolio_config = {
            'total_investment': 1000000,  # 总投资额
            'asset_classes': {
                'hk_stocks': {'max_weight': 0.30},  # 港股最大权重30%
                'us_stocks': {'max_weight': 0.35},  # 美股最大权重35%
                'sg_stocks': {'max_weight': 0.10},  # 新加坡股票最大权重10%
                'etfs': {'max_weight': 0.15},  # ETF最大权重15%
                'futures': {'max_weight': 0.05},  # 期货最大权重5%
                'funds': {'max_weight': 0.10},  # 基金最大权重10%
                'crypto': {'max_weight': 0.20},  # 数字货币最大权重20%
            },
            'risk_level': 'moderate',  # 风险级别
            'investment_horizon': 'medium',  # 投资期限
            'diversification_min': 8,  # 最少分散品种数量
        }
        
        # 风险参数
        self.risk_params = {
            'conservative': {
                'max_weight_single': 0.10,  # 单个品种最大权重
                'max_loss_tolerance': 0.05,  # 最大亏损容忍度
                'min_correlation': 0.3,  # 最小相关系数
                'rebalance_frequency': 'monthly',  # 再平衡频率
            },
            'moderate': {
                'max_weight_single': 0.15,  # 单个品种最大权重
                'max_loss_tolerance': 0.10,  # 最大亏损容忍度
                'min_correlation': 0.2,  # 最小相关系数
                'rebalance_frequency': 'weekly',  # 再平衡频率
            },
            'aggressive': {
                'max_weight_single': 0.25,  # 单个品种最大权重
                'max_loss_tolerance': 0.20,  # 最大亏损容忍度
                'min_correlation': 0.1,  # 最小相关系数
                'rebalance_frequency': 'daily',  # 再平衡频率
            }
        }
        
    def analyze_correlation(self, all_data):
        """分析相关性"""
        correlations = {}
        
        for market_type, data_list in all_data.items():
            if data_list:
                # 提取价格序列
                price_series = {}
                for data in data_list[:10]:  # 分析前10个品种
                    symbol = data['symbol']
                    if 'data' in data:
                        df = data['data']
                        if isinstance(df, pd.DataFrame):
                            if 'Close' in df.columns:
                                price_series[symbol] = df['Close']
                            elif 'close' in df.columns:
                                price_series[symbol] = df['close']
                
                # 计算相关性矩阵
                if len(price_series) > 1:
                    price_df = pd.DataFrame(price_series)
                    correlation_matrix = price_df.corr()
                    
                    # 提取高相关性品种
                    high_corr = []
                    for i in range(len(correlation_matrix.columns)):
                        for j in range(i+1, len(correlation_matrix.columns)):
                            col1 = correlation_matrix.columns[i]
                            col2 = correlation_matrix.columns[j]
                            corr_value = correlation_matrix.iloc[i, j]
                            if corr_value > 0.7:
                                high_corr.append((col1, col2, corr_value))
                    
                    correlations[market_type] = {
                        'matrix': correlation_matrix,
                        'high_corr': high_corr,
                        'avg_corr': correlation_matrix.mean().mean()
                    }
        
        return correlations
    
    def calculate_returns(self, all_data):
        """计算回报率"""
        returns = {}
        
        for market_type, data_list in all_data.items():
            if data_list:
                market_returns = []
                for data in data_list[:10]:
                    symbol = data['symbol']
                    if 'data' in data:
                        df = data['data']
                        if isinstance(df, pd.DataFrame):
                            if 'Close' in df.columns:
                                prices = df['Close']
                            elif 'close' in df.columns:
                                prices = df['close']
                            
                            if len(prices) >= 30:
                                # 计算30天回报率
                                return_30d = (prices.iloc[-1] - prices.iloc[-30]) / prices.iloc[-30]
                                # 计算7天回报率
                                return_7d = (prices.iloc[-1] - prices.iloc[-7]) / prices.iloc[-7]
                                
                                market_returns.append({
                                    'symbol': symbol,
                                    'return_7d': return_7d,
                                    'return_30d': return_30d,
                                })
                
                returns[market_type] = market_returns
        
        return returns
    
    def calculate_risk_metrics(self, all_data):
        """计算风险指标"""
        risk_metrics = {}
        
        for market_type, data_list in all_data.items():
            if data_list:
                volatilities = []
                for data in data_list[:10]:
                    symbol = data['symbol']
                    if 'data' in data:
                        df = data['data']
                        if isinstance(df, pd.DataFrame):
                            if 'Close' in df.columns:
                                prices = df['Close']
                            elif 'close' in df.columns:
                                prices = df['close']
                            
                            # 计算波动率（标准差）
                            volatility = prices.std()
                            volatilities.append({
                                'symbol': symbol,
                                'volatility': volatility,
                                'volatility_ratio': volatility / prices.mean()
                            })
                
                risk_metrics[market_type] = volatilities
        
        return risk_metrics
    
    def optimize_portfolio(self, all_data, returns_data, risk_data):
        """优化投资组合"""
        # 风险等级参数
        risk_params = self.risk_params[self.portfolio_config['risk_level']]
        
        # 候选品种
        candidates = []
        
        for market_type, data_list in all_data.items():
            if data_list:
                market_weight = self.portfolio_config['asset_classes'][market_type]['max_weight']
                
                for data in data_list[:20]:
                    symbol = data['symbol']
                    tech_analysis = self.collector.analyze_technical(data)
                    trend_analysis = self.collector.analyze_trend(data)
                    
                    if tech_analysis and trend_analysis:
                        # 计算品种评分
                        score = 0
                        
                        # 回报率加分
                        for returns in returns_data[market_type]:
                            if returns['symbol'] == symbol:
                                score += returns['return_7d'] * 100
                                score += returns['return_30d'] * 50
        
                        # 技术指标加分
                        if tech_analysis['rsi'] < 30:
                            score += 20  # 超卖买入机会
                        elif tech_analysis['rsi'] > 70:
                            score -= 10  # 超买风险
        
                        if tech_analysis['macd_hist'] > 0:
                            score += 15  # MACD买入信号
        
                        if trend_analysis['trend'] == '上涨趋势':
                            score += 20
                        
                        # 风险调整（波动率低的加分）
                        for risk in risk_data[market_type]:
                            if risk['symbol'] == symbol:
                                if risk['volatility_ratio'] < 0.05:
                                    score += 10
                                elif risk['volatility_ratio'] < 0.1:
                                    score += 5
        
                        # 相关性调整（避免高度相关）
                        # 这里需要考虑相关性矩阵
        
                        candidates.append({
                            'symbol': symbol,
                            'market_type': market_type,
                            'score': score,
                            'current_price': tech_analysis['current_price'],
                            'weight': market_weight / 10,  # 初始权重（后期优化）
                            'volatility': risk['volatility_ratio'] if risk['symbol'] == symbol else None
                        })
        
        # 按评分排序
        sorted_candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)
        
        # 构建优化组合
        optimized_portfolio = {}
        total_score = sum([c['score'] for c in sorted_candidates[:self.portfolio_config['diversification_min']]])
        
        for candidate in sorted_candidates[:self.portfolio_config['diversification_min']]:
            # 计算权重（基于评分）
            weight = (candidate['score'] / total_score) * self.portfolio_config['asset_classes'][candidate['market_type']]['max_weight']
            
            # 限制单个品种权重
            if weight > risk_params['max_weight_single']:
                weight = risk_params['max_weight_single']
            
            optimized_portfolio[candidate['symbol']] = {
                'weight': weight,
                'market_type': candidate['market_type'],
                'score': candidate['score'],
                'current_price': candidate['current_price'],
                'investment_amount': weight * self.portfolio_config['total_investment'],
                'volatility': candidate['volatility']
            }
        
        # 调整权重，确保各市场比例符合配置
        final_portfolio = {}
        market_weights = {}
        
        for symbol, details in optimized_portfolio.items():
            market_type = details['market_type']
            
            if market_type not in market_weights:
                market_weights[market_type] = details['weight']
            else:
                market_weights[market_type] += details['weight']
        
        # 调整权重（如果某个市场超过配置上限）
        for market_type, current_weight in market_weights.items():
            max_weight = self.portfolio_config['asset_classes'][market_type]['max_weight']
            
            if current_weight > max_weight:
                # 需要减权
                reduction_factor = max_weight / current_weight
                
                for symbol, details in optimized_portfolio.items():
                    if details['market_type'] == market_type:
                        details['weight'] *= reduction_factor
                        details['investment_amount'] = details['weight'] * self.portfolio_config['total_investment']
        
        # 汇总投资金额
        total_investment = sum([d['investment_amount'] for d in optimized_portfolio.values()])
        
        # 如果总投资小于配置金额，重新分配
        if total_investment < self.portfolio_config['total_investment']:
            remaining = self.portfolio_config['total_investment'] - total_investment
            
            # 分配给评分最高的品种
            top_symbol = sorted_candidates[0]['symbol']
            if top_symbol in optimized_portfolio:
                optimized_portfolio[top_symbol]['investment_amount'] += remaining
                optimized_portfolio[top_symbol]['weight'] = optimized_portfolio[top_symbol]['investment_amount'] / self.portfolio_config['total_investment']
        
        return optimized_portfolio
    
    def generate_portfolio_report(self, portfolio):
        """生成投资组合报告"""
        timestamp = datetime.now().strftime("%Y%m%d")
        report_file = f"portfolio_optimization_{timestamp}.txt"
        
        report_content = f"""
=== 投资组合优化报告 ===
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

投资配置:
- 总投资额: ${self.portfolio_config['total_investment']}
- 风险级别: {self.portfolio_config['risk_level']}
- 投资期限: {self.portfolio_config['investment_horizon']}
- 最少分散品种: {self.portfolio_config['diversification_min']}

各市场最大权重配置:
"""
        
        for market_type, config in self.portfolio_config['asset_classes'].items():
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(market_type, market_type)
            
            report_content += f"- {market_name}: {config['max_weight'] * 100}%\n"
        
        report_content += f"""
风险参数 ({self.portfolio_config['risk_level']}):
"""
        
        for param, value in self.risk_params[self.portfolio_config['risk_level']].items():
            param_name = {
                'max_weight_single': '单个品种最大权重',
                'max_loss_tolerance': '最大亏损容忍度',
                'min_correlation': '最小相关系数',
                'rebalance_frequency': '再平衡频率'
            }.get(param, param)
            
            report_content += f"- {param_name}: {value}\n"
        
        report_content += f"""
优化投资组合:
"""
        
        total_amount = sum([d['investment_amount'] for d in portfolio.values()])
        total_weight = sum([d['weight'] for d in portfolio.values()])
        
        # 按市场类型分组
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
                'score': details['score'],
                'current_price': details['current_price']
            })
        
        for market_name, items in market_groups.items():
            report_content += f"""
{market_name}投资:
"""
            
            for item in items:
                report_content += f"""
{item['symbol']}:
  - 权重: {item['weight'] * 100:.1f}%
  - 投资金额: ${item['investment_amount']:.2f}
  - 评分: {item['score']:.1f}
  - 当前价格: ${item['current_price']:.2f}
"""
        
        report_content += f"""
投资组合总结:
- 总投资额: ${total_amount:.2f}
- 总权重: {total_weight * 100:.1f}%
- 品种数量: {len(portfolio)}

风险管理建议:
"""
        
        if self.portfolio_config['risk_level'] == 'conservative':
            report_content += """
保守型策略建议:
1. 止损设置: 单品种亏损超过5%时止损
2. 仓位管理: 单个品种不超过10%
3. 分批建仓: 分3次入场
4. 定期调整: 每月再平衡
"""
        elif self.portfolio_config['risk_level'] == 'moderate':
            report_content += """
平衡型策略建议:
1. 止损设置: 单品种亏损超过10%时止损
2. 仓位管理: 单个品种不超过15%
3. 分批建仓: 分2次入场
4. 定期调整: 每周再平衡
"""
        else:
            report_content += """
激进型策略建议:
1. 止损设置: 单品种亏损超过20%时止损
2. 仓位管理: 单个品种不超过25%
3. 分批建仓: 分1次入场
4. 定期调整: 每日再平衡
"""
        
        report_content += f"""
执行建议:
1. 按建议权重分批买入
2. 关注每日监控系统的警报
3. 定期检查技术指标变化
4. 关注市场宏观经济变化

=== 报告结束 ===
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"投资组合报告保存: {report_file}")
        
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
        
        # 绘制品种权重图
        symbols = list(portfolio.keys())
        weights = [portfolio[s]['weight'] * 100 for s in symbols]
        
        plt.figure(figsize=(12, 8))
        plt.barh(symbols, weights)
        plt.xlabel('权重 (%)')
        plt.title('投资组合品种权重')
        
        chart_file2 = f"portfolio_weights_{timestamp}.png"
        plt.savefig(chart_file2)
        plt.close()
        
        print(f"投资组合权重图保存: {chart_file2}")
        
        return chart_file, chart_file2
    
    def run_optimization(self):
        """运行投资组合优化"""
        print("=== 开始投资组合优化 ===")
        
        # 获取市场数据
        all_data = self.collector.get_all_market_data()
        
        # 分析相关性
        correlations = self.analyze_correlation(all_data)
        
        # 计算回报率
        returns = self.calculate_returns(all_data)
        
        # 计算风险指标
        risk_metrics = self.calculate_risk_metrics(all_data)
        
        # 优化投资组合
        optimized_portfolio = self.optimize_portfolio(all_data, returns, risk_metrics)
        
        # 生成报告
        report_file = self.generate_portfolio_report(optimized_portfolio)
        
        # 绘制图表
        chart_files = self.plot_portfolio_composition(optimized_portfolio)
        
        # 打印优化结果
        print("\n=== 投资组合优化结果 ===")
        print(f"总品种数: {len(optimized_portfolio)}")
        
        for market_type, config in self.portfolio_config['asset_classes'].items():
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(market_type, market_type)
            
            # 计算该市场的总投资
            market_investment = sum([d['investment_amount'] for d in optimized_portfolio.values() if d['market_type'] == market_type])
            market_weight = market_investment / self.portfolio_config['total_investment']
            
            print(f"{market_name}: {market_weight * 100:.1f}% (${market_investment:.2f})")
        
        print(f"\n投资组合报告保存: {report_file}")
        print(f"图表保存: {chart_files[0]}, {chart_files[1]}")
        
        return optimized_portfolio
    
    def rebalance_portfolio(self, current_portfolio):
        """重新平衡投资组合"""
        print("=== 开始投资组合再平衡 ===")
        
        # 获取当前市场数据
        all_data = self.collector.get_all_market_data()
        
        # 检查每个品种的当前表现
        for symbol, details in current_portfolio.items():
            market_type = details['market_type']
            
            # 查找当前数据
            for data in all_data[market_type]:
                if data['symbol'] == symbol:
                    tech_analysis = self.collector.analyze_technical(data)
                    trend_analysis = self.collector.analyze_trend(data)
                    
                    if tech_analysis and trend_analysis:
                        # 检查是否需要调整权重
                        new_score = 0
                        
                        # 技术指标评分
                        if tech_analysis['rsi'] < 30:
                            new_score += 20
                        elif tech_analysis['rsi'] > 70:
                            new_score -= 10
                        
                        if tech_analysis['macd_hist'] > 0:
                            new_score += 15
                        
                        if trend_analysis['trend'] == '上涨趋势':
                            new_score += 20
                        
                        # 比较新旧评分
                        old_score = details['score']
                        
                        if new_score > old_score + 20:
                            print(f"{symbol}: 评分显著提升 ({old_score} → {new_score}), 建议增加权重")
                        elif new_score < old_score - 20:
                            print(f"{symbol}: 评分显著下降 ({old_score} → {new_score}), 建议减少权重")
        
        # 重新运行优化
        returns = self.calculate_returns(all_data)
        risk_metrics = self.calculate_risk_metrics(all_data)
        optimized_portfolio = self.optimize_portfolio(all_data, returns, risk_metrics)
        
        return optimized_portfolio

if __name__ == "__main__":
    optimizer = PortfolioOptimizer()
    
    # 运行投资组合优化
    portfolio = optimizer.run_optimization()
    
    print("\n=== 使用方法 ===")
    print("1. optimizer.run_optimization() - 运行投资组合优化")
    print("2. optimizer.rebalance_portfolio(current_portfolio) - 重新平衡投资组合")
    print("3. 修改portfolio_config调整配置参数")