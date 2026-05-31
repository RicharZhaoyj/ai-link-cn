#!/bin/bash
# 状态监控系统定时任务配置
# 创建时间: 2026年5月31日 04:40 AM

set -e

echo "🚀 配置状态监控系统定时任务..."
echo "================================"

# 脚本路径
COLLECTOR_SCRIPT="/root/.openclaw/workspace/scripts/status_collector_simple.sh"
ANALYZER_SCRIPT="/root/.openclaw/workspace/scripts/status_analyzer_simple.sh"
WORKSPACE_DIR="/root/.openclaw/workspace"
CRON_FILE="/etc/cron.d/ai-link-status-monitor"

# 检查脚本是否存在
if [ ! -f "$COLLECTOR_SCRIPT" ]; then
    echo "❌ 错误: 状态收集脚本不存在: $COLLECTOR_SCRIPT"
    exit 1
fi

if [ ! -f "$ANALYZER_SCRIPT" ]; then
    echo "❌ 错误: 状态分析脚本不存在: $ANALYZER_SCRIPT"
    exit 1
fi

echo "✅ 找到监控脚本:"
echo "   - 收集脚本: $COLLECTOR_SCRIPT"
echo "   - 分析脚本: $ANALYZER_SCRIPT"

# 创建cron配置文件
echo "📝 创建cron配置文件: $CRON_FILE"

cat > "$CRON_FILE" << EOF
# AI.link.cn 状态监控系统定时任务
# 配置时间: 2026年5月31日 04:40 AM
# 注意: 所有时间基于系统时区 (Asia/Shanghai)

# 每5分钟收集一次状态数据
*/5 * * * * root cd $WORKSPACE_DIR && $COLLECTOR_SCRIPT >> /var/log/status-collector.log 2>&1

# 每10分钟分析一次状态数据
*/10 * * * * root cd $WORKSPACE_DIR && $ANALYZER_SCRIPT >> /var/log/status-analyzer.log 2>&1

# 每天凌晨2:00清理旧的状态文件 (保留7天)
0 2 * * * root find $WORKSPACE_DIR/status -name "*.json" -mtime +7 -delete
0 2 * * * root find $WORKSPACE_DIR/analysis -name "*.json" -mtime +7 -delete

# 每天凌晨3:00生成每日状态报告
0 3 * * * root cd $WORKSPACE_DIR && echo "=== 每日状态报告 $(date) ===" >> /var/log/status-daily.log && $ANALYZER_SCRIPT >> /var/log/status-daily.log 2>&1
EOF

# 设置文件权限
chmod 644 "$CRON_FILE"

echo "✅ cron配置文件创建完成: $CRON_FILE"
echo ""
echo "📋 定时任务配置详情:"
echo "===================="
cat "$CRON_FILE"
echo ""
echo "⏰ 监控频率:"
echo "  • 状态收集: 每5分钟一次"
echo "  • 状态分析: 每10分钟一次"
echo "  • 文件清理: 每天凌晨2:00 (保留7天)"
echo "  • 每日报告: 每天凌晨3:00"
echo ""
echo "📊 日志文件位置:"
echo "  • 收集日志: /var/log/status-collector.log"
echo "  • 分析日志: /var/log/status-analyzer.log"
echo "  • 日报日志: /var/log/status-daily.log"
echo ""
echo "🔧 测试运行监控系统..."
echo ""

# 测试运行收集脚本
echo "测试状态收集..."
if cd "$WORKSPACE_DIR" && "$COLLECTOR_SCRIPT"; then
    echo "✅ 状态收集测试成功"
else
    echo "❌ 状态收集测试失败"
    exit 1
fi

echo ""

# 测试运行分析脚本
echo "测试状态分析..."
if cd "$WORKSPACE_DIR" && "$ANALYZER_SCRIPT"; then
    echo "✅ 状态分析测试成功"
else
    echo "❌ 状态分析测试失败"
    exit 1
fi

echo ""
echo "🎯 状态监控系统配置完成!"
echo ""
echo "📁 重要文件位置:"
echo "  • 状态数据: $WORKSPACE_DIR/status/"
echo "  • 分析结果: $WORKSPACE_DIR/analysis/"
echo "  • 监控脚本: $WORKSPACE_DIR/scripts/"
echo ""
echo "🔍 手动检查状态:"
echo "  cd $WORKSPACE_DIR && ./scripts/status_collector_simple.sh"
echo "  cd $WORKSPACE_DIR && ./scripts/status_analyzer_simple.sh"
echo ""
echo "📈 查看最新状态:"
echo "  cat $WORKSPACE_DIR/status/latest_status.json | jq ."
echo "  cat $WORKSPACE_DIR/analysis/latest_analysis.json | jq ."
echo ""
echo "⚠️  注意: cron服务需要重启才能生效"
echo "  重启命令: systemctl restart cron"
echo ""
echo "✅ 状态监控系统定时任务配置完成!"
echo "   系统现在可以每5分钟自动收集状态，确保状态不明不超过30分钟"