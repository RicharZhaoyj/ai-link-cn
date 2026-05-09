#!/usr/bin/env python3
"""
简单的加密货币分析脚本
获取实时数据并提供交易建议
"""

import os
import subprocess
import json

# 技能路径
skill_dir = "/root/.openclaw/workspace/skills/crypto-market-data"

def run_script(script_name, args):
    """运行Node.js脚本"""
    script_path = os.path.join(skill_dir, "scripts", script_name)
    cmd = f"node {script_path} {args}"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except:
                print(f"JSON解析错误: {result.stdout}")
                return None
        else:
            print(f"错误: {result.stderr}")
            return None
    except Exception as e:
        print(f"运行脚本出错: {e}")
        return None

def analyze_crypto():
    """分析主要加密货币"""
    print("=== 加密货币走势分析 ===\n")
    
    # 获取比特币价格
    btc_data = run_script("get_crypto_price.js", "bitcoin")
    if btc_data:
        btc_price = btc_data.get("bitcoin", {}).get("usd", None)
        print(f"比特币(BTC)当前价格: ${btc_price}")
    
    # 获取以太坊价格
    eth_data = run_script("get_crypto_price.js", "ethereum")
    if eth_data:
        eth_price = eth_data.get("ethereum", {}).get("usd", None)
        print(f"以太坊(ETH)当前价格: ${eth_price}")
    
    # 获取Solana价格
    sol_data = run_script("get_crypto_price.js", "solana")
    if sol_data:
        sol_price = sol_data.get("solana", {}).get("usd", None)
        print(f"Solana(SOL)当前价格: ${sol_price}")
    
    # 获取热门加密货币
    trending_data = run_script("get_trending_coins.js", "")
    if trending_data:
        coins = trending_data.get("coins", [])
        print(f"\n热门加密货币(前5名):")
        for i, coin in enumerate(coins[:5]):
            coin_info = coin.get("item", {})
            name = coin_info.get("name", "")
            symbol = coin_info.get("symbol", "")
            price_data = coin_info.get("data", {}).get("price", None)
            print(f"  {i+1}. {name} ({symbol}): ${price_data}")
    
    # 获取顶级加密货币
    top_data = run_script("get_top_coins.js", "--per_page=10")
    if top_data:
        print(f"\n市值排名前10的加密货币:")
        for i, coin in enumerate(top_data[:10]):
            coin_info = coin.get("item", {})
            name = coin_info.get("name", "")
            symbol = coin_info.get("symbol", "")
            price_data = coin_info.get("data", {}).get("price", None)
            market_cap_rank = coin_info.get("market_cap_rank", "")
            print(f"  {i+1}. {name} ({symbol}) - 市值排名: #{market_cap_rank} - 价格: ${price_data}")
    
    print("\n=== 技术分析建议 ===\n")
    
    # 基于价格给出建议
    if btc_price and eth_price:
        if btc_price > 70000:
            print("比特币(技术分析):")
            print("  - 价格高于$70,000，可能存在阻力")
            print("  - 建议观察RSI是否超过70")
            print("  - 关注MACD指标变化")
        else:
            print("比特币(技术分析):")
            print("  - 价格相对适中")
            print("  - 建议关注成交量变化")
            print("  - 观察是否形成支撑位")
        
        if eth_price > 4000:
            print("\n以太坊(技术分析):")
            print("  - 价格高于$4,000，注意阻力位")
            print("  - 观察布林带宽度")
            print("  - 关注MACD交叉信号")
        else:
            print("\n以太坊(技术分析):")
            print("  - 价格相对合理")
            print("  - 建议关注MA30支撑")
            print("  - 观察RSI指标")
    
    print("\n=== AiCoin操作指南 ===\n")
    print("请在AiCoin中执行以下操作:")
    print("1. 打开技术分析图表:")
    print("   - 选择BTC/USDT或ETH/USDT")
    print("   - 添加以下技术指标:")
    print("     • 移动平均线(MA7, MA30)")
    print("     • RSI(14)")
    print("     • MACD")
    print("     • 布林带")
    
    print("2. 观察信号:")
    print("   - RSI > 70: 超买信号，考虑卖出")
    print("   - RSI < 30: 超卖信号，考虑买入")
    print("   - MACD柱状图 > 0: 买入信号")
    print("   - MACD柱状图 < 0: 卖出信号")
    
    print("3. 设置价格警报:")
    print("   - BTC突破$75,000: 考虑卖出")
    print("   - BTC跌破$65,000: 考虑买入")
    print("   - ETH突破$4,200: 考虑卖出")
    print("   - ETH跌破$3,500: 考虑买入")
    
    print("\n=== 交易建议 ===\n")
    print("当前市场观察:")
    print("1. 热门币种: RAVE, TAO, MON, VVV, PENGU")
    print("2. 关注Solana(SOL)生态")
    print("3. Zcash(ZEC)有隐私特性")
    print("4. 观察AI相关加密货币")
    
    print("\n=== 风险管理 ===\n")
    print("建议:")
    print("1. 仓位管理: 不要超过30%单币种仓位")
    print("2. 止损设置: 设置10-15%止损线")
    print("3. 分批买入: 分批入场而非一次性")
    print("4. 定期复盘: 每日复盘交易决策")

def get_global_market():
    """获取全球市场数据"""
    global_data = run_script("get_global_market_data.js", "")
    if global_data:
        print("\n=== 全球市场概况 ===")
        print(f"总市值: ${global_data.get('total_market_cap', '未知')}")
        print(f"活跃加密货币数量: {global_data.get('active_cryptocurrencies', '未知')}")
        print(f"市场份额: BTC: {global_data.get('btc_dominance', '未知')}%, ETH: {global_data.get('eth_dominance', '未知')}%")

if __name__ == "__main__":
    analyze_crypto()
    get_global_market()