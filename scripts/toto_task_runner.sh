#!/bin/bash

# 新加坡TOTO彩票查询任务执行器
# 这个脚本将被定时任务调用

set -e

WORKSPACE_DIR="/root/.openclaw/workspace"
SCRIPT_PATH="$WORKSPACE_DIR/scripts/sg_toto_corrected.sh"
LOG_DIR="$WORKSPACE_DIR/logs"

echo "===== 新加坡TOTO彩票查询任务开始 ====="
echo "执行时间: $(TZ=Asia/Singapore date '+%Y-%m-%d %H:%M:%S %Z')"

# 检查脚本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ 错误：TOTO查询脚本不存在: $SCRIPT_PATH"
    exit 1
fi

# 执行查询脚本
echo "执行查询脚本..."
bash "$SCRIPT_PATH"

# 检查是否需要发送通知
echo "检查通知文件..."
NOTIFICATION_FILE=$(ls -t "$WORKSPACE_DIR/data/lottery/urgent_notification_"*.txt 2>/dev/null | head -1)

if [ -f "$NOTIFICATION_FILE" ]; then
    echo "📢 发现紧急通知文件: $NOTIFICATION_FILE"
    echo "内容:"
    cat "$NOTIFICATION_FILE"
    
    # 这里应该添加实际的元宝消息发送逻辑
    # 现在只是记录日志
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 需要发送通知：预测头奖超过250万" >> "$LOG_DIR/toto_notifications_sent.log"
else
    echo "✅ 没有需要发送的紧急通知"
fi

echo "===== 任务执行完成 ====="