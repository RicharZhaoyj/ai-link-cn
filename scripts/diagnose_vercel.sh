#!/bin/bash

# Vercel网站状态诊断工具
echo "🔍 Vercel网站状态诊断工具"
echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

SITE_URL="https://project-f5cf8.vercel.app"
GITHUB_REPO="RicharZhaoyj/ai-link-cn"

echo "=== 1. 网络连通性测试 ==="

# 1.1 DNS解析
echo "1.1 DNS解析测试..."
nslookup project-f5cf8.vercel.app 2>/dev/null | grep -A2 "Non-auth"
if [ $? -eq 0 ]; then
    echo "✅ DNS解析正常"
else
    echo "❌ DNS解析失败"
fi

# 1.2 基础连通性
echo ""
echo "1.2 基础连通性测试..."
ping -c 3 project-f5cf8.vercel.app 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ ICMP连通正常"
else
    echo "❌ ICMP连通失败"
fi

# 1.3 HTTP访问测试
echo ""
echo "1.3 HTTP访问测试..."
echo "尝试访问: $SITE_URL"

# 尝试多种方法
curl -I --max-time 10 "$SITE_URL" 2>/dev/null | head -1
if [ $? -eq 0 ]; then
    echo "✅ HTTP访问成功"
else
    echo "❌ HTTP访问失败"
    echo "   尝试HTTPS降级到HTTP..."
    curl -I --max-time 10 "http://project-f5cf8.vercel.app" 2>/dev/null | head -1
    if [ $? -eq 0 ]; then
        echo "⚠️  HTTP访问成功，HTTPS可能有问题"
    else
        echo "❌ HTTP/HTTPS均失败"
    fi
fi

echo ""
echo "=== 2. 本地代码状态 ==="

# 2.1 检查Git状态
echo "2.1 Git仓库状态..."
cd /root/.openclaw/workspace 2>/dev/null
if [ $? -eq 0 ]; then
    git status --short | head -5
    echo "当前分支: $(git branch --show-current)"
    echo "远程仓库: $(git remote get-url origin)"
else
    echo "❌ 无法进入工作目录"
fi

# 2.2 检查关键文件
echo ""
echo "2.2 关键文件检查..."
required_files=("index.html" "robots.txt" "sitemap.xml")
for file in "${required_files[@]}"; do
    if [ -f "/root/.openclaw/workspace/$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 缺失"
    fi
done

# 2.3 检查构建配置
echo ""
echo "2.3 构建配置检查..."
if [ -f "/root/.openclaw/workspace/package.json" ]; then
    echo "✅ package.json 存在"
    echo "   Node版本要求: $(grep -o '"node":.*' /root/.openclaw/workspace/package.json 2>/dev/null || echo '未指定')"
elif [ -f "/root/.openclaw/workspace/vercel.json" ]; then
    echo "✅ vercel.json 存在"
else
    echo "⚠️  无构建配置文件，Vercel可能使用默认配置"
fi

echo ""
echo "=== 3. 部署历史分析 ==="

# 3.1 检查部署日志
echo "3.1 部署日志..."
if [ -f "/root/.openclaw/workspace/logs/deployment_history.log" ]; then
    tail -5 "/root/.openclaw/workspace/logs/deployment_history.log"
else
    echo "⚠️  无部署历史日志"
fi

# 3.2 检查自动更新日志
echo ""
echo "3.2 自动更新状态..."
if [ -f "/root/.openclaw/workspace/logs/cron_auto_update.log" ]; then
    last_update=$(tail -1 "/root/.openclaw/workspace/logs/cron_auto_update.log" | grep -o '\[.*\]' | head -1)
    echo "最后自动更新: ${last_update:-未知}"
else
    echo "⚠️  无自动更新日志"
fi

echo ""
echo "=== 4. 可能的问题诊断 ==="

echo "4.1 可能的原因分析:"
echo "1. ❌ Vercel项目被暂停或删除"
echo "   - 需要登录Vercel控制台检查"
echo "2. ❌ GitHub Webhook失效"
echo "   - 需要登录GitHub检查Webhook设置"
echo "3. ❌ 构建配置错误"
echo "   - 可能需要vercel.json或package.json"
echo "4. ❌ 域名/DNS问题"
echo "   - 域名解析到: $(nslookup project-f5cf8.vercel.app 2>/dev/null | grep 'Address:' | tail -1 | awk '{print $2}')"
echo "5. ❌ 网络防火墙/屏蔽"
echo "   - 可能被地区性屏蔽"

echo ""
echo "4.2 快速测试其他Vercel项目..."
curl -I --max-time 5 "https://vercel.com" 2>/dev/null | head -1
if [ $? -eq 0 ]; then
    echo "✅ Vercel主站可访问"
else
    echo "❌ Vercel主站无法访问，可能是网络问题"
fi

echo ""
echo "=== 5. 解决方案建议 ==="

echo "5.1 立即执行:"
echo "   🚨 1. 登录 Vercel控制台 (https://vercel.com)"
echo "      - 检查项目状态"
echo "      - 查看构建日志"
echo "      - 重新触发部署"
echo ""
echo "   🔧 2. 登录 GitHub仓库 (https://github.com/$GITHUB_REPO)"
echo "      - 检查Settings → Webhooks"
echo "      - 验证Vercel Webhook是否正常"
echo "      - 手动触发GitHub Actions"
echo ""
echo "   📝 3. 检查本地配置"
echo "      - 确保有vercel.json或package.json"
echo "      - 验证项目结构符合Vercel要求"

echo ""
echo "5.2 替代方案 (如果Vercel不可用):"
echo "   💡 1. 使用GitHub Pages (免费)"
echo "      - 启用GitHub Pages功能"
echo "      - 切换到gh-pages分支"
echo ""
echo "   💡 2. 使用Netlify (免费)"
echo "      - 连接GitHub仓库"
echo "      - 自动部署"
echo ""
echo "   💡 3. 使用Cloudflare Pages (免费)"
echo "      - 快速部署静态网站"

echo ""
echo "=== 6. 诊断总结 ==="

# 生成状态码
if curl -I --max-time 5 "$SITE_URL" 2>/dev/null | grep -q "200"; then
    STATUS="🟢 正常运行"
elif ping -c 1 project-f5cf8.vercel.app 2>/dev/null; then
    STATUS="🟡 部分问题 (可ping通但HTTP失败)"
else
    STATUS="🔴 完全不可访问"
fi

echo "网站状态: $STATUS"
echo "最后已知更新: 2026-05-18 02:30:06"
echo "GitHub仓库: $GITHUB_REPO"
echo ""

echo "🚀 下一步建议:"
echo "   1. 立即登录Vercel控制台检查项目状态"
echo "   2. 如果Vercel不可用，考虑迁移到GitHub Pages"
echo "   3. 修复后重新测试网站访问"
echo "   4. 开始流量获取计划"

echo ""
echo "📋 检查清单:"
echo "   [ ] 1. Vercel项目状态 ✅/❌"
echo "   [ ] 2. GitHub Webhook设置 ✅/❌"
echo "   [ ] 3. 构建配置正确 ✅/❌"
echo "   [ ] 4. 网站可访问 ✅/❌"