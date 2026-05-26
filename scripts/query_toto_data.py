#!/usr/bin/env python3
"""
新加坡TOTO彩票数据查询脚本
用于从官方网站获取实时开奖数据和头奖信息
"""

import requests
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import sys

def fetch_singaporepools():
    """从新加坡博彩公司官网获取数据"""
    print("正在访问新加坡博彩公司官网...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    
    try:
        # 尝试访问TOTO结果页面
        url = "https://www.singaporepools.com.sg/en/product/Pages/toto_results.aspx"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"成功访问网站，状态码: {response.status_code}")
            return response.text
        else:
            print(f"网站访问失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"访问网站时出错: {e}")
        return None

def fetch_lottosg():
    """从其他彩票网站获取数据作为备用"""
    print("正在尝试访问lotto.net...")
    
    try:
        url = "https://www.lotto.net/singapore-toto"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"成功访问lotto.net，状态码: {response.status_code}")
            return response.text
        else:
            print(f"lotto.net访问失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"访问lotto.net时出错: {e}")
        return None

def parse_jackpot_info(html_content):
    """解析网页内容提取头奖信息"""
    print("解析网页内容中...")
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取所有文本
        text = soup.get_text()
        
        # 查找头奖相关信息
        jackpot_patterns = [
            r'Jackpot.*?(\$\d+(?:,\d+)*)',
            r'Group\s*1.*?(\$\d+(?:,\d+)*)',
            r'Estimated.*?(\$\d+(?:,\d+)*)',
            r'S\$(\d+(?:,\d+)*)',
            r'(\d+(?:,\d+)*)\s*million',
        ]
        
        jackpot_info = {}
        
        for pattern in jackpot_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                print(f"找到匹配模式 '{pattern}': {matches}")
                jackpot_info[f"pattern_{pattern[:20]}"] = matches[:5]
        
        # 查找日期信息
        date_patterns = [
            r'Draw Date.*?(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4})',
            r'Next Draw.*?(\d{1,2}/\d{1,2}/\d{4})',
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                print(f"找到日期匹配 '{pattern}': {matches}")
                jackpot_info["draw_dates"] = matches
        
        # 查找中奖号码
        number_patterns = [
            r'Winning Numbers.*?([\d\s,]+)',
            r'Numbers.*?([\d\s,]+)',
            r'(\d{1,2}(?:\s+\d{1,2}){5,})',  # 匹配6个或更多数字
        ]
        
        for pattern in number_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                print(f"找到号码匹配 '{pattern}': {matches}")
                jackpot_info["winning_numbers"] = matches
        
        return jackpot_info
        
    except Exception as e:
        print(f"解析网页内容时出错: {e}")
        return {}

def generate_report(jackpot_data, source):
    """生成数据报告"""
    print("\n" + "="*60)
    print("新加坡TOTO彩票数据查询报告")
    print("="*60)
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"数据来源: {source}")
    print("-"*60)
    
    if not jackpot_data:
        print("⚠️ 未能从网站提取到彩票数据")
        print("可能原因:")
        print("1. 网站反爬虫机制阻止了访问")
        print("2. 网页结构发生变化")
        print("3. 网络连接问题")
        print("\n建议:")
        print("1. 直接访问: https://www.singaporepools.com.sg")
        print("2. 使用新加坡博彩公司官方APP")
        print("3. 查看当地新闻媒体")
        return
    
    print("📊 提取到的信息:")
    
    # 显示头奖金额信息
    jackpot_found = False
    for key, values in jackpot_data.items():
        if "pattern" in key and values:
            print(f"\n💰 头奖相关信息 ({key}):")
            for value in values[:3]:  # 显示前3个
                if "S$" in str(value) or "$" in str(value):
                    print(f"  - 金额: {value}")
                    jackpot_found = True
                else:
                    print(f"  - 可能金额: S${value}")
                    jackpot_found = True
    
    if not jackpot_found:
        print("\n💰 头奖金额: 未找到明确的头奖金额信息")
        print("  新加坡TOTO头奖通常从100万新元起")
        print("  如果连续多期无人中奖，奖池会累积增加")
    
    # 显示日期信息
    if "draw_dates" in jackpot_data and jackpot_data["draw_dates"]:
        print(f"\n📅 开奖日期:")
        for date in jackpot_data["draw_dates"][:3]:
            print(f"  - {date}")
    
    # 显示中奖号码
    if "winning_numbers" in jackpot_data and jackpot_data["winning_numbers"]:
        print(f"\n🔢 中奖号码:")
        for numbers in jackpot_data["winning_numbers"][:2]:
            print(f"  - {numbers}")
    
    print("\n" + "="*60)
    print("📌 新加坡TOTO彩票基本信息:")
    print("="*60)
    print("开奖时间: 周一、周四、周六晚上6:30（新加坡时间）")
    print("官方网站: https://www.singaporepools.com.sg")
    print("头奖起点: 100万新元")
    print("查询建议: 对于最准确信息，请直接访问官方网站")
    print("="*60)

def main():
    """主函数"""
    print("开始执行新加坡TOTO彩票数据查询...")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 尝试从主要网站获取数据
    html_content = fetch_singaporepools()
    source = "新加坡博彩公司官网"
    
    # 如果主要网站失败，尝试备用网站
    if not html_content:
        print("主网站访问失败，尝试备用网站...")
        html_content = fetch_lottosg()
        source = "lotto.net"
    
    if html_content:
        # 解析数据
        jackpot_data = parse_jackpot_info(html_content)
        
        # 生成报告
        generate_report(jackpot_data, source)
        
        # 保存原始数据用于调试
        with open('/tmp/toto_raw_data.txt', 'w', encoding='utf-8') as f:
            f.write(f"Source: {source}\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"Data length: {len(html_content)}\n")
            f.write("\nExtracted info:\n")
            f.write(json.dumps(jackpot_data, indent=2, ensure_ascii=False))
            
        print(f"\n原始数据已保存到: /tmp/toto_raw_data.txt")
        
    else:
        print("所有网站访问都失败了")
        generate_report({}, "无法访问任何网站")
    
    print("\n查询完成!")

if __name__ == "__main__":
    main()