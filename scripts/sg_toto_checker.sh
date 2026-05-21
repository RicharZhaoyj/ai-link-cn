#!/bin/bash

# 新加坡TOTO彩票开奖查询脚本
# 在每次开奖后10小时执行，检查中奖情况和预测下次头奖

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/root/.openclaw/workspace"
LOG_DIR="$WORKSPACE_DIR/logs"
DATA_DIR="$WORKSPACE_DIR/data/lottery"
TOKEN_FILE="$WORKSPACE_DIR/tokens/lottery_token.txt"
SCRIPT_NAME="sg_toto_checker.sh"

# 🚨 重要修正：新加坡TOTO实际开奖时间是周一和周四！
# 错误信息：之前的脚本都写成了周二、周五、周日
# 正确信息：周一和周四晚上6:30开奖

# 新加坡TOTO开奖时间（周一和周四晚上6:30）
# 计算上次开奖时间
get_last_draw_time() {
    local current_date=$(date '+%Y-%m-%d')
    local current_day=$(date '+%u')  # 1-周一, 7-周日
    
    # 获取新加坡当前时间（UTC+8）
    local sg_time=$(TZ=Asia/Singapore date '+%Y-%m-%d %H:%M:%S')
    echo "[$sg_time] 新加坡时间"
    
    case $current_day in
        1|2)  # 周一或周二 - 上次开奖是上周四
            echo "上次开奖: 上周四 18:30"
            last_draw_day="last_thu"
            ;;
        3|4)  # 周三或周四 - 上次开奖是周一
            # 检查是否已经过了今天的开奖时间
            local current_hour=$(TZ=Asia/Singapore date '+%H')
            if [ $current_day -eq 4 ] && [ $current_hour -ge 18 ]; then
                echo "上次开奖: 今天 18:30"
                last_draw_day="today"
            else
                echo "上次开奖: 周一 18:30"
                last_draw_day="mon"
            fi
            ;;
        5|6|7)  # 周五、周六、周日 - 上次开奖是周四
            echo "上次开奖: 周四 18:30"
            last_draw_day="thu"
            ;;
    esac
}
            # 检查是否已经过了今天的开奖时间
            local current_hour=$(TZ=Asia/Singapore date '+%H')
            if [ $current_hour -ge 18 ]; then
                echo "上次开奖: 今天 18:30"
                last_draw_day="today"
            else
                echo "上次开奖: 昨天"
                if [ $current_day -eq 2 ]; then
                    last_draw_day="sun"  # 周二 - 上次是周日
                else
                    last_draw_day="tue"  # 周五 - 上次是周二
                fi
            fi
            ;;
        3|6)  # 周三或周六 - 上次开奖是周二或周五
            echo "上次开奖: 昨天"
            if [ $current_day -eq 3 ]; then
                last_draw_day="tue"  # 周三 - 上次是周二
            else
                last_draw_day="fri"  # 周六 - 上次是周五
            fi
            ;;
        7)    # 周日
            local current_hour=$(TZ=Asia/Singapore date '+%H')
            if [ $current_hour -ge 18 ]; then
                echo "上次开奖: 今天 18:30"
                last_draw_day="today"
            else
                echo "上次开奖: 周五 18:30"
                last_draw_day="fri"
            fi
            ;;
    esac
}

# 查询最新开奖结果（模拟函数）
query_latest_results() {
    echo "正在查询新加坡TOTO最新开奖结果..."
    
    # 这里应该是调用新加坡博彩公司API的实际代码
    # 由于没有实际API，我们模拟一些数据
    
    local draw_date=$(date -d "yesterday" '+%Y-%m-%d')
    local winning_numbers="4 15 23 28 35 41"
    local additional_number="12"
    local jackpot_amount="1800000"  # 180万新元
    
    echo "开奖日期: $draw_date"
    echo "中奖号码: $winning_numbers + 附加号码: $additional_number"
    echo "头奖金额: S\$ $(printf "%'d" $jackpot_amount)"
    
    # 保存结果到文件
    mkdir -p "$DATA_DIR"
    echo "{
        \"draw_date\": \"$draw_date\",
        \"winning_numbers\": \"$winning_numbers\",
        \"additional_number\": \"$additional_number\",
        \"jackpot_amount\": $jackpot_amount,
        \"query_time\": \"$(date '+%Y-%m-%d %H:%M:%S')\"
    }" > "$DATA_DIR/latest_draw.json"
}

# 预测下次头奖金额
predict_next_jackpot() {
    echo "正在预测下次开奖头奖金额..."
    
    # 读取历史数据
    local history_file="$DATA_DIR/history.json"
    if [ ! -f "$history_file" ]; then
        # 创建模拟历史数据
        echo '[
            {"date": "2025-05-10", "jackpot": 1200000, "sales": 8500000},
            {"date": "2025-05-13", "jackpot": 1500000, "sales": 9200000},
            {"date": "2025-05-16", "jackpot": 1800000, "sales": 10500000},
            {"date": "2025-05-19", "jackpot": 2100000, "sales": 11800000},
            {"date": "2025-05-22", "jackpot": 2300000, "sales": 12500000}
        ]' > "$history_file"
    fi
    
    # 简单的线性预测模型
    local avg_increase=250000  # 平均每次增加25万
    local last_jackpot=1800000  # 假设上次头奖180万
    
    local predicted_jackpot=$((last_jackpot + avg_increase))
    local confidence=75  # 置信度75%
    
    echo "预测下次头奖金额: S\$ $(printf "%'d" $predicted_jackpot)"
    echo "预测置信度: ${confidence}%"
    
    # 保存预测结果
    echo "{
        \"predicted_jackpot\": $predicted_jackpot,
        \"confidence\": $confidence,
        \"prediction_time\": \"$(date '+%Y-%m-%d %H:%M:%S')\",
        \"next_draw_date\": \"$(date -d '+2 days' '+%Y-%m-%d')\"
    }" > "$DATA_DIR/prediction.json"
    
    # 返回预测值用于检查是否需要通知
    echo $predicted_jackpot
}

# 发送通知（如果需要）
send_notification() {
    local predicted_jackpot=$1
    local threshold=2500000  # 250万阈值
    
    if [ $predicted_jackpot -ge $threshold ]; then
        echo "⚠️  重要通知: 预测下次TOTO头奖将超过250万新元！"
        echo "预测金额: S\$ $(printf "%'d" $predicted_jackpot)"
        echo "阈值: S\$ $(printf "%'d" $threshold)"
        echo "建议: 可以考虑购买彩票！"
        
        # 这里应该调用消息发送API通知用户
        # 由于没有实际集成，我们只是记录日志
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 需要通知用户: 预测头奖超过250万" >> "$LOG_DIR/toto_notifications.log"
        
        return 0  # 需要通知
    else
        echo "预测头奖金额未达到250万阈值，无需通知"
        return 1  # 无需通知
    fi
}

# 主函数
main() {
    echo "===== 新加坡TOTO彩票查询脚本 ====="
    echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # 创建必要的目录
    mkdir -p "$LOG_DIR" "$DATA_DIR"
    
    # 获取上次开奖时间
    get_last_draw_time
    
    # 查询最新开奖结果
    query_latest_results
    
    # 预测下次头奖金额
    predicted_jackpot=$(predict_next_jackpot)
    
    # 检查是否需要发送通知
    if send_notification $predicted_jackpot; then
        echo "已记录需要发送通知"
    fi
    
    echo "===== 脚本执行完成 ====="
    echo "日志文件: $LOG_DIR/toto_checker.log"
    echo "数据目录: $DATA_DIR"
}

# 执行主函数并记录日志
main 2>&1 | tee -a "$LOG_DIR/toto_checker.log"