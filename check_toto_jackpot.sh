#!/bin/bash

# 新加坡TOTO彩票头奖查询脚本
# 查询新加坡TOTO彩票下期头奖金额

# 设置日期和时间
DATE=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/root/.openclaw/workspace/toto_jackpot.log"

# 尝试查询新加坡TOTO网站
echo "=== TOTO Jackpot Check at $DATE ===" >> "$LOG_FILE"

# 方法1: 尝试从singaporepools网站获取
echo "尝试从新加坡博彩公司官网查询..." >> "$LOG_FILE"
WEB_CONTENT=$(curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "https://www.singaporepools.com.sg/en/product/Pages/toto_results.aspx" 2>/dev/null)

if [ -n "$WEB_CONTENT" ]; then
    # 尝试提取Jackpot相关信息
    JACKPOT_INFO=$(echo "$WEB_CONTENT" | grep -i "jackpot\|group 1\|estimated\|next draw" -A 2 -B 2 | head -50)
    
    if [ -n "$JACKPOT_INFO" ]; then
        echo "找到Jackpot信息:" >> "$LOG_FILE"
        echo "$JACKPOT_INFO" >> "$LOG_FILE"
    else
        echo "未找到明显的Jackpot信息，尝试查找金额模式..." >> "$LOG_FILE"
        # 尝试查找金额模式
        AMOUNTS=$(echo "$WEB_CONTENT" | grep -oE 'S\$[0-9,]+|[0-9,]+ million|S\$[0-9]+,[0-9]+' | head -10)
        if [ -n "$AMOUNTS" ]; then
            echo "找到金额信息:" >> "$LOG_FILE"
            echo "$AMOUNTS" >> "$LOG_FILE"
        else
            echo "未找到金额信息" >> "$LOG_FILE"
        fi
    fi
else
    echo "无法访问网站" >> "$LOG_FILE"
fi

# 方法2: 尝试其他彩票信息网站
echo -e "\n尝试从其他彩票信息网站查询..." >> "$LOG_FILE"
LOTTO_INFO=$(curl -s -L "https://www.lotto.net/singapore-toto/jackpot" 2>/dev/null | grep -i "jackpot\|prize\|amount" -A 2 -B 2 | head -30)

if [ -n "$LOTTO_INFO" ]; then
    echo "从lotto.net找到信息:" >> "$LOG_FILE"
    echo "$LOTTO_INFO" >> "$LOG_FILE"
else
    echo "其他网站也无信息" >> "$LOG_FILE"
fi

# 生成简单的报告
echo -e "\n=== 查询结果总结 ===" >> "$LOG_FILE"
echo "查询时间: $DATE" >> "$LOG_FILE"
echo "数据源1: 新加坡博彩公司官网" >> "$LOG_FILE"
echo "数据源2: lotto.net" >> "$LOG_FILE"
echo -e "\n建议: 如需要精确信息，请直接访问 https://www.singaporepools.com.sg" >> "$LOG_FILE"
echo "=== 查询结束 ===" >> "$LOG_FILE"

# 也输出到控制台
tail -20 "$LOG_FILE"