#!/bin/bash
# 新加坡TOTO彩票自动查询脚本
# 专为定时任务设计

set -e

echo "🎱 ========================================="
echo "🎱 新加坡TOTO彩票自动查询报告"
echo "🎱 ========================================="
echo "⏰ 查询时间: $(TZ=Asia/Singapore date '+%Y-%m-%d %H:%M:%S') (新加坡时间)"
echo "📅 当前日期: $(TZ=Asia/Singapore date '+%A')"

# 检查今天是否是开奖日
DAY_OF_WEEK=$(TZ=Asia/Singapore date '+%u')
TODAY=$(TZ=Asia/Singapore date '+%Y-%m-%d')

case $DAY_OF_WEEK in
    1|4)  # 周一(1)或周四(4)
        echo "✅ 今天是开奖日！开奖时间: 18:30"
        ;;
    *)
        echo "⏸️ 今天不是开奖日 (开奖日: 周一和周四)"
        ;;
esac

echo ""
echo "🔍 尝试获取最新开奖结果..."

# 使用现有脚本查询
SCRIPT_DIR="/root/.openclaw/workspace/scripts"
if [ -f "$SCRIPT_DIR/query_toto_simple.sh" ]; then
    # 执行查询脚本
    echo "📊 执行查询脚本..."
    bash "$SCRIPT_DIR/query_toto_simple.sh" | head -30
    
    echo ""
    echo "📈 开奖数据分析:"
    echo "• 上次开奖时间: 需要从查询结果中提取"
    echo "• 下次开奖时间: $(TZ=Asia/Singapore date -d '+3 days' '+%Y-%m-%d %H:%M') (如果今天是周一)"
    echo "• 或: $(TZ=Asia/Singapore date -d '+4 days' '+%Y-%m-%d %H:%M') (如果今天是周四)"
    
    # 保存查询结果到日志
    LOG_DIR="/root/.openclaw/workspace/logs/toto"
    mkdir -p "$LOG_DIR"
    LOG_FILE="$LOG_DIR/toto_$(date '+%Y%m%d_%H%M%S').log"
    
    bash "$SCRIPT_DIR/query_toto_simple.sh" > "$LOG_FILE" 2>&1
    
    echo ""
    echo "📁 详细日志已保存到: $LOG_FILE"
    
else
    echo "❌ 查询脚本不存在: $SCRIPT_DIR/query_toto_simple.sh"
    echo ""
    echo "⚠️ 备用查询方法:"
    echo "1. 访问官网: https://www.singaporepools.com.sg"
    echo "2. 查看历史开奖记录"
    echo "3. 检查下一次开奖时间"
fi

echo ""
echo "🎯 重要提醒:"
echo "1. 开奖时间: 每周一和周四 18:30 (新加坡时间)"
echo "2. 查询最佳时间: 开奖后1-2小时 (19:30-20:30)"
echo "3. 合法购彩: 仅限新加坡境内合法渠道"
echo "4. 理性投注: 请勿过度投注，保持健康心态"

echo ""
echo "⏰ 下一次定时查询:"
echo "• 周一: 19:30 (新加坡时间)"
echo "• 周四: 19:30 (新加坡时间)"

echo ""
echo "🎱 ========================================="
echo "🎱 查询完成"
echo "🎱 ========================================="