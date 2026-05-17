#!/bin/bash
# 系统备份脚本

set -e

WORKSPACE="/root/.openclaw/workspace"
BACKUP_DIR="$WORKSPACE/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

echo "=== 系统备份开始 $(date) ==="

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份关键文件
echo "备份关键文件..."
tar -czf "$BACKUP_FILE" \
    --exclude="node_modules" \
    --exclude=".git" \
    --exclude="backups" \
    "$WORKSPACE/pages" \
    "$WORKSPACE/scripts" \
    "$WORKSPACE"/*.md \
    "$WORKSPACE"/*.html

# 检查备份文件
if [ -f "$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "备份完成: $BACKUP_FILE ($BACKUP_SIZE)"
    
    # 删除旧备份（保留最近7天）
    find "$BACKUP_DIR" -name "backup_*.tar.gz" -type f -mtime +7 -delete
    
    # 备份数据库文件（如果有）
    if [ -f "$WORKSPACE/ai_tools_database.json" ]; then
        cp "$WORKSPACE/ai_tools_database.json" "$BACKUP_DIR/ai_tools_database_$TIMESTAMP.json"
        echo "数据库备份完成"
    fi
else
    echo "备份失败"
    exit 1
fi

echo "=== 系统备份完成 $(date) ==="
