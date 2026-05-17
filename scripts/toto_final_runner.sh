#!/bin/bash

# 新加坡TOTO彩票最终任务执行器
# 这个脚本将被定时任务调用，执行增强版分析

set -e

WORKSPACE_DIR="/root/.openclaw/workspace"
SCRIPT_PATH="$WORKSPACE_DIR/scripts/sg_toto_enhanced.sh"
LOG_DIR="$WORKSPACE_DIR/logs"
DATA_DIR="$WORKSPACE_DIR/data/lottery"
REPORT_DIR="$DATA_DIR/reports"

echo "===== 新加坡TOTO彩票分析任务开始 ====="
echo "执行时间: $(TZ=Asia/Singapore date '+%Y-%m-%d %H:%M:%S %Z')"

# 创建必要目录
mkdir -p "$LOG_DIR" "$DATA_DIR" "$REPORT_DIR"

# 检查脚本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ 错误：TOTO增强版分析脚本不存在: $SCRIPT_PATH"
    exit 1
fi

# 执行增强版分析脚本
echo "执行增强版分析脚本..."
bash "$SCRIPT_PATH"

# 检查是否有紧急通知需要发送
echo ""
echo "检查是否需要发送通知..."
NOTIFICATION_FILE=$(ls -t "$DATA_DIR/full_report_"*.txt 2>/dev/null | head -1)
ANALYSIS_FILE="$DATA_DIR/analysis_$(date '+%Y%m%d').json"

if [ -f "$NOTIFICATION_FILE" ]; then
    echo "🚨 发现紧急通知报告: $NOTIFICATION_FILE"
    echo ""
    echo "报告摘要："
    head -20 "$NOTIFICATION_FILE"
    echo "..."
    
    # 检查预测是否超过250万
    if [ -f "$ANALYSIS_FILE" ]; then
        THRESHOLD_CHECK=$(jq -r '.threshold_check' "$ANALYSIS_FILE" 2>/dev/null || echo "false")
        PREDICTED_JACKPOT=$(jq -r '.predicted_jackpot' "$ANALYSIS_FILE" 2>/dev/null || echo "0")
        
        if [ "$THRESHOLD_CHECK" = "true" ] && [ $PREDICTED_JACKPOT -ge 2500000 ]; then
            echo ""
            echo "✅ 确认：预测头奖超过250万，需要发送通知！"
            echo "预测金额: S\$ $(printf "%'d" $PREDICTED_JACKPOT)"
            
            # 这里应该调用元宝消息发送API
            # 临时方案：记录日志
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 需要发送通知：预测头奖 S\$ $(printf "%'d" $PREDICTED_JACKPOT) 超过250万" >> "$LOG_DIR/toto_notifications_sent.log"
            
            # 移动报告到历史目录
            mv "$NOTIFICATION_FILE" "$REPORT_DIR/" 2>/dev/null || true
        else
            echo "❌ 分析文件显示预测未达到250万阈值"
        fi
    fi
    
else
    echo "✅ 没有需要发送的紧急通知"
    
    # 如果有分析文件，显示摘要
    if [ -f "$ANALYSIS_FILE" ]; then
        echo ""
        echo "📊 本次分析摘要："
        CURRENT=$(jq -r '.current_jackpot' "$ANALYSIS_FILE")
        PREDICTED=$(jq -r '.predicted_jackpot' "$ANALYSIS_FILE")
        THRESHOLD_CHECK=$(jq -r '.threshold_check' "$ANALYSIS_FILE")
        
        echo "本期头奖: S\$ $(printf "%'d" $CURRENT)"
        echo "预测下次头奖: S\$ $(printf "%'d" $PREDICTED)"
        echo "250万阈值状态: $( [ "$THRESHOLD_CHECK" = "true" ] && echo "已超过 ✓" || echo "未达到 ✗" )"
    fi
fi

echo ""
echo "===== 任务执行完成 ====="
echo "日志目录: $LOG_DIR"
echo "数据目录: $DATA_DIR"
echo "报告目录: $REPORT_DIR"