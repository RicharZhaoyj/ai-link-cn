#!/bin/bash

# 自动更新时间显示脚本
# 从Git提交记录获取最新更新时间，并更新index.html中的硬编码时间

set -e

WORKSPACE="/root/.openclaw/workspace"
INDEX_FILE="$WORKSPACE/index.html"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# 检查是否在Git仓库中
if [ ! -d "$WORKSPACE/.git" ]; then
    echo "错误: 不在Git仓库中"
    exit 1
fi

cd "$WORKSPACE"

# 获取最新的提交时间
log "获取最新的Git提交时间..."
LATEST_COMMIT_TIME=$(git log -1 --format="%cd" --date=format:"%Y年%m月%d日 %H:%M:%S")
LATEST_COMMIT_DATE=$(git log -1 --format="%cd" --date=format:"%Y-%m-%dT%H:%M:%S+08:00")

if [ -z "$LATEST_COMMIT_TIME" ]; then
    echo "错误: 无法获取提交时间"
    exit 1
fi

log "最新提交时间: $LATEST_COMMIT_TIME"
log "ISO格式: $LATEST_COMMIT_DATE"

# 检查index.html文件是否存在
if [ ! -f "$INDEX_FILE" ]; then
    echo "错误: index.html文件不存在"
    exit 1
fi

# 备份原文件
BACKUP_FILE="$INDEX_FILE.backup.$(date +%Y%m%d_%H%M%S)"
cp "$INDEX_FILE" "$BACKUP_FILE"
log "已备份原文件: $BACKUP_FILE"

# 更新时间常量
log "更新JavaScript中的时间常量..."
sed -i "s/const REAL_UPDATE_TIME = \"[0-9]\+年[0-9]\+月[0-9]\+日 [0-9]\+:[0-9]\+:[0-9]\+\";/const REAL_UPDATE_TIME = \"$LATEST_COMMIT_TIME\";/" "$INDEX_FILE"

# 更新时间戳
log "更新JavaScript中的时间戳..."
sed -i "s/const REAL_UPDATE_TIMESTAMP = new Date(\"[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\}T[0-9]\\{2\\}:[0-9]\\{2\\}:[0-9]\\{2\\}\+08:00\").getTime();/const REAL_UPDATE_TIMESTAMP = new Date(\"$LATEST_COMMIT_DATE\").getTime();/" "$INDEX_FILE"

# 更新HTML中的硬编码时间
log "更新HTML中的硬编码时间..."
sed -i "s/<span class=\"time-value\" id=\"realUpdateTimeDisplay\">[0-9]\+年[0-9]\+月[0-9]\+日 [0-9]\+:[0-9]\+:[0-9]\+<\/span>/<span class=\"time-value\" id=\"realUpdateTimeDisplay\">$LATEST_COMMIT_TIME<\/span>/" "$INDEX_FILE"

# 验证更新
log "验证更新..."
UPDATED_TIME=$(grep -o "const REAL_UPDATE_TIME = \"[^\"]*\"" "$INDEX_FILE" | cut -d'"' -f2)
UPDATED_DISPLAY=$(grep -o "<span class=\"time-value\" id=\"realUpdateTimeDisplay\">[^<]*</span>" "$INDEX_FILE" | sed 's/<[^>]*>//g')

if [ "$UPDATED_TIME" = "$LATEST_COMMIT_TIME" ] && [ "$UPDATED_DISPLAY" = "$LATEST_COMMIT_TIME" ]; then
    success "时间显示已成功更新到: $LATEST_COMMIT_TIME"
    
    # 显示更新前后的差异
    echo ""
    echo "=== 更新详情 ==="
    echo "JavaScript常量: $UPDATED_TIME"
    echo "HTML显示: $UPDATED_DISPLAY"
    echo ""
    
    # 检查是否需要提交到Git
    if git diff --name-only | grep -q "index.html"; then
        log "检测到index.html有变化，建议提交到Git"
        echo "运行以下命令提交更改:"
        echo "  git add index.html"
        echo "  git commit -m 'fix: 更新网站最后显示时间为$LATEST_COMMIT_TIME'"
        echo "  git push origin main"
    fi
else
    echo "警告: 时间更新可能未完全成功"
    echo "期望: $LATEST_COMMIT_TIME"
    echo "实际常量: $UPDATED_TIME"
    echo "实际显示: $UPDATED_DISPLAY"
fi

log "脚本执行完成"