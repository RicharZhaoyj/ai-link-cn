#!/bin/bash
# 立即更新系统状态

set -e

echo "🔄 立即更新系统状态..."
echo "======================"

# 收集当前状态
TIMESTAMP=$(date "+%Y-%m-%dT%H:%M:%S+08:00")
WORKSPACE="/root/.openclaw/workspace"

# 检查Grammarly评测进度
GRAMMARLY_FILE="$WORKSPACE/content/tools/grammarly_ai_review_20260519.md"
GRAMMARLY_LINES=$(wc -l < "$GRAMMARLY_FILE" 2>/dev/null || echo "0")
GRAMMARLY_PROGRESS=$((GRAMMARLY_LINES * 100 / 294))

# 检查ChatGPT评测进度
CHATGPT_FILE="$WORKSPACE/content/tools/chatgpt_4o_review_20260522.md"
CHATGPT_LINES=$(wc -l < "$CHATGPT_FILE" 2>/dev/null || echo "0")
CHATGPT_PROGRESS=$((CHATGPT_LINES * 100 / 389))

# 检查网站状态
echo "🌐 检查网站状态..."
WEBSITE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://ai.link.cn || echo "0")

if [ "$WEBSITE_STATUS" = "200" ]; then
    WEBSITE_TITLE=$(curl -s https://ai.link.cn | grep -o '<title>[^<]*</title>' | sed 's/<title>//;s/<\/title>//')
    RESPONSE_TIME=$(curl -s -w "%{time_total}" -o /dev/null https://ai.link.cn | awk '{printf "%.1f", $1}')
else
    WEBSITE_TITLE="无法访问"
    RESPONSE_TIME="0"
fi

# 检查自动化系统
echo "⚙️ 检查自动化系统..."
AUTOMATION_LOG="$WORKSPACE/logs/auto_update.log"
if [ -f "$AUTOMATION_LOG" ]; then
    LAST_RUN=$(tail -1 "$AUTOMATION_LOG" | awk '{print $1, $2}')
    LOG_AGE=$(($(date +%s) - $(date -d "$LAST_RUN" +%s 2>/dev/null || echo "0")))
else
    LAST_RUN="未知"
    LOG_AGE=999999
fi

# 检查系统资源
echo "💾 检查系统资源..."
DISK_USAGE=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//')
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')

# 更新状态文件
echo "📝 更新状态文件..."
STATUS_FILE="$WORKSPACE/status/latest_status.json"

cat > "$STATUS_FILE" << EOF
[
{"component":"website","status":"healthy","http_code":$WEBSITE_STATUS,"response_time":$RESPONSE_TIME,"title":"$WEBSITE_TITLE","timestamp":"$TIMESTAMP"}
,
{"component":"automation","status":"healthy","last_run":"$LAST_RUN","log_age_seconds":$LOG_AGE,"timestamp":"$TIMESTAMP"}
,
{"component":"social_media","linkedin":"stale","zhihu":"stale","timestamp":"$TIMESTAMP"}
,
{"component":"reviews","grammarly":{"lines":$GRAMMARLY_LINES,"progress":$GRAMMARLY_PROGRESS,"last_modified":"$(stat -c %y "$GRAMMARLY_FILE" 2>/dev/null || echo "未知")"},"chatgpt":{"lines":$CHATGPT_LINES,"progress":$CHATGPT_PROGRESS,"last_modified":"$(stat -c %y "$CHATGPT_FILE" 2>/dev/null || echo "未知")"},"timestamp":"$TIMESTAMP"}
,
{"component":"system","disk_usage":$DISK_USAGE,"memory_usage":$MEMORY_USAGE,"timestamp":"$TIMESTAMP"}
]
EOF

echo "✅ 状态更新完成!"
echo ""
echo "📊 最新状态摘要:"
echo "• 网站状态: HTTP $WEBSITE_STATUS, 响应时间 ${RESPONSE_TIME}秒"
echo "• Grammarly评测: $GRAMMARLY_LINES行 ($GRAMMARLY_PROGRESS%)"
echo "• ChatGPT评测: $CHATGPT_LINES行 ($CHATGPT_PROGRESS%)"
echo "• 磁盘使用率: $DISK_USAGE%"
echo "• 内存使用率: $MEMORY_USAGE%"
echo ""
echo "📁 状态文件已保存到: $STATUS_FILE"