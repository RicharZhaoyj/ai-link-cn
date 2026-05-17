#!/bin/bash
# 系统健康检查脚本

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/health_check_$(date +%Y%m%d_%H%M%S).log"
ALERT_FILE="$WORKSPACE/logs/alerts.log"

echo "=== 系统健康检查开始 $(date) ===" > "$LOG_FILE"

# 检查目录权限
echo "检查目录权限..." >> "$LOG_FILE"
for dir in "$WORKSPACE" "$WORKSPACE/logs" "$WORKSPACE/backups" "$WORKSPACE/discovered_tools"; do
    if [ -d "$dir" ]; then
        if [ ! -w "$dir" ]; then
            echo "警告: 目录不可写: $dir" >> "$LOG_FILE"
            echo "$(date) - 目录不可写: $dir" >> "$ALERT_FILE"
        fi
    else
        echo "警告: 目录不存在: $dir" >> "$LOG_FILE"
        echo "$(date) - 目录不存在: $dir" >> "$ALERT_FILE"
    fi
done

# 检查关键文件
echo "检查关键文件..." >> "$LOG_FILE"
for file in "$WORKSPACE/index.html" "$WORKSPACE/pages/tools/index.html"; do
    if [ ! -f "$file" ]; then
        echo "错误: 关键文件不存在: $file" >> "$LOG_FILE"
        echo "$(date) - 关键文件不存在: $file" >> "$ALERT_FILE"
    fi
done

# 检查磁盘空间
echo "检查磁盘空间..." >> "$LOG_FILE"
DISK_USAGE=$(df -h "$WORKSPACE" | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "警告: 磁盘使用率过高: ${DISK_USAGE}%" >> "$LOG_FILE"
    echo "$(date) - 磁盘使用率过高: ${DISK_USAGE}%" >> "$ALERT_FILE"
fi

# 检查内存使用
echo "检查内存使用..." >> "$LOG_FILE"
MEM_FREE=$(free -m | awk 'NR==2{printf "%.0f", $4*100/$2}')
if [ "$MEM_FREE" -lt 20 ]; then
    echo "警告: 可用内存不足: ${MEM_FREE}%" >> "$LOG_FILE"
    echo "$(date) - 可用内存不足: ${MEM_FREE}%" >> "$ALERT_FILE"
fi

# 检查Cron任务
echo "检查Cron任务..." >> "$LOG_FILE"
if crontab -l | grep -q "daily_discovery.sh"; then
    echo "Cron任务正常" >> "$LOG_FILE"
else
    echo "错误: Cron任务未设置" >> "$LOG_FILE"
    echo "$(date) - Cron任务未设置" >> "$ALERT_FILE"
fi

# 生成健康报告
HEALTH_STATUS="正常"
if [ -f "$ALERT_FILE" ] && [ -s "$ALERT_FILE" ]; then
    ALERT_COUNT=$(grep -c "$(date +%Y-%m-%d)" "$ALERT_FILE" 2>/dev/null || echo 0)
    if [ "$ALERT_COUNT" -gt 0 ]; then
        HEALTH_STATUS="警告($ALERT_COUNT个问题)"
    fi
fi

echo "系统健康状态: $HEALTH_STATUS" >> "$LOG_FILE"
echo "=== 系统健康检查完成 $(date) ===" >> "$LOG_FILE"

# 如果有严重问题，可以在这里添加通知机制
# 例如发送邮件或Slack通知

exit 0
