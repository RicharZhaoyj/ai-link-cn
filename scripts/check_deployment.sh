#!/bin/bash

# 网站部署状态检查脚本

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/deployment_check_$(date +%Y%m%d_%H%M%S).log"

echo "=== AI.link.cn 部署状态检查 ==="
echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 检查Git状态
echo "1. Git状态检查"
cd "$WORKSPACE"
git status --porcelain | head -10
echo "当前分支: $(git branch --show-current)"
echo "最后提交: $(git log --oneline -1)"
echo ""

# 2. 检查GitHub同步
echo "2. GitHub同步状态"
git fetch origin
LOCAL_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/main)

if [ "$LOCAL_COMMIT" = "$REMOTE_COMMIT" ]; then
    echo "✅ 本地和远程GitHub同步"
else
    echo "❌ 本地和远程不同步"
    echo "   本地: $LOCAL_COMMIT"
    echo "   远程: $REMOTE_COMMIT"
fi
echo ""

# 3. 检查网站文件
echo "3. 网站文件检查"
echo "主页文件:"
ls -la index*.html 2>/dev/null || echo "没有找到主页文件"
echo ""
echo "工具页面:"
ls -la pages/tools/*.html 2>/dev/null | wc -l | xargs echo "共有工具页面数量: "
ls -la pages/tools/*.html 2>/dev/null | head -5
echo ""

# 4. 检查定时任务
echo "4. 定时任务检查"
echo "当前crontab配置:"
crontab -l | grep -E "daily_discovery|auto_update|weekly_content" | head -10
echo ""

# 5. 检查网站是否可以访问（简化）
echo "5. 网站访问测试"
echo "尝试访问: https://project-f5cf8.vercel.app/"
echo "注意: 如果网站未部署或网络问题，此测试可能失败"
echo ""

# 6. 检查Vercel配置
echo "6. Vercel配置检查"
echo "vercel.json配置存在: $( [ -f "vercel.json" ] && echo "✅" || echo "❌" )"
echo "package.json存在: $( [ -f "package.json" ] && echo "✅" || echo "❌" )"
echo ""

# 7. 立即手动部署
echo "7. 立即手动部署"
echo "运行自动更新脚本..."
if bash scripts/auto_update_site.sh > /tmp/deploy_test.log 2>&1; then
    echo "✅ 自动更新脚本执行成功"
    echo "生成的文件:"
    find pages/tools -name "*.html" -newer /tmp/deploy_test.log 2>/dev/null | head -5
else
    echo "❌ 自动更新脚本执行失败"
    echo "错误日志:"
    tail -10 /tmp/deploy_test.log
fi
echo ""

# 8. 手动推送变更
echo "8. 手动推送变更"
if git status --porcelain | grep -q "."; then
    echo "检测到未提交的变更"
    git add .
    git commit -m "Manual fix: 修复部署问题 $(date '+%Y-%m-%d %H:%M:%S')"
    if git push origin main; then
        echo "✅ 手动推送成功"
    else
        echo "❌ 手动推送失败"
    fi
else
    echo "✅ 没有未提交的变更"
fi
echo ""

echo "=== 检查完成 ==="
echo "建议:"
echo "1. 检查Vercel项目控制台: https://vercel.com/dashboard"
echo "2. 检查GitHub Actions状态"
echo "3. 如果Vercel部署失败，尝试重新连接GitHub仓库"
echo "4. 等待几分钟让Vercel自动部署生效"