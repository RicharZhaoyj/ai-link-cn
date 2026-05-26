#!/bin/bash

# 新加坡TOTO彩票简单查询脚本
# 使用curl和grep从网站获取数据

echo "================================================================"
echo "新加坡TOTO彩票数据查询报告"
echo "================================================================"
echo "查询时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 尝试从新加坡博彩公司官网获取数据
echo -e "\n🔍 正在访问新加坡博彩公司官网..."
URL="https://www.singaporepools.com.sg/en/product/Pages/toto_results.aspx"

# 尝试获取网页内容
WEB_CONTENT=$(curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "$URL" 2>/dev/null)

if [ $? -eq 0 ] && [ -n "$WEB_CONTENT" ]; then
    echo "✅ 成功访问网站"
    
    # 保存网页内容用于分析
    echo "$WEB_CONTENT" > /tmp/toto_webpage.html
    echo "网页已保存到: /tmp/toto_webpage.html"
    
    # 尝试提取关键信息
    echo -e "\n📊 分析网页内容..."
    
    # 查找Jackpot相关信息
    echo "💰 查找头奖信息..."
    JACKPOT_INFO=$(echo "$WEB_CONTENT" | grep -i "jackpot\|group 1\|estimated\|next draw" -A 2 -B 2 | head -10)
    if [ -n "$JACKPOT_INFO" ]; then
        echo "找到Jackpot相关信息:"
        echo "$JACKPOT_INFO"
    else
        echo "未找到明显的Jackpot信息"
    fi
    
    # 查找金额模式
    echo -e "\n💵 查找金额信息..."
    AMOUNTS=$(echo "$WEB_CONTENT" | grep -oE 'S\$[0-9,]+|\$[0-9,]+|[0-9,]+ million' | head -10)
    if [ -n "$AMOUNTS" ]; then
        echo "找到金额信息:"
        echo "$AMOUNTS" | while read amount; do
            echo "  - $amount"
        done
    else
        echo "未找到明确的金额信息"
    fi
    
    # 查找日期信息
    echo -e "\n📅 查找日期信息..."
    DATES=$(echo "$WEB_CONTENT" | grep -oE '[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}|[0-9]{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+[0-9]{4}' | head -5)
    if [ -n "$DATES" ]; then
        echo "找到日期信息:"
        echo "$DATES" | while read date; do
            echo "  - $date"
        done
    else
        echo "未找到日期信息"
    fi
    
    # 查找数字模式
    echo -e "\n🔢 查找中奖号码..."
    NUMBERS=$(echo "$WEB_CONTENT" | grep -oE '[0-9]{1,2}(?:\s+[0-9]{1,2}){5,}' | head -5)
    if [ -n "$NUMBERS" ]; then
        echo "找到可能的号码组合:"
        echo "$NUMBERS" | while read nums; do
            echo "  - $nums"
        done
    else
        echo "未找到明确的号码组合"
    fi
    
else
    echo "❌ 无法访问新加坡博彩公司官网"
    echo "可能原因:"
    echo "  1. 网站反爬虫机制"
    echo "  2. 网络连接问题"
    echo "  3. 网站暂时不可用"
fi

# 尝试其他来源
echo -e "\n🔍 尝试其他彩票信息网站..."
LOTTO_URL="https://www.lotto.net/singapore-toto"
LOTTO_CONTENT=$(curl -s -L "$LOTTO_URL" 2>/dev/null)

if [ $? -eq 0 ] && [ -n "$LOTTO_CONTENT" ]; then
    echo "✅ 成功访问lotto.net"
    
    echo -e "\n💰 从lotto.net查找头奖信息..."
    LOTTO_JACKPOT=$(echo "$LOTTO_CONTENT" | grep -i "jackpot\|prize" -A 2 -B 2 | head -10)
    if [ -n "$LOTTO_JACKPOT" ]; then
        echo "找到信息:"
        echo "$LOTTO_JACKPOT"
    else
        echo "未找到信息"
    fi
else
    echo "❌ 无法访问lotto.net"
fi

# 显示新加坡TOTO基本信息
echo -e "\n================================================================"
echo "📌 新加坡TOTO彩票基本信息"
echo "================================================================"
echo "开奖时间: 周一、周四、周六 晚上6:30（新加坡时间）"
echo "官方网站: https://www.singaporepools.com.sg"
echo "头奖起点: 100万新元（约500万人民币）"
echo "奖池累积: 如果无人中奖，奖池会累积到下一期"
echo "购买方式: 新加坡博彩公司投注站或官方APP"
echo -e "\n💡 查询建议:"
echo "  1. 最准确信息请直接访问官方网站"
echo "  2. 可使用新加坡博彩公司官方APP"
echo "  3. 关注新加坡当地新闻媒体"
echo "================================================================"
echo "查询完成于: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================================"

# 生成总结报告
echo -e "\n📋 总结报告:"
if [ -n "$AMOUNTS" ] || [ -n "$JACKPOT_INFO" ]; then
    echo "✅ 已从网站获取到相关信息"
    echo "建议: 定期任务将在每天04:30（新加坡时间）自动查询"
else
    echo "⚠️ 未能从网站获取到头奖金额信息"
    echo "建议: 如需精确信息，请直接访问官方网站"
fi