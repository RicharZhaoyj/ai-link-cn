#!/bin/bash
# 每日AI工具发现脚本

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/discovery_$(date +%Y%m%d).log"
NODE_PATH="/root/.nvm/versions/node/v22.22.1/bin/node"

echo "=== 每日AI工具发现开始 $(date) ===" > "$LOG_FILE"

cd "$WORKSPACE"

# 运行工具发现器
echo "运行AI工具发现器..." >> "$LOG_FILE"
if [ -f "scripts/ai_tools_discoverer.js" ]; then
    # 使用实际发现器
    $NODE_PATH scripts/ai_tools_discoverer.js >> "$LOG_FILE" 2>&1
else
    # 如果没有实际发现器，使用测试版本
    echo "使用测试版本发现器..." >> "$LOG_FILE"
    $NODE_PATH scripts/test_discoverer.js >> "$LOG_FILE" 2>&1
fi

# 生成发现报告
echo "生成发现报告..." >> "$LOG_FILE"

# 检查今天是否有新的工具报告
NEW_TOOLS_COUNT=$(find "$WORKSPACE/discovered_tools" -name "new_tools_*.md" -type f -mtime 0 2>/dev/null | wc -l || echo 0)

if [ -d "$WORKSPACE/discovered_tools" ]; then
    echo "今日发现新工具报告数量: $NEW_TOOLS_COUNT" >> "$LOG_FILE"
    
    # 如果有新工具报告，展示文件名
    if [ "$NEW_TOOLS_COUNT" -gt 0 ]; then
        echo "📁 今日报告文件:" >> "$LOG_FILE"
        find "$WORKSPACE/discovered_tools" -name "new_tools_*.md" -type f -mtime 0 2>/dev/null | head -5 >> "$LOG_FILE"
    fi
else
    echo "未找到discovered_tools目录" >> "$LOG_FILE"
fi

echo "=== 每日AI工具发现完成 $(date) ===" >> "$LOG_FILE"
