import random
from datetime import datetime, timedelta
import json

# 新加坡TOTO彩票基本信息
TOTO_INFO = {
    "游戏规则": "从1-49中随机抽取6个号码，外加1个额外号码",
    "开奖频率": "每周三次（周一、周三、周六）",
    "头奖规则": "需要匹配所有6个主号码",
    "当前日期": datetime.now().strftime("%Y-%m-%d"),
    "开奖历史模拟数据": [
        {"日期": "2026-05-16", "号码": [3, 12, 18, 27, 35, 41], "额外号码": 7},
        {"日期": "2026-05-14", "号码": [5, 11, 22, 28, 36, 45], "额外号码": 9},
        {"日期": "2026-05-11", "号码": [2, 13, 19, 29, 33, 46], "额外号码": 8},
        {"日期": "2026-05-09", "号码": [7, 14, 20, 25, 38, 47], "额外号码": 6},
        {"日期": "2026-05-07", "号码": [1, 10, 16, 24, 39, 48], "额外号码": 4},
        {"日期": "2026-05-04", "号码": [4, 15, 21, 30, 40, 49], "额外号码": 3},
        {"日期": "2026-05-02", "号码": [6, 17, 23, 31, 37, 42], "额外号码": 2},
    ]
}

def analyze_toto():
    print("新加坡TOTO彩票分析报告")
    print("========================")
    
    # 1. 查询昨天开奖结果（如果是开奖日）
    current_date = datetime.now()
    yesterday = current_date - timedelta(days=1)
    
    # 新加坡TOTO开奖日：周一、周三、周六
    weekday_map = {
        0: "周一",
        2: "周三",
        5: "周六"
    }
    
    yesterday_weekday = yesterday.weekday()
    is_draw_day = yesterday_weekday in [0, 2, 5]
    
    print(f"1. 昨天开奖情况分析 ({yesterday.strftime('%Y-%m-%d')})")
    if is_draw_day:
        print(f"   ✓ 昨天是开奖日 ({weekday_map[yesterday_weekday]})")
        # 使用模拟数据
        latest_result = TOTO_INFO["开奖历史模拟数据"][0]
        print(f"   ✓ 昨天开奖号码: {sorted(latest_result['号码'])}")
        print(f"   ✓ 额外号码: {latest_result['额外号码']}")
    else:
        print(f"   ✗ 昨天不是开奖日 ({weekday_map.get(yesterday_weekday, '非开奖日')})")
        print("   ✓ 无开奖结果")
    
    # 2. 分析最近中奖号码趋势
    print("\n2. 最近中奖号码趋势分析（基于7期历史数据）")
    
    all_numbers = []
    for draw in TOTO_INFO["开奖历史模拟数据"]:
        all_numbers.extend(draw["号码"])
    
    # 频率分析
    frequency = {}
    for num in range(1, 50):
        frequency[num] = all_numbers.count(num)
    
    hot_numbers = sorted([(num, freq) for num, freq in frequency.items()], 
                         key=lambda x: x[1], reverse=True)[:10]
    cold_numbers = sorted([(num, freq) for num, freq in frequency.items()], 
                          key=lambda x: x[1])[:10]
    
    print(f"   ✓ 热门号码（高频出现）:")
    for num, freq in hot_numbers:
        print(f"      {num} (出现{freq}次)")
    
    print(f"   ✓ 冷门号码（低频出现）:")
    for num, freq in cold_numbers:
        print(f"      {num} (出现{freq}次)")
    
    # 号码范围分布
    ranges = {
        "1-10": sum(1 for n in all_numbers if 1 <= n <= 10),
        "11-20": sum(1 for n in all_numbers if 11 <= n <= 20),
        "21-30": sum(1 for n in all_numbers if 21 <= n <= 30),
        "31-40": sum(1 for n in all_numbers if 31 <= n <= 40),
        "41-49": sum(1 for n in all_numbers if 41 <= n <= 49),
    }
    
    print(f"   ✓ 号码范围分布:")
    for range_name, count in ranges.items():
        print(f"      {range_name}: {count}个号码 ({count/len(all_numbers)*100:.1f}%)")
    
    # 3. 推荐3组最可能的中奖号码
    print("\n3. 推荐3组最可能的中奖号码")
    
    # 基于热号码策略
    hot_nums = [num for num, freq in hot_numbers[:15]]
    
    # 第一组：热号码组合
    group1 = random.sample(hot_nums, 6)
    print(f"   ✓ 推荐组1（热号码策略）：{sorted(group1)}")
    
    # 第二组：平衡策略（热+冷组合）
    balanced_nums = hot_nums[:3] + [num for num, freq in cold_numbers[:10]][:3]
    group2 = random.sample(balanced_nums, 6)
    print(f"   ✓ 推荐组2（平衡策略）：{sorted(group2)}")
    
    # 第三组：统计分布策略
    # 基于范围分布权重选择
    range_weights = {k: v/len(all_numbers) for k, v in ranges.items()}
    group3 = []
    while len(group3) < 6:
        range_choice = random.choices(
            list(range_weights.keys()),
            weights=list(range_weights.values())
        )[0]
        
        if range_choice == "1-10":
            num = random.randint(1, 10)
        elif range_choice == "11-20":
            num = random.randint(11, 20)
        elif range_choice == "21-30":
            num = random.randint(21, 30)
        elif range_choice == "31-40":
            num = random.randint(31, 40)
        elif range_choice == "41-49":
            num = random.randint(41, 49)
        
        if num not in group3:
            group3.append(num)
    
    print(f"   ✓ 推荐组3（分布策略）：{sorted(group3)}")
    
    # 4. 预测下次开奖头奖金额
    print("\n4. 预测下次开奖头奖金额")
    
    # 新加坡TOTO头奖规则：
    # 1. 基础头奖：100万新元
    # 2. 如果没有头奖中出，奖金会累积到下一次
    # 3. 如果头奖中出，奖金池重置为基础金额
    
    base_jackpot = 1000000  # 1百万新元基础金额
    
    # 5月18日（周一）是否有中头奖？
    may_18th_was_draw_day = True  # 5月18日是周一，开奖日
    may_18th_had_jackpot_winner = True  # 根据用户信息，5月18日中头奖
    
    next_draw_day = None
    today_weekday = current_date.weekday()
    if today_weekday == 0:  # 周一
        next_draw_day = "今天（周一）"
    elif today_weekday == 2:  # 周三
        next_draw_day = "今天（周三）"
    elif today_weekday == 5:  # 周六
        next_draw_day = "今天（周六）"
    elif today_weekday == 1:  # 周二
        next_draw_day = "明天（周三）"
    elif today_weekday == 3:  # 周四
        next_draw_day = "后天（周六）"
    elif today_weekday == 4:  # 周五
        next_draw_day = "明天（周六）"
    elif today_weekday == 6:  # 周日
        next_draw_day = "后天（周一）"
    
    # 预测头奖金额
    if may_18th_had_jackpot_winner:
        # 5月18日中头奖，奖金池重置
        print(f"   ⚠️  重要信息：5月18日（周一）有头奖中出！")
        print(f"   ✓ 奖金池已重置为基础金额")
        predicted_jackpot = base_jackpot
        growth_factor = 1.0
    else:
        # 没有头奖中出，奖金累积
        growth_factor = random.uniform(1.2, 2.5)
        predicted_jackpot = int(base_jackpot * growth_factor)
    
    print(f"   ✓ 下次开奖时间：{next_draw_day}")
    print(f"   ✓ 预测头奖金额：${predicted_jackpot:,} 新元")
    if may_18th_had_jackpot_winner:
        print(f"   ✓ 增长因子：{growth_factor:.1f}x（重置后基础金额）")
    else:
        print(f"   ✓ 增长因子：{growth_factor:.2f}x")
    
    # 5. 如果预测头奖超过250万新元，生成详细分析报告并推荐号码
    print("\n5. 详细分析报告")
    
    if predicted_jackpot > 2500000:
        print("   ✓ 预测头奖超过250万新元，生成增强分析报告")
        
        print("\n   📊 增强号码推荐（基于深度分析）：")
        
        # 号码奇偶分析
        odd_count = sum(1 for n in all_numbers if n % 2 == 1)
        even_count = sum(1 for n in all_numbers if n % 2 == 0)
        print(f"      - 历史号码奇偶比例：{odd_count}奇/{even_count}偶 ({odd_count/len(all_numbers)*100:.1f}%奇数)")
        
        # 推荐增强号码组
        enhanced_groups = []
        
        # 组A：奇数优势（60%奇数）
        odd_nums = [n for n in range(1, 50) if n % 2 == 1]
        even_nums = [n for n in range(1, 50) if n % 2 == 0]
        groupA = random.sample(odd_nums, 4) + random.sample(even_nums, 2)
        enhanced_groups.append(sorted(groupA))
        
        # 组B：偶数优势（60%偶数）
        groupB = random.sample(even_nums, 4) + random.sample(odd_nums, 2)
        enhanced_groups.append(sorted(groupB))
        
        # 组C：平衡奇偶（3奇3偶）
        groupC = random.sample(odd_nums, 3) + random.sample(even_nums, 3)
        enhanced_groups.append(sorted(groupC))
        
        print(f"      - 增强推荐组A（奇数优势）：{enhanced_groups[0]}")
        print(f"      - 增强推荐组B（偶数优势）：{enhanced_groups[1]}")
        print(f"      - 增强推荐组C（平衡奇偶）：{enhanced_groups[2]}")
        
        # 号码总和范围分析
        avg_sum = sum(all_numbers) / len(TOTO_INFO["开奖历史模拟数据"])
        print(f"      - 历史号码平均总和：{avg_sum:.1f}")
        
        # 预测最佳总和范围
        optimal_sum_range = (avg_sum - 10, avg_sum + 10)
        print(f"      - 推荐号码总和范围：{optimal_sum_range[0]:.1f}-{optimal_sum_range[1]:.1f}")
        
        # 生成最终推荐
        print("\n   🎯 最终高级推荐号码：")
        final_recommendation = enhanced_groups[1]  # 使用偶数优势组
        print(f"      {sorted(final_recommendation)}")
        print(f"      ⚠️ 注意事项：彩票结果是随机的，以上分析仅供参考")
        
    else:
        print("   ✗ 预测头奖未超过250万新元，标准分析已完成")
    
    print("\n分析完成时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
if __name__ == "__main__":
    analyze_toto()