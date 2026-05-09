#!/usr/bin/env python3
"""
统一市场数据收集器 - 获取港股、美股、新加坡股市、基金、ETF、期货和数字货币数据
"""

import pandas as pd
import yfinance as yf
import ccxt
from datetime import datetime, timedelta
import warnings
import time
import json

warnings.filterwarnings('ignore')

class MarketDataCollector:
    """多市场数据收集器"""
    
    def __init__(self):
        # 数字货币交易所
        self.exchange = ccxt.binance({
            'apiKey': '',
            'secret': '',
            'options': {'defaultType': 'spot'}
        })
        
        # 股票市场配置
        self.stock_markets = {
            'hk': {
                'name': '港股',
                'symbols': [
                    '00700.HK',  # 腾讯控股
                    '00939.HK',  # 建设银行
                    '00005.HK',  # 汇丰控股
                    '00001.HK',  # 长和
                    '02318.HK',  # 平安保险
                    '02800.HK',  # 盈富基金
                    '00883.HK',  # 中海油
                    '01288.HK',  # 农业银行
                    '00941.HK',  # 中国移动
                    '02628.HK',  # 中国人寿
                ]
            },
            'us': {
                'name': '美股',
                'symbols': [
                    'AAPL',  # 苹果
                    'MSFT',  # 微软
                    'GOOGL',  # 谷歌
                    'AMZN',  # 亚马逊
                    'TSLA',  # 特斯拉
                    'NVDA',  # 英伟达
                    'META',  # Meta
                    'NFLX',  # Netflix
                    'BRK-B',  # 伯克希尔
                    'JPM',   # 摩根大通
                ]
            },
            'sg': {
                'name': '新加坡股市',
                'symbols': [
                    'D05.SI',   # DBS Bank
                    'U11.SI',   # UOB Bank
                    'O39.SI',   # OCBC Bank
                    'Z74.SI',   # Singtel
                    'C6L.SI',   # Singapore Airlines
                    'BN4.SI',   # Keppel Corp
                    'F34.SI',   # Wilmar International
                    'S68.SI',   # SGX
                    'U14.SI',   # UOL Group
                    'S51.SI',   # SingPost
                ]
            }
        }
        
        # ETF列表
        self.etf_symbols = [
            'SPY',   # SPDR S&P 500 ETF
            'QQQ',   # Invesco QQQ ETF
            'VTI',   # Vanguard Total Stock Market ETF
            'VT',    # Vanguard Total World Stock ETF
            'EEM',   # iShares MSCI Emerging Markets ETF
            'IWM',   # iShares Russell 2000 ETF
            'ARKK',  # ARK Innovation ETF
            'GLD',   # SPDR Gold Shares ETF
            'SLV',   # iShares Silver Trust ETF
            'BND',   # Vanguard Total Bond Market ETF
        ]
        
        # 期货列表
        self.futures_symbols = [
            'GC=F',  # 黄金期货
            'SI=F',  # 白银期货
            'CL=F',  # 原油期货
            'NG=F',  # 天然气期货
            'ZC=F',  # 玉米期货
            'ZS=F',  # 大豆期货
            'ZW=F',  # 小麦期货
            'LE=F',  # 活牛期货
            'HE=F',  # 生猪期货
            'HG=F',  # 铜期货
        ]
        
        # 基金列表（部分ETF作为基金）
        self.fund_symbols = [
            'VOO',   # Vanguard S&P 500 ETF
            'VGK',   # Vanguard FTSE Europe ETF
            'VPL',   # Vanguard FTSE Pacific ETF
            'VWO',   # Vanguard FTSE Emerging Markets ETF
            'VEA',   # Vanguard FTSE Developed Markets ETF
            'VSS',   # Vanguard FTSE All-World ex-US Small-Cap ETF
            'VNQ',   # Vanguard Real Estate ETF
            'VGT',   # Vanguard Information Technology ETF
            'VFH',   # Vanguard Financials ETF
            'VHT',   # Vanguard Health Care ETF
        ]
        
        # 数字货币配置
        self.crypto_symbols = [
            'BTC/USDT',  # 比特币
            'ETH/USDT',  # 以太坊
            'SOL/USDT',  # Solana
            'BNB/USDT',  # Binance Coin
            'XRP/USDT',  # Ripple
            'ADA/USDT',  # Cardano
            'DOGE/USDT', # Dogecoin
            'DOT/USDT',  # Polkadot
            'MATIC/USDT', # Polygon
            'LINK/USDT', # Chainlink
        ]
    
    def get_stock_data(self, symbol, period='30d'):
        """获取股票数据"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if len(data) > 0:
                return {
                    'symbol': symbol,
                    'data': data,
                    'last_price': data['Close'].iloc[-1],
                    'volume': data['Volume'].iloc[-1],
                    'change_percent': ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
                }
            else:
                return None
        except Exception as e:
            print(f"获取股票{symbol}数据失败: {e}")
            return None
    
    def get_crypto_data(self, symbol, timeframe='1d', limit=30):
        """获取数字货币数据"""
        try:
            # 转换币种符号格式
            if '/' in symbol:
                base, quote = symbol.split('/')
                symbol = f"{base}/{quote}"
            
            # 获取OHLCV数据
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit)
            
            if len(ohlcv) > 0:
                # 转换为DataFrame
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                
                return {
                    'symbol': symbol,
                    'data': df,
                    'last_price': df['close'].iloc[-1],
                    'volume': df['volume'].iloc[-1],
                    'change_percent': ((df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]) * 100
                }
            else:
                return None
        except Exception as e:
            print(f"获取数字货币{symbol}数据失败: {e}")
            return None
    
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
        
        print("开始获取港股数据...")
        for symbol in self.stock_markets['hk']['symbols']:
            data = self.get_stock_data(symbol)
            if data:
                all_data['hk_stocks'].append(data)
        
        print("开始获取美股数据...")
        for symbol in self.stock_markets['us']['symbols']:
            data = self.get_stock_data(symbol)
            if data:
                all_data['us_stocks'].append(data)
        
        print("开始获取新加坡股票数据...")
        for symbol in self.stock_markets['sg']['symbols']:
            data = self.get_stock_data(symbol)
            if data:
                all_data['sg_stocks'].append(data)
        
        print("开始获取ETF数据...")
        for symbol in self.etf_symbols:
            data = self.get_stock_data(symbol)
            if data:
                all_data['etfs'].append(data)
        
        print("开始获取期货数据...")
        for symbol in self.futures_symbols:
            data = self.get_stock_data(symbol)
            if data:
                all_data['futures'].append(data)
        
        print("开始获取基金数据...")
        for symbol in self.fund_symbols:
            data = self.get_stock_data(symbol)
            if data:
                all_data['funds'].append(data)
        
        print("开始获取数字货币数据...")
        for symbol in self.crypto_symbols:
            data = self.get_crypto_data(symbol)
            if data:
                all_data['crypto'].append(data)
        
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
    
    def analyze_trend(self, data):
        """分析趋势"""
        df = data['data']
        
        if isinstance(df, pd.DataFrame):
            if 'Close' in df.columns:
                prices = df['Close']
            elif 'close' in df.columns:
                prices = df['close']
            else:
                return None
            
            # 计算7日和30日移动平均
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
        return None
    
    def analyze_technical(self, data):
        """技术分析"""
        df = data['data']
        
        if isinstance(df, pd.DataFrame):
            if 'Close' in df.columns:
                prices = df['Close']
            elif 'close' in df.columns:
                prices = df['close']
            else:
                return None
            
            # RSI计算
            delta = prices.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # MACD计算
            ema12 = prices.ewm(span=12).mean()
            ema26 = prices.ewm(span=26).mean()
            macd = ema12 - ema26
            macd_signal = macd.ewm(span=9).mean()
            macd_hist = macd - macd_signal
            
            # 布林带计算
            bb_middle = prices.rolling(window=20).mean()
            std = prices.rolling(window=20).std()
            bb_upper = bb_middle + 2 * std
            bb_lower = bb_middle - 2 * std
            
            return {
                'rsi': rsi,
                'macd_hist': macd_hist.iloc[-1],
                'bb_upper': bb_upper.iloc[-1],
                'bb_lower': bb_lower.iloc[-1],
                'bb_middle': bb_middle.iloc[-1],
                'current_price': prices.iloc[-1],
                'price_position': ((prices.iloc[-1] - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])) * 100 if bb_upper.iloc[-1] > bb_lower.iloc[-1] else None
            }
        return None
    
    def save_data(self, all_data, summary):
        """保存数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存原始数据
        data_file = f"market_data_{timestamp}.json"
        with open(data_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': all_data,
                'summary': summary
            }, f, indent=4)
        
        # 生成报告
        report_file = f"market_report_{timestamp}.txt"
        report_content = self.generate_report(all_data, summary)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"数据保存为: {data_file}")
        print(f"报告保存为: {report_file}")
        
        return data_file, report_file
    
    def generate_report(self, all_data, summary):
        """生成详细报告"""
        report = f"""
=== 多市场投资分析报告 ===
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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
            
            report += f"""
{market_name}市场:
- 分析数量: {market_summary['count']}
- 平均价格: {market_summary['avg_price']:.2f}
- 平均涨跌幅: {market_summary['avg_change']:.2f}%
- 平均成交量: {market_summary['avg_volume']:.2f}

涨幅前三:
"""
            for gainer in market_summary['top_gainers']:
                report += f"  {gainer['symbol']}: {gainer['change_percent']:.2f}% (价格: {gainer['last_price']:.2f})\n"
            
            report += f"""
跌幅前三:
"""
            for loser in market_summary['top_losers']:
                report += f"  {loser['symbol']}: {loser['change_percent']:.2f}% (价格: {loser['last_price']:.2f})\n"
        
        report += f"""
二、详细分析:
"""
        
        # 详细分析每个市场的代表性品种
        for market_type, data_list in all_data.items():
            if data_list:
                market_name = {
                    'hk_stocks': '港股',
                    'us_stocks': '美股',
                    'sg_stocks': '新加坡股市',
                    'etfs': 'ETF',
                    'futures': '期货',
                    'funds': '基金',
                    'crypto': '数字货币'
                }.get(market_type, market_type)
                
                report += f"""
{market_name}市场代表品种分析:
"""
                
                for data in data_list[:5]:  # 分析前5个
                    symbol = data['symbol']
                    trend_analysis = self.analyze_trend(data)
                    technical_analysis = self.analyze_technical(data)
                    
                    if trend_analysis and technical_analysis:
                        report += f"""
{symbol}:
- 当前价格: {technical_analysis['current_price']:.2f}
- 涨跌幅: {data['change_percent']:.2f}%
- 趋势: {trend_analysis['trend']}
- RSI: {technical_analysis['rsi']:.1f}
- MACD柱状图: {technical_analysis['macd_hist']:.4f}
"""
                        
                        # RSI信号
                        if technical_analysis['rsi'] < 30:
                            report += f"- RSI信号: 超卖（买入机会）\n"
                        elif technical_analysis['rsi'] > 70:
                            report += f"- RSI信号: 超买（卖出机会）\n"
                        else:
                            report += f"- RSI信号: 中性\n"
                        
                        # MACD信号
                        if technical_analysis['macd_hist'] > 0:
                            report += f"- MACD信号: 买入信号\n"
                        else:
                            report += f"- MACD信号: 卖出信号\n"
                        
                        # 布林带位置
                        if technical_analysis['price_position'] is not None:
                            if technical_analysis['price_position'] > 80:
                                report += f"- 布林带位置: 接近上轨（上涨信号）\n"
                            elif technical_analysis['price_position'] < 20:
                                report += f"- 布林带位置: 接近下轨（下跌信号）\n"
                            else:
                                report += f"- 布林带位置: 中性区域\n"
        
        report += f"""
三、投资建议:
1. 重点关注涨幅前三的品种，但需警惕过度上涨
2. 关注技术指标（RSI/MACD）同时好转的品种
3. 对于下跌品种，需要进一步分析基本面
4. 数字货币波动较大，建议分批建仓
5. 设置止损位：港股/美股 10%，数字货币 15%

四、后续操作:
1. 每小时更新一次数据
2. 设置价格警报：突破阻力位/跌破支撑位
3. 关注市场重大新闻
4. 定期调整投资组合

=== 报告结束 ===
"""
        
        return report
    
    def run(self):
        """运行完整分析"""
        print("=== 开始多市场数据收集和分析 ===")
        
        # 获取所有市场数据
        all_data = self.get_all_market_data()
        
        if not all_data['hk_stocks'] and not all_data['us_stocks'] and not all_data['sg_stocks']:
            print("股票数据获取失败，尝试另一种方法...")
            return
        
        # 生成市场概况
        summary = self.generate_market_summary(all_data)
        
        # 保存数据和报告
        data_file, report_file = self.save_data(all_data, summary)
        
        # 打印简要报告
        print("\n=== 市场概况摘要 ===")
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
        
        print("\n=== 分析完成 ===")
        print(f"详细报告请查看: {report_file}")
        print(f"原始数据请查看: {data_file}")
        
        return all_data, summary

if __name__ == "__main__":
    collector = MarketDataCollector()
    collector.run()