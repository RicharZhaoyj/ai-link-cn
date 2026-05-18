#!/bin/bash

# GitHub Pages部署备选方案
echo "🚀 GitHub Pages备选部署方案"
echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKSPACE="/root/.openclaw/workspace"
GH_PAGES_BRANCH="gh-pages"

echo "=== 1. 检查当前状态 ==="

# 检查Git状态
cd "$WORKSPACE" || exit 1
echo "当前分支: $(git branch --show-current)"
echo "未提交的更改:"
git status --short | head -10

echo ""
echo "=== 2. 准备GitHub Pages部署 ==="

# 创建gh-pages分支的部署目录
TEMP_DIR="/tmp/gh-pages-$(date +%s)"
mkdir -p "$TEMP_DIR"

echo "复制文件到临时目录..."
cp -r *.html "$TEMP_DIR/"
cp -r pages "$TEMP_DIR/
cp -r css "$TEMP_DIR/
cp robots.txt sitemap.xml "$TEMP_DIR/" 2>/dev/null

echo "创建GitHub Pages配置..."
cat > "$TEMP_DIR/.nojekyll" << EOF
# 禁用Jekyll处理
EOF

cat > "$TEMP_DIR/index.html" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=./pages/tools/index.html">
    <title>AI.link.cn - 重定向中</title>
</head>
<body>
    <p>正在重定向到工具列表页面...</p>
    <script>
        window.location.href = "./pages/tools/index.html";
    </script>
</body>
</html>
EOF

echo ""
echo "=== 3. 创建GitHub Actions工作流 ==="

GITHUB_ACTIONS_DIR="$WORKSPACE/.github/workflows"
mkdir -p "$GITHUB_ACTIONS_DIR"

cat > "$GITHUB_ACTIONS_DIR/deploy.yml" << EOF
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Pages
        uses: actions/configure-pages@v3

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: .

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v2
EOF

echo "✅ GitHub Actions工作流已创建: .github/workflows/deploy.yml"

echo ""
echo "=== 4. 部署指令 ==="

echo "🔧 手动部署步骤:"
echo ""
echo "1. 提交更改到GitHub:"
echo "   git add ."
echo "   git commit -m '准备GitHub Pages部署'"
echo "   git push origin main"
echo ""
echo "2. 启用GitHub Pages:"
echo "   访问 https://github.com/RicharZhaoyj/ai-link-cn/settings/pages"
echo "   设置 Source: GitHub Actions"
echo ""
echo "3. 运行部署工作流:"
echo "   访问 https://github.com/RicharZhaoyj/ai-link-cn/actions"
echo "   运行 'Deploy to GitHub Pages' 工作流"
echo ""
echo "4. 访问网站:"
echo "   https://richarzhaoyj.github.io/ai-link-cn/"

echo ""
echo "=== 5. 备选方案: Netlify部署 ==="

cat > "$WORKSPACE/netlify.toml" << EOF
[build]
  publish = "."
  command = "echo 'No build required'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/css/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
EOF

echo "✅ Netlify配置文件已创建: netlify.toml"
echo ""
echo "🔧 Netlify部署步骤:"
echo "1. 访问 https://app.netlify.com/"
echo "2. 连接GitHub仓库"
echo "3. 自动部署完成"
echo "4. 获得免费域名: *.netlify.app"

echo ""
echo "=== 6. 总结 ==="

echo "🎯 建议部署方案:"
echo ""
echo "方案1: GitHub Pages (推荐)"
echo "   ✅ 完全免费"
echo "   ✅ 集成GitHub工作流"
echo "   ✅ 自定义域名支持"
echo "   ⚠️  需要手动配置"
echo ""
echo "方案2: Netlify"
echo "   ✅ 部署简单"
echo "   ✅ 自动SSL"
echo "   ✅ 全球CDN"
echo "   ✅ 免费计划充足"
echo ""
echo "方案3: Cloudflare Pages"
echo "   ✅ 极速全球网络"
echo "   ✅ 免费自定义域名"
echo "   ✅ 自动构建部署"
echo ""
echo "🚀 立即行动建议:"
echo "   1. 先尝试修复Vercel项目"
echo "   2. 如果Vercel不可用，启用GitHub Pages"
echo "   3. 同时配置Netlify作为备份"

echo ""
echo "📋 检查清单:"
echo "   [ ] 1. GitHub仓库设置为公开"
echo "   [ ] 2. 启用GitHub Pages"
echo "   [ ] 3. 配置自定义域名 (可选)"
echo "   [ ] 4. 测试网站访问"