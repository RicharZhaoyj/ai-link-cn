#!/usr/bin/env python3
"""
多市场实时监控系统 - 监控港股、美股、新加坡股市、基金、ETF、期货和数字货币
支持实时警报和自动化分析
"""

import time
import json
import schedule
from datetime import datetime, timedelta
from market_data_collector import MarketDataCollector
import pandas as pd
import numpy as np

class MarketMonitor:
    """多市场实时监控器"""
    
    def __init__(self):
        self.collector = MarketDataCollector()
        self.alerts = []  # 警报列表
        self.alert_thresholds = {
            'price_change': 5.0,  # 价格变化超过5%触发警报
            'volume_change': 50.0,  # 成交量变化超过50%触发警报
            'technical_alert': {
                'rsi_threshold': 30,  # RSI低于30触发买入警报
                'rsi_overheat': 70,  # RSI高于70触发卖出警报
                'macd_threshold': 0.1,  # MACD柱状图超过阈值触发警报
            }
        }
        
        self.historical_data = {}
        
        # 价格警报配置文件
        self.price_alerts_config = {
            'hk_stocks': {
                '00700.HK': {'buy': 300, 'sell': 400},  # 腾讯控股
                '00939.HK': {'buy': 4.5, 'sell': 5.5},  # 建设银行
                '00005.HK': {'buy': 60, 'sell': 70},  # 汇丰控股
            },
            'us_stocks': {
                'AAPL': {'buy': 150, 'sell': 180},  # 苹果
                'MSFT': {'buy': 350, 'sell': 420},  # 微软
                'GOOGL': {'buy': 130, 'sell': 160},  # 谷歌
            },
            'crypto': {
                'BTC/USDT': {'buy': 65000, 'sell': 75000},  # 比特币
                'ETH/USDT': {'buy': 3500, 'sell': 4500},  # 以太坊
                'SOL/USDT': {'buy': 150, 'sell': 200},  # Solana
            }
        }
        
        # 支持的分析频率
        self.analysis_frequency = {
            'real_time': 30,  # 30秒
            'hourly': 3600,  # 每小时
            'daily': 86400,  # 每天
            'weekly': 604800,  # 每周
        }
        
        print("=== 多市场实时监控系统启动 ===")
        
    def check_price_alert(self, symbol, current_price, market_type):
        """检查价格警报"""
        if market_type in self.price_alerts_config and symbol in self.price_alerts_config[market_type]:
            thresholds = self.price_alerts_config[market_type][symbol]
            
            if current_price <= thresholds['buy']:
                alert_type = '买入警报'
                alert_message = f"{symbol} 价格已跌至买入价位 ${current_price}"
            elif current_price >= thresholds['sell']:
                alert_type = '卖出警报'
                alert_message = f"{symbol} 价格已涨至卖出价位 ${current_price}"
            else:
                return
            
            alert = {
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'type': alert_type,
                'message': alert_message,
                'current_price': current_price,
                'threshold': thresholds[alert_type.split('警报')[0]],
                'market_type': market_type
            }
            
            self.alerts.append(alert)
            print(f"⚠️ {alert_type}: {alert_message}")
            
            # 保存警报到文件
            self.save_alert_to_file(alert)
    
    def check_technical_alert(self, symbol, technical_data, market_type):
        """检查技术指标警报"""
        rsi = technical_data.get('rsi')
        macd_hist = technical_data.get('macd_hist')
        
        if rsi is not None:
            if rsi < self.alert_thresholds['technical_alert']['rsi_threshold']:
                alert_type = 'RSI买入信号'
                alert_message = f"{symbol} RSI低于{self.alert_thresholds['technical_alert']['rsi_threshold']} (当前: {rsi:.1f}) - 超卖状态"
                
                alert = {
                    'timestamp': datetime.now().isoformat(),
                    'symbol': symbol,
                    'type': alert_type,
                    'message': alert_message,
                    'current_rsi': rsi,
                    'market_type': market_type
                }
                
                self.alerts.append(alert)
                print(f"⚠️ {alert_type}: {alert_message}")
                self.save_alert_to_file(alert)
            
            elif rsi > self.alert_thresholds['technical_alert']['rsi_overheat']:
                alert_type = 'RSI卖出信号'
                alert_message = f"{symbol} RSI高于{self.alert_thresholds['technical_alert']['rsi_overheat']} (当前: {rsi:.1f}) - 超买状态"
                
                alert = {
                    'timestamp': datetime.now().isoformat(),
                    'symbol': symbol,
                    'type': alert_type,
                    'message': alert_message,
                    'current_rsi': rsi,
                    'market_type': market_type
                }
                
                self.alerts.append(alert)
                print(f"⚠️ {alert_type}: {alert_message}")
                self.save_alert_to_file(alert)
        
        if macd_hist is not None:
            if abs(macd_hist) > self.alert_thresholds['technical_alert']['macd_threshold']:
                if macd_hist > 0:
                    alert_type = 'MACD买入信号'
                else:
                    alert_type = 'MACD卖出信号'
                
                alert_message = f"{symbol} MACD柱状图突破阈值 (当前: {macd_hist:.4f})"
                
                alert = {
                    'timestamp': datetime.now().isoformat(),
                    'symbol': symbol,
                    'type': alert_type,
                    'message': alert_message,
                    'current_macd': macd_hist,
                    'market_type': market_type
                }
                
                self.alerts.append(alert)
                print(f"⚠️ {alert_type}: {alert_message}")
                self.save_alert_to_file(alert)
    
    def check_volume_alert(self, symbol, current_volume, historical_volume, market_type):
        """检查成交量警报"""
        if historical_volume and current_volume > historical_volume * 1.5:
            alert_type = '成交量放大'
            alert_message = f"{symbol} 成交量放大超过50% (当前: {current_volume:.2f}, 历史平均: {historical_volume:.2f})"
            
            alert = {
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'type': alert_type,
                'message': alert_message,
                'current_volume': current_volume,
                'historical_volume': historical_volume,
                'market_type': market_type
            }
            
            self.alerts.append(alert)
            print(f"⚠️ {alert_type}: {alert_message}")
            self.save_alert_to_file(alert)
    
    def save_alert_to_file(self, alert):
        """保存警报到文件"""
        timestamp = datetime.now().strftime("%Y%m%d")
        alert_file = f"market_alerts_{timestamp}.txt"
        
        with open(alert_file, 'a', encoding='utf-8') as f:
            alert_str = f"""
[警报] {alert['timestamp']}
类型: {alert['type']}
市场: {alert['market_type']}
品种: {alert['symbol']}
信息: {alert['message']}
"""
            if 'current_price' in alert:
                alert_str += f"当前价格: {alert['current_price']}\n"
            if 'threshold' in alert:
                alert_str += f"阈值: {alert['threshold']}\n"
            if 'current_rsi' in alert:
                alert_str += f"当前RSI: {alert['current_rsi']}\n"
            if 'current_macd' in alert:
                alert_str += f"当前MACD: {alert['current_macd']}\n"
            if 'current_volume' in alert:
                alert_str += f"当前成交量: {alert['current_volume']}\n"
            if 'historical_volume' in alert:
                alert_str += f"历史成交量: {alert['historical_volume']}\n"
            
            alert_str += "\n"
            f.write(alert_str)
    
    def analyze_market_health(self, all_data):
        """分析市场健康状况"""
        market_health = {}
        
        for market_type, data_list in all_data.items():
            if data_list:
                # 计算平均涨跌幅
                avg_change = sum([d['change_percent'] for d in data_list]) / len(data_list)
                
                # 计算上涨/下跌比例
                positive_count = sum([1 for d in data_list if d['change_percent'] > 0])
                negative_count = sum([1 for d in data_list if d['change_percent'] < 0])
                
                # 计算技术指标状态
                bullish_count = 0
                bearish_count = 0
                
                for d in data_list:
                    tech = self.collector.analyze_technical(d)
                    if tech:
                        if tech['macd_hist'] > 0:
                            bullish_count += 1
                        else:
                            bearish_count += 1
                
                health_score = 0
                if avg_change > 0:
                    health_score += 20
                if positive_count > negative_count:
                    health_score += 20
                if bullish_count > bearish_count:
                    health_score += 20
                if avg_change > 1:  # 平均涨幅大于1%
                    health_score += 10
                
                market_health[market_type] = {
                    'health_score': health_score,
                    'avg_change': avg_change,
                    'positive_rate': positive_count / len(data_list) * 100,
                    'negative_rate': negative_count / len(data_list) * 100,
                    'bullish_rate': bullish_count / len(data_list) * 100,
                    'bearish_rate': bearish_count / len(data_list) * 100,
                    'status': '健康' if health_score >= 50 else '谨慎' if health_score >= 30 else '危险'
                }
        
        return market_health
    
    def generate_recommendations(self, all_data, market_health):
        """生成投资建议"""
        recommendations = []
        
        # 寻找最具潜力的品种
        for market_type, data_list in all_data.items():
            if data_list:
                # 排序：涨幅大 + RSI低位 + MACD转正
                sorted_data = sorted(data_list, key=lambda x: 
                    abs(x['change_percent']) * 0.3 + 
                    self.collector.analyze_technical(x).get('rsi', 50) * 0.7, 
                    reverse=True)
                
                for data in sorted_data[:3]:
                    symbol = data['symbol']
                    tech = self.collector.analyze_technical(data)
                    trend = self.collector.analyze_trend(data)
                    
                    if tech and trend:
                        recommendation_score = 0
                        
                        if tech['rsi'] < self.alert_thresholds['technical_alert']['rsi_threshold']:
                            recommendation_score += 30
                        if tech['macd_hist'] > 0:
                            recommendation_score += 20
                        if trend['trend'] == '上涨趋势':
                            recommendation_score += 20
                        if data['change_percent'] > 0:
                            recommendation_score += 10
                        
                        if recommendation_score >= 50:
                            recommendations.append({
                                'symbol': symbol,
                                'market_type': market_type,
                                'score': recommendation_score,
                                'current_price': tech['current_price'],
                                'change_percent': data['change_percent'],
                                'rsi': tech['rsi'],
                                'macd_hist': tech['macd_hist'],
                                'trend': trend['trend'],
                                'recommendation': '买入'
                            })
                        elif recommendation_score >= 30:
                            recommendations.append({
                                'symbol': symbol,
                                'market_type': market_type,
                                'score': recommendation_score,
                                'current_price': tech['current_price'],
                                'change_percent': data['change_percent'],
                                'rsi': tech['rsi'],
                                'macd_hist': tech['macd_hist'],
                                'trend': trend['trend'],
                                'recommendation': '谨慎关注'
                            })
        
        return recommendations
    
    def monitor_once(self):
        """执行一次监控"""
        print(f"\n=== 执行实时监控 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        
        # 获取市场数据
        all_data = self.collector.get_all_market_data()
        
        # 检查警报
        print("检查价格和技术指标警报...")
        for market_type, data_list in all_data.items():
            if data_list:
                for data in data_list[:10]:  # 检查前10个品种
                    symbol = data['symbol']
                    
                    # 价格警报
                    self.check_price_alert(symbol, data['last_price'], market_type)
                    
                    # 技术指标警报
                    technical_data = self.collector.analyze_technical(data)
                    if technical_data:
                        self.check_technical_alert(symbol, technical_data, market_type)
                    
                    # 成交量警报（如果有历史数据）
                    if symbol in self.historical_data:
                        historical_volume = self.historical_data[symbol]['volume']
                        self.check_volume_alert(symbol, data['volume'], historical_volume, market_type)
        
        # 分析市场健康状况
        market_health = self.analyze_market_health(all_data)
        
        print("\n=== 市场健康状况 ===")
        for market_type, health in market_health.items():
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(market_type, market_type)
            
            print(f"{market_name}: 健康度{health['health_score']} ({health['status']})")
            print(f"  平均涨跌幅: {health['avg_change']:.2f}%")
            print(f"  上涨比例: {health['positive_rate']:.1f}%")
            print(f"  看涨比例: {health['bullish_rate']:.1f}%")
        
        # 生成投资建议
        recommendations = self.generate_recommendations(all_data, market_health)
        
        print("\n=== 投资建议 ===")
        for recommendation in recommendations[:5]:
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(recommendation['market_type'], recommendation['market_type'])
            
            print(f"{market_name} - {recommendation['symbol']}: {recommendation['recommendation']} (评分: {recommendation['score']})")
            print(f"  价格: {recommendation['current_price']:.2f}, 涨跌幅: {recommendation['change_percent']:.2f}%")
            print(f"  RSI: {recommendation['rsi']:.1f}, MACD: {recommendation['macd_hist']:.4f}")
            print(f"  趋势: {recommendation['trend']}")
        
        # 保存历史数据
        for market_type, data_list in all_data.items():
            for data in data_list[:20]:
                symbol = data['symbol']
                self.historical_data[symbol] = {
                    'volume': data['volume'],
                    'last_price': data['last_price'],
                    'timestamp': datetime.now().isoformat()
                }
        
        # 保存本次监控结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"monitor_results_{timestamp}.json"
        
        with open(result_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'alerts': self.alerts,
                'market_health': market_health,
                'recommendations': recommendations,
                'historical_data': self.historical_data
            }, f, indent=4)
        
        print(f"\n监控结果保存: {result_file}")
        print(f"警报总数: {len(self.alerts)}")
        
        # 清理旧的警报
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
        
        return all_data
    
    def start_monitoring(self, interval_minutes=30):
        """启动定时监控"""
        print(f"启动定时监控系统，每{interval_minutes}分钟执行一次")
        
        def scheduled_monitor():
            self.monitor_once()
        
        schedule.every(interval_minutes).minutes.do(scheduled_monitor)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("监控停止")
    
    def stop_monitoring(self):
        """停止监控"""
        schedule.clear()
        print("定时监控已停止")
    
    def generate_daily_report(self):
        """生成每日报告"""
        print("生成每日投资分析报告...")
        
        # 获取全天数据
        all_data = self.collector.get_all_market_data()
        market_health = self.analyze_market_health(all_data)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        report_file = f"daily_report_{timestamp}.txt"
        
        report_content = f"""
=== 每日投资分析报告 ===
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

一、全天市场概况:
"""
        
        for market_type, health in market_health.items():
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
- 健康度评分: {health['health_score']} ({health['status']})
- 平均涨跌幅: {health['avg_change']:.2f}%
- 上涨比例: {health['positive_rate']:.1f}%
- 下跌比例: {health['negative_rate']:.1f}%
- 看涨比例: {health['bullish_rate']:.1f}%
- 看跌比例: {health['bearish_rate']:.1f}%
"""
        
        # 全天警报总结
        report_content += f"""
二、全天警报统计:
"""
        
        alert_stats = {}
        for alert in self.alerts:
            market_type = alert['market_type']
            alert_type = alert['type']
            
            if market_type not in alert_stats:
                alert_stats[market_type] = {}
            
            if alert_type not in alert_stats[market_type]:
                alert_stats[market_type][alert_type] = 0
            
            alert_stats[market_type][alert_type] += 1
        
        for market_type, stats in alert_stats.items():
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
{market_name}市场警报统计:
"""
            
            for alert_type, count in stats.items():
                report_content += f"- {alert_type}: {count}次\n"
        
        # 全天推荐汇总
        report_content += f"""
三、全天投资建议汇总:
"""
        
        recommendations = self.generate_recommendations(all_data, market_health)
        
        for recommendation in recommendations[:10]:
            market_name = {
                'hk_stocks': '港股',
                'us_stocks': '美股',
                'sg_stocks': '新加坡股市',
                'etfs': 'ETF',
                'futures': '期货',
                'funds': '基金',
                'crypto': '数字货币'
            }.get(recommendation['market_type'], recommendation['market_type'])
            
            report_content += f"""
{market_name} - {recommendation['symbol']}:
- 建议: {recommendation['recommendation']}
- 评分: {recommendation['score']}
- 价格: {recommendation['current_price']:.2f}
- 涨跌幅: {recommendation['change_percent']:.2f}%
- RSI: {recommendation['rsi']:.1f}
- MACD: {recommendation['macd_hist']:.4f}
"""
        
        # 明日关注重点
        report_content += f"""
四、明日关注重点:
1. 重点关注评分 > 60的品种
2. 注意市场健康度评分变化
3. 关注重要政策和经济数据发布
4. 关注主要品种的技术指标变化

五、风险管理:
1. 止损位建议:
   - 港股/美股: 10%
   - ETF/基金: 8%
   - 期货: 15%
   - 数字货币: 20%
2. 仓位管理: 单品种不超过总投资额的20%
3. 风险分散: 至少配置5个不同品种

=== 报告结束 ===
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"每日报告保存: {report_file}")
        
        return report_file

if __name__ == "__main__":
    monitor = MarketMonitor()
    
    # 运行一次测试
    print("=== 测试运行 ===")
    monitor.monitor_once()
    
    print("\n=== 可以启动定时监控 ===")
    print("使用方法:")
    print("1. monitor.start_monitoring(30) - 每30分钟监控一次")
    print("2. monitor.generate_daily_report() - 生成每日报告")
    print("3. monitor.stop_monitoring() - 停止监控")