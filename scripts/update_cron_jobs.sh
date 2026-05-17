#!/bin/bash

# 更新AI.link.cn的定时任务配置
# 添加缺失的自动更新环节

set -e

echo "=== 更新AI.link.cn定时任务 ==="

# 获取当前crontab
CRON_TEMP=$(mktemp)
crontab -l > "$CRON_TEMP" 2>/dev/null || echo "# AI.link.cn定时任务" > "$CRON_TEMP"

# 移除旧的自动更新任务（如果存在）
sed -i '/auto_update_site.sh/d' "$CRON_TEMP"

# 添加新的自动更新任务（在发现任务后30分钟执行）
echo "# 自动更新网站（在发现任务后30分钟执行）" >> "$CRON_TEMP"
echo "30 2 * * * /root/.openclaw/workspace/scripts/auto_update_site.sh >> /root/.openclaw/workspace/logs/cron_auto_update.log 2>&1" >> "$CRON_TEMP"

# 添加每日健康检查（可选）
echo "# 每日健康检查" >> "$CRON_TEMP"
echo "0 8 * * * /root/.openclaw/workspace/scripts/health_check.sh >> /root/.openclaw/workspace/logs/cron_health.log 2>&1" >> "$CRON_TEMP"

# 应用新的crontab
crontab "$CRON_TEMP"

# 清理临时文件
rm -f "$CRON_TEMP"

echo "新的定时任务配置:"
crontab -l

echo ""
echo "=== 更新完成 ==="
echo "1. 每日发现任务: 凌晨2点"
echo "2. 自动网站更新: 凌晨2:30（发现后30分钟）"
echo "3. 健康检查任务: 早上8点"
echo ""
echo "日志文件:"
echo "  - /root/.openclaw/workspace/logs/cron_auto_update.log"
echo "  - /root/.openclaw/workspace/logs/cron_health.log"