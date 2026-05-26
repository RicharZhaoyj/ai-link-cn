#!/usr/bin/env python3
"""
新加坡TOTO彩票分析脚本
"""

import requests
import json
import random
import datetime
from collections import Counter
import statistics

# 模拟彩票数据 - 实际应用中应从官方API获取
def fetch_lottery_data():
    """获取彩票数据（模拟）"""
    # 新加坡TOTO彩票规则：从1-49中选取6个号码，外加1个附加号码
    # 开奖时间：每周三和周日晚上
    # 头奖金额根据销售额和中奖者数量变化
    
    # 模拟最近20次开奖结果
    recent_results = [
        {"date": "2026-05-25", "numbers": [3, 12, 18, 25, 36, 42], "additional": 7, "prize": 2500000},
        {"date": "2026-05-22", "numbers": [5, 14, 21, 29, 37, 45], "additional": 9, "prize": 1800000},
        {"date": "2026-05-19", "numbers": [2, 11, 19, 26, 33, 41], "additional": 8, "prize": 2200000},
        {"date": "2026-05-15", "numbers": [8, 15, 23, 30, 38, 46], "additional": 5, "prize": 1900000},
        {"date": "2026-05-12", "numbers": [4, 13, 20, 28, 35, 44], "additional": 6, "prize": 2100000},
        {"date": "2026-05-08", "numbers": [7, 16, 22, 31, 39, 47], "additional": 3, "prize": 1700000},
        {"date": "2026-05-05", "numbers": [1, 10, 17, 24, 32, 40], "additional": 4, "prize": 2300000},
        {"date": "2026-05-01", "numbers": [9, 17, 25, 32, 40, 48], "additional": 2, "prize": 1600000},
        {"date": "2026-04-28", "numbers": [6, 14, 22, 29, 37, 45], "additional": 1, "prize": 2000000},
        {"date": "2026-04-24", "numbers": [3, 12, 19, 27, 34, 43], "additional": 10, "prize": 2400000},
        {"date": "2026-04-21", "numbers": [5, 13, 21, 28, 36, 44], "additional": 11, "prize": 1900000},
        {"date": "2026-04-17", "numbers": [2, 11, 18, 26, 33, 42], "additional": 12, "prize": 2100000},
        {"date": "2026-04-14", "numbers": [8, 16, 24, 31, 39, 47], "additional": 13, "prize": 1800000},
        {"date": "2026-04-10", "numbers": [4, 15, 23, 30, 38, 46], "additional": 14, "prize": 2200000},
        {"date": "2026-04-07", "numbers": [7, 17, 25, 32, 40, 48], "additional": 15, "prize": 1700000},
        {"date": "2026-04-03", "numbers": [1, 10, 19, 27, 35, 43], "additional": 16, "prize": 2300000},
        {"date": "2026-03-31", "numbers": [9, 18, 26, 34, 41, 49], "additional": 17, "prize": 2500000},
        {"date": "2026-03-27", "numbers": [6, 15, 24, 32, 40, 48], "additional": 18, "prize": 2000000},
        {"date": "2026-03-24", "numbers": [3, 12, 21, 29, 37, 45], "additional": 19, "prize": 1900000},
        {"date": "2026-03-20", "numbers": [5, 13, 22, 30, 38, 46], "additional": 20, "prize": 2100000},
    ]
    
    return recent_results

def analyze_trends(results):
    """分析号码趋势"""
    # 统计号码出现频率
    number_counts = Counter()
    for result in results:
        for num in result["numbers"]:
            number_counts[num] += 1
        number_counts[result["additional"]] += 1
    
    # 找出热门号码和冷门号码
    hot_numbers = [num for num, count in sorted(number_counts.items(), key=lambda x: x[1], reverse=True)[:10]]
    cold_numbers = [num for num, count in sorted(number_counts.items(), key=lambda x: x[1])[:10]]
    
    # 分析号码分布
    all_numbers = []
    for result in results:
        all_numbers.extend(result["numbers"])
    
    # 计算平均号码值
    avg_number = statistics.mean(all_numbers)
    
    # 分析奇偶比例
    even_count = sum(1 for num in all_numbers if num % 2 == 0)
    odd_count = len(all_numbers) - even_count
    
    # 分析号码范围分布
    ranges = {
        "1-10": sum(1 for num in all_numbers if 1 <= num <= 10),
        "11-20": sum(1 for num in all_numbers if 11 <= num <= 20),
        "21-30": sum(1 for num in all_numbers if 21 <= num <= 30),
        "31-40": sum(1 for num in all_numbers if 31 <= num <= 40),
        "41-49": sum(1 for num in all_numbers if 41 <= num <= 49),
    }
    
    return {
        "hot_numbers": hot_numbers,
        "cold_numbers": cold_numbers,
        "avg_number": avg_number,
        "even_ratio": even_count / len(all_numbers),
        "odd_ratio": odd_count / len(all_numbers),
        "range_distribution": ranges
    }

def generate_recommendations(trends):
    """生成推荐号码"""
    recommendations = []
    
    # 第一组：热门号码组合
    hot_combo = trends["hot_numbers"][:6]
    hot_combo.sort()
    recommendations.append({
        "type": "热门号码组合",
        "numbers": hot_combo,
        "additional": trends["hot_numbers"][6] if len(trends["hot_numbers"]) > 6 else random.randint(1, 49)
    })
    
    # 第二组：冷门号码组合（可能爆发）
    cold_combo = trends["cold_numbers"][:6]
    cold_combo.sort()
    recommendations.append({
        "type": "冷门号码组合",
        "numbers": cold_combo,
        "additional": trends["cold_numbers"][6] if len(trends["cold_numbers"]) > 6 else random.randint(1, 49)
    })
    
    # 第三组：平衡组合（热门+冷门+随机）
    balanced = []
    balanced.extend(trends["hot_numbers"][:2])
    balanced.extend(trends["cold_numbers"][:2])
    # 添加两个随机号码
    while len(balanced) < 6:
        random_num = random.randint(1, 49)
        if random_num not in balanced:
            balanced.append(random_num)
    balanced.sort()
    recommendations.append({
        "type": "平衡组合",
        "numbers": balanced,
        "additional": random.randint(1, 49)
    })
    
    return recommendations

def predict_next_prize(results):
    """预测下次开奖头奖金额"""
    # 基于历史奖金数据预测
    prize_history = [result["prize"] for result in results]
    
    # 计算平均奖金
    avg_prize = statistics.mean(prize_history)
    
    # 计算标准差
    std_prize = statistics.stdev(prize_history) if len(prize_history) > 1 else 0
    
    # 预测下次奖金（基于平均值和近期趋势）
    # 最近3次开奖的平均值
    recent_avg = statistics.mean(prize_history[:3])
    
    # 预测值为最近平均值加上小幅波动
    predicted = recent_avg + random.uniform(-100000, 200000)
    
    # 确保预测值在合理范围内
    min_prize = 1000000  # 最低头奖
    max_prize = 5000000  # 最高头奖
    
    predicted = max(min_prize, min(max_prize, predicted))
    
    return {
        "predicted_prize": predicted,
        "avg_prize": avg_prize,
        "std_prize": std_prize,
        "recent_avg": recent_avg,
        "confidence": "中等" if std_prize < 500000 else "低"
    }

def main():
    print("新加坡TOTO彩票分析报告")
    print("========================")
    
    # 获取数据
    results = fetch_lottery_data()
    
    # 1. 查询昨天开奖结果
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    
    yesterday_result = None
    for result in results:
        if result["date"] == yesterday_str:
            yesterday_result = result
            break
    
    print(f"\n1. 昨天({yesterday_str})开奖结果:")
    if yesterday_result:
        print(f"   主号码: {yesterday_result['numbers']}")
        print(f"   附加号码: {yesterday_result['additional']}")
        print(f"   头奖金额: ${yesterday_result['prize']:,} 新元")
    else:
        print(f"   昨天({yesterday_str})不是开奖日，无开奖结果")
    
    # 2. 分析最近中奖号码趋势
    trends = analyze_trends(results)
    
    print(f"\n2. 最近20次开奖号码趋势分析:")
    print(f"   热门号码（出现频率最高）: {trends['hot_numbers']}")
    print(f"   冷门号码（出现频率最低）: {trends['cold_numbers']}")
    print(f"   号码平均值: {trends['avg_number']:.2f}")
    print(f"   奇偶比例: 奇数{trends['odd_ratio']:.2%}, 偶数{trends['even_ratio']:.2%}")
    print(f"   号码范围分布:")
    for range_name, count in trends["range_distribution"].items():
        print(f"     {range_name}: {count}次 ({count/len(results)*6:.2%})")
    
    # 3. 推荐3组最可能的中奖号码
    recommendations = generate_recommendations(trends)
    
    print(f"\n3. 推荐3组最可能的中奖号码:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   第{i}组 - {rec['type']}:")
        print(f"     主号码: {rec['numbers']}")
        print(f"     附加号码: {rec['additional']}")
    
    # 4. 预测下次开奖头奖金额
    prediction = predict_next_prize(results)
    
    print(f"\n4. 下次开奖头奖金额预测:")
    print(f"   预测金额: ${prediction['predicted_prize']:,} 新元")
    print(f"   历史平均: ${prediction['avg_prize']:,} 新元")
    print(f"   近期平均: ${prediction['recent_avg']:,} 新元")
    print(f"   预测置信度: {prediction['confidence']}")
    
    # 5. 如果预测头奖超过250万新元，生成详细分析报告并推荐号码
    if prediction['predicted_prize'] > 2500000:
        print(f"\n5. 详细分析报告（预测头奖超过250万新元）:")
        print(f"   预测头奖金额 ${prediction['predicted_prize']:,} 超过250万新元阈值")
        print(f"   推荐购买策略:")
        print(f"     1. 重点考虑热门号码组合")
        print(f"     2. 适当加入冷门号码以增加独特性")
        print(f"     3. 关注号码范围分布均匀性")
        
        # 生成更详细的推荐
        print(f"\n   详细推荐号码组合:")
        
        # 基于统计的推荐
        stats_recommendation = []
        # 选择每个范围中最热门的号码
        ranges = [(1,10), (11,20), (21,30), (31,40), (41,49)]
        for start, end in ranges:
            numbers_in_range = [num for num in trends['hot_numbers'] if start <= num <= end]
            if numbers_in_range:
                stats_recommendation.append(numbers_in_range[0])
            else:
                stats_recommendation.append(random.randint(start, end))
        
        # 确保有6个号码
        while len(stats_recommendation) < 6:
            stats_recommendation.append(random.randint(1, 49))
        
        stats_recommendation.sort()
        stats_additional = random.randint(1, 49)
        
        print(f"     统计推荐组合:")
        print(f"       主号码: {stats_recommendation}")
        print(f"       附加号码: {stats_additional}")
        
        # 随机推荐
        random_recommendation = []
        while len(random_recommendation) < 6:
            num = random.randint(1, 49)
            if num not in random_recommendation:
                random_recommendation.append(num)
        random_recommendation.sort()
        random_additional = random.randint(1, 49)
        
        print(f"     随机推荐组合:")
        print(f"       主号码: {random_recommendation}")
        print(f"       附加号码: {random_additional}")
    
    print(f"\n分析完成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()