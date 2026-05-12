#!/bin/bash
# Vercel构建脚本

echo "🚀 开始构建 AI.link.cn 项目..."

# 检查必要文件
echo "📁 检查项目文件..."
if [ ! -f "package.json" ]; then
  echo "❌ package.json 不存在"
  exit 1
fi

if [ ! -f "index.html" ]; then
  echo "❌ index.html 不存在"
  exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
npm install --production

# 创建必要的目录
echo "📁 创建目录结构..."
mkdir -p api config docs scripts src

# 创建构建信息文件
echo "📊 创建构建信息..."
cat > build-info.json << EOF
{
  "project": "ai-link-cn",
  "version": "1.0.0",
  "build_date": "$(date -Iseconds)",
  "build_environment": "$NODE_ENV",
  "site_url": "$SITE_URL",
  "features": [
    "ai-tools-reviews",
    "affiliate-marketing",
    "seo-optimized",
    "responsive-design"
  ]
}
EOF

# 复制配置文件
echo "⚙️ 复制配置文件..."
cp -r config/* . 2>/dev/null || true

# 创建部署就绪文件
echo "✅ 创建部署就绪标记..."
cat > .deploy-ready << EOF
AI.link.cn - 部署就绪
构建时间: $(date)
版本: 1.0.0
状态: 准备上线
EOF

# 验证构建
echo "🔍 验证构建..."
if [ -f "index.html" ] && [ -f "package.json" ]; then
  echo "✅ 构建成功!"
  echo "📊 构建统计:"
  echo "  - HTML文件: index.html ($(wc -l < index.html) 行)"
  echo "  - 配置文件: $(ls config/*.json 2>/dev/null | wc -l) 个"
  echo "  - 源代码: $(ls src/*.js 2>/dev/null | wc -l) 个"
  echo "  - 文档: $(ls docs/*.md 2>/dev/null | wc -l) 个"
else
  echo "❌ 构建失败: 缺少必要文件"
  exit 1
fi

echo ""
echo "🎉 AI.link.cn 构建完成!"
echo "🌐 网站将部署到: $SITE_URL"
echo "📅 构建时间: $(date)"
echo "🚀 准备上线!"