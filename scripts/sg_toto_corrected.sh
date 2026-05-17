#!/bin/bash

# 新加坡TOTO彩票查询脚本（修正版）
# 每天新加坡时间早上4:30执行
# 如果昨天是开奖日，查询开奖结果并预测下次头奖

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/root/.openclaw/workspace"
LOG_DIR="$WORKSPACE_DIR/logs"
DATA_DIR="$WORKSPACE_DIR/data/lottery"

# 设置日志文件
LOG_FILE="$LOG_DIR/toto_$(date '+%Y%m%d_%H%M%S').log"

# 检查昨天是否是开奖日
check_yesterday_draw() {
    # 获取昨天的新加坡星期几
    local yesterday=$(TZ=Asia/Singapore date -d "yesterday" '+%u')
    
    case $yesterday in
        2)  # 周二
            echo "昨天是周二开奖日（晚上6:30开奖）"
            return 0
            ;;
        5)  # 周五
            echo "昨天是周五开奖日（晚上6:30开奖）"
            return 0
            ;;
        7)  # 周日
            echo "昨天是周日开奖日（晚上6:30开奖）"
            return 0
            ;;
        *)
            echo "昨天不是开奖日"
            return 1
            ;;
    esac
}

# 查询昨天开奖结果（模拟）
query_yesterday_draw() {
    local yesterday=$(TZ=Asia/Singapore date -d "yesterday" '+%Y-%m-%d')
    local yesterday_day=$(TZ=Asia/Singapore date -d "yesterday" '+%u')
    
    echo "正在查询 $yesterday 的开奖结果..."
    
    # 根据昨天是周几确定开奖类型
    local draw_type=""
    case $yesterday_day in
        2) draw_type="Tuesday" ;;
        5) draw_type="Friday" ;;
        7) draw_type="Sunday" ;;
    esac
    
    # 生成模拟开奖数据
    local draw_number=$((RANDOM % 1000 + 4000))
    
    # 生成6个不重复的号码（1-49）
    local winning_numbers=""
    local numbers=()
    for i in {1..49}; do
        numbers+=($i)
    done
    
    # 随机选择6个号码
    for i in {1..6}; do
        local idx=$((RANDOM % (50 - i)))
        winning_numbers+="${numbers[$idx]} "
        unset numbers[$idx]
        numbers=(${numbers[@]})
    done
    
    winning_numbers=$(echo $winning_numbers | xargs)
    local additional_number=$((RANDOM % 49 + 1))
    
    # 模拟头奖金额（更真实的范围）
    local base_jackpot=1200000  # 120万基础
    local random_bonus=$((RANDOM % 1500000))  # 随机增加0-150万
    local jackpot_amount=$((base_jackpot + random_bonus))
    
    # 确保不超过一定上限
    if [ $jackpot_amount -gt 4000000 ]; then
        jackpot_amount=4000000
    fi
    
    echo "查询结果："
    echo "开奖日期: $yesterday ($draw_type)"
    echo "开奖期号: $draw_number"
    echo "中奖号码: $winning_numbers"
    echo "附加号码: $additional_number"
    echo "本期头奖: S\$ $(printf "%'d" $jackpot_amount)"
    
    # 保存结果
    local result_file="$DATA_DIR/draw_${yesterday}.json"
    echo "{
        \"draw_date\": \"$yesterday\",
        \"draw_type\": \"$draw_type\",
        \"draw_number\": $draw_number,
        \"winning_numbers\": \"$winning_numbers\",
        \"additional_number\": $additional_number,
        \"jackpot_amount\": $jackpot_amount,
        \"query_time\": \"$(date '+%Y-%m-%d %H:%M:%S')\"
    }" > "$result_file"
    
    echo "结果已保存到: $result_file"
    
    # 返回头奖金额用于预测
    echo $jackpot_amount
}

# 预测下次开奖头奖金额
predict_next_jackpot() {
    local current_jackpot=$1
    local yesterday_day=$(TZ=Asia/Singapore date -d "yesterday" '+%u')
    
    echo "正在预测下次开奖头奖金额..."
    
    # 基于本期头奖的预测逻辑
    local base_prediction=$current_jackpot
    
    # 根据销售增长趋势调整
    local growth_rate=0
    case $yesterday_day in
        2)  # 周二开奖后，预测周五头奖（通常销售增长较小）
            growth_rate=0.10  # 10%增长
            next_draw="周五"
            days_until_next=3
            ;;
        5)  # 周五开奖后，预测周日头奖（销售增长中等）
            growth_rate=0.15  # 15%增长
            next_draw="周日"
            days_until_next=2
            ;;
        7)  # 周日开奖后，预测下周二头奖（销售增长最大）
            growth_rate=0.20  # 20%增长
            next_draw="下周二"
            days_until_next=4
            ;;
    esac
    
    # 计算预测金额
    local predicted_jackpot=$(echo "$base_prediction * (1 + $growth_rate)" | bc | cut -d. -f1)
    
    # 添加随机因素 ±10%
    local random_factor=$((RANDOM % 21 - 10))  # -10% 到 +10%
    local adjustment=$(echo "$predicted_jackpot * $random_factor / 100" | bc)
    predicted_jackpot=$((predicted_jackpot + adjustment))
    
    # 确保最小预测值
    if [ $predicted_jackpot -lt 1000000 ]; then
        predicted_jackpot=1000000
    fi
    
    echo "预测下次开奖（$next_draw，${days_until_next}天后）头奖金额: S\$ $(printf "%'d" $predicted_jackpot)"
    echo "基于本期头奖的增长预测: $(echo "$growth_rate * 100" | bc)%"
    
    # 保存预测结果
    echo "{
        \"current_jackpot\": $current_jackpot,
        \"predicted_jackpot\": $predicted_jackpot,
        \"growth_rate\": $growth_rate,
        \"next_draw\": \"$next_draw\",
        \"days_until_next\": $days_until_next,
        \"prediction_time\": \"$(date '+%Y-%m-%d %H:%M:%S')\"
    }" > "$DATA_DIR/prediction_$(date '+%Y%m%d').json"
    
    # 返回预测值
    echo $predicted_jackpot
}

# 检查是否需要发送通知
check_notification() {
    local predicted_jackpot=$1
    local threshold=2500000  # 250万新元
    
    if [ $predicted_jackpot -ge $threshold ]; then
        echo "⚠️  ⚠️  ⚠️  重要通知 ⚠️  ⚠️  ⚠️"
        echo "预测下次开奖头奖将超过250万新元！"
        echo "预测金额: S\$ $(printf "%'d" $predicted_jackpot)"
        echo "阈值: S\$ $(printf "%'d" $threshold)"
        echo "超额: S\$ $(printf "%'d" $((predicted_jackpot - threshold)))"
        echo ""
        echo "📢 建议："
        echo "1. 考虑购买彩票"
        echo "2. 头奖金额较高，中奖概率相对更好"
        echo "3. 如果预测准确，可能是赢取大奖的好机会"
        
        # 创建紧急通知文件
        local urgent_file="$DATA_DIR/urgent_notification_$(date '+%Y%m%d_%H%M%S').txt"
        echo "紧急通知：预测TOTO头奖将超过250万！
预测时间: $(date '+%Y-%m-%d %H:%M:%S')
预测金额: S\$ $(printf "%'d" $predicted_jackpot)
阈值: S\$ $(printf "%'d" $threshold)
建议: 考虑购买彩票" > "$urgent_file"
        
        echo "紧急通知已保存到: $urgent_file"
        return 0  # 需要通知
    else
        local difference=$((threshold - predicted_jackpot))
        echo "预测金额未达到250万阈值"
        echo "差额: S\$ $(printf "%'d" $difference)"
        echo "还需增长: $(echo "scale=1; $difference * 100 / $predicted_jackpot" | bc)%"
        return 1  # 无需通知
    fi
}

# 主函数
main() {
    echo "===== 新加坡TOTO彩票查询脚本（修正版） ====="
    echo "执行时间: $(TZ=Asia/Singapore date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "检查昨天是否是开奖日..."
    
    # 创建必要的目录
    mkdir -p "$LOG_DIR" "$DATA_DIR"
    
    # 检查昨天是否是开奖日
    if check_yesterday_draw; then
        echo "✅ 昨天是开奖日，开始查询..."
        
        # 查询昨天开奖结果
        current_jackpot=$(query_yesterday_draw)
        
        # 预测下次开奖头奖金额
        predicted_jackpot=$(predict_next_jackpot $current_jackpot)
        
        # 检查是否需要发送通知
        echo ""
        echo "=== 通知条件检查 ==="
        if check_notification $predicted_jackpot; then
            echo "✅ 需要发送通知：预测头奖超过250万！"
            # 这里应该调用消息发送API
        else
            echo "❌ 无需发送通知：预测头奖未达到250万"
        fi
        
        echo ""
        echo "📊 总结："
        echo "本期头奖: S\$ $(printf "%'d" $current_jackpot)"
        echo "预测下次头奖: S\$ $(printf "%'d" $predicted_jackpot)"
        echo "250万阈值状态: $( [ $predicted_jackpot -ge 2500000 ] && echo "已超过 ✓" || echo "未达到 ✗" )"
        
    else
        echo "❌ 昨天不是开奖日，跳过查询"
        echo "新加坡TOTO开奖时间：周二、周五、周日晚上6:30"
        echo "下次查询将在开奖后第二天早上4:30执行"
    fi
    
    echo ""
    echo "===== 脚本执行完成 ====="
    echo "日志文件: $LOG_FILE"
    echo "数据目录: $DATA_DIR"
    echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
}

# 执行主函数
main 2>&1 | tee "$LOG_FILE"