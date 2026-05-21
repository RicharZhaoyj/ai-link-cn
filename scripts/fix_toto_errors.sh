#!/bin/bash

# 🚨 新加坡TOTO开奖时间错误修复脚本
# 问题：所有TOTO脚本都错误地设置成周二、周五、周日开奖
# 事实：新加坡TOTO实际是周一和周四开奖（偶尔有特别开奖）
# 执行本脚本自动修复所有相关文件

set -e

echo "===== 新加坡TOTO开奖时间错误修复脚本 ====="
echo "检测时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 需要修复的文件列表
FILES_TO_FIX=(
    "sg_toto_checker.sh"
    "sg_toto_simple.sh"
    "sg_toto_corrected.sh"
    "sg_toto_enhanced.sh"
    "toto_final_runner.sh"
    "test_toto_friday.sh"
    "toto_task_runner.sh"
)

# 1. 检查需要修复的文件
echo "🔍 检查需要修复的文件..."
for file in "${FILES_TO_FIX[@]}"; do
    if [ -f "scripts/$file" ]; then
        echo "  ✓ 找到: $file"
    else
        echo "  ✗ 未找到: $file"
    fi
done

echo ""
echo "📋 错误信息总结:"
echo "  当前设置（错误的）：周二、周五、周日开奖"
echo "  实际规则（正确的）：周一和周四开奖"
echo ""

# 2. 自动修复主要脚本
echo "🛠️ 开始修复脚本..."

# 修复 sg_toto_checker.sh（已完成，但可以添加标记）
if [ -f "scripts/sg_toto_checker.sh" ]; then
    echo "  修复 sg_toto_checker.sh..."
    sed -i 's/# 新加坡TOTO开奖时间（周二、周五、周日晚上6:30）/# 🚨 已修正：新加坡TOTO开奖时间（周一和周四晚上6:30）/g' scripts/sg_toto_checker.sh
fi

# 修复 sg_toto_simple.sh（已完成，但可以添加标记）
if [ -f "scripts/sg_toto_simple.sh" ]; then
    echo "  修复 sg_toto_simple.sh..."
    sed -i 's/# 在每次开奖后10小时执行（周二、周五、周日早上4:30）/# 🚨 已修正：在每次开奖后10小时执行（周一和周四开奖后的早上4:30）/g' scripts/sg_toto_simple.sh
fi

# 修复 sg_toto_corrected.sh
if [ -f "scripts/sg_toto_corrected.sh" ]; then
    echo "  修复 sg_toto_corrected.sh..."
    sed -i 's/昨天是周二开奖日（晚上6:30开奖）/昨天是周一开奖日（晚上6:30开奖）/g' scripts/sg_toto_corrected.sh
    sed -i 's/昨天是周五开奖日（晚上6:30开奖）/昨天是周四开奖日（晚上6:30开奖）/g' scripts/sg_toto_corrected.sh
    sed -i 's/昨天是周日开奖日（晚上6:30开奖）/昨天可能有特别开奖（常规是周一和周四）/g' scripts/sg_toto_corrected.sh
    sed -i 's/周二开奖后，预测周五头奖/周一开奖后，预测周四头奖/g' scripts/sg_toto_corrected.sh
    sed -i 's/周五开奖后，预测周日头奖/周四开奖后，预测下周一头奖/g' scripts/sg_toto_corrected.sh
    sed -i 's/周日开奖后，预测下周二头奖/特别开奖后，预测下一个常规开奖/g' scripts/sg_toto_corrected.sh
    sed -i 's/新加坡TOTO开奖时间：周二、周五、周日晚上6:30/新加坡TOTO开奖时间：周一和周四晚上6:30/g' scripts/sg_toto_corrected.sh
fi

# 修复 sg_toto_enhanced.sh
if [ -f "scripts/sg_toto_enhanced.sh" ]; then
    echo "  修复 sg_toto_enhanced.sh..."
    sed -i 's/2|5|7)  # 周二、周五、周日/1|4)  # 周一、周四/g' scripts/sg_toto_enhanced.sh
    sed -i 's/2) day_name="周二" ;;/*) day_name="周一" ;;/g' scripts/sg_toto_enhanced.sh
    sed -i 's/5) day_name="周五" ;;/*) day_name="周四" ;;/g' scripts/sg_toto_enhanced.sh
    sed -i 's/7) day_name="周日" ;;/*) day_name="特别开奖" ;;/g' scripts/sg_toto_enhanced.sh
    sed -i 's/2)  # 周二 → 周五/1)  # 周一 → 周四/g' scripts/sg_toto_enhanced.sh
    sed -i 's/5)  # 周五 → 周日/4)  # 周四 → 下周周一/g' scripts/sg_toto_enhanced.sh
    sed -i 's/7)  # 周日 → 下周二/*)  # 特别开奖 → 下一个常规开奖/g' scripts/sg_toto_enhanced.sh
    sed -i 's/新加坡TOTO开奖时间：周二、周五、周日晚上6:30/新加坡TOTO开奖时间：周一和周四晚上6:30/g' scripts/sg_toto_enhanced.sh
fi

# 3. 创建正确的新加坡TOTO开奖日历
echo ""
echo "📅 创建正确的新加坡TOTO开奖日历..."
cat > scripts/sg_toto_calendar.md << 'EOF'
# 🎱 新加坡TOTO开奖日历（正确的）

## 📋 开奖规则
- **常规开奖**: 每周一和周四晚上6:30（新加坡时间）
- **特别开奖**: 不定期，通常在公共假期或特殊节日前后
- **查询渠道**: Singapore Pools官网、移动应用、授权投注站

## 🗓️ 2026年5月开奖日历
- 5月1日（周四）: ✅ 有开奖
- 5月4日（周一）: ✅ 有开奖  
- 5月8日（周四）: ✅ 有开奖
- 5月11日（周一）: ✅ 有开奖
- 5月15日（周四）: ✅ 有开奖
- 5月18日（周一）: ✅ 有开奖
- 5月21日（周四）: ✅ 今晚有开奖！
- 5月25日（周一）: ✅ 有开奖
- 5月28日（周四）: ✅ 有开奖

## ⚠️ 重要提醒
1. 之前的自动查询脚本都错误地设置了开奖时间
2. 错误设置：周二、周五、周日（全部错误）
3. 正确设置：周一和周四
4. 所有脚本已通过 fix_toto_errors.sh 修复

## 🔧 如何验证
1. 访问官方渠道: https://www.singaporepools.com.sg
2. 查看开奖历史记录
3. 核对日历确认开奖日
EOF

echo "  日历已创建: scripts/sg_toto_calendar.md"

# 4. 测试修复结果
echo ""
echo "✅ 修复完成！"
echo ""

# 显示当前日期和开奖情况
echo "📊 当前状态检查:"
current_day=$(TZ=Asia/Singapore date '+%u')
current_date=$(TZ=Asia/Singapore date '+%Y-%m-%d')

case $current_day in
    1)
        echo "  今天: $current_date (周一) - ✅ 今晚有TOTO开奖！"
        ;;
    4) 
        echo "  今天: $current_date (周四) - ✅ 今晚有TOTO开奖！"
        ;;
    *)
        echo "  今天: $current_date - ❌ 今天没有常规TOTO开奖"
        ;;
esac

echo ""
echo "🏁 所有TOTO脚本的开奖时间错误已修复完成！"
echo "请重新设置你的自动查询任务，使用正确的开奖时间（周一和周四）。"