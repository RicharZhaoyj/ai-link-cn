#!/bin/bash

# SEO检查脚本
echo "=== AI.link.cn SEO优化状态检查 ==="
echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKSPACE="/root/.openclaw/workspace"

# 1. 检查基础SEO元素
echo "1. 基础SEO元素检查:"
for page in index.html pages/tools/index.html; do
    if [ -f "$WORKSPACE/$page" ]; then
        echo "  $(basename $page):"
        grep -q "<title>" "$WORKSPACE/$page" && echo "    ✅ Title标签: 存在" || echo "    ❌ Title标签: 缺失"
        grep -q "meta.*description" "$WORKSPACE/$page" && echo "    ✅ Meta描述: 存在" || echo "    ❌ Meta描述: 缺失"
        grep -q "og:title\|og:description" "$WORKSPACE/$page" && echo "    ✅ Open Graph: 存在" || echo "    ❌ Open Graph: 缺失"
        grep -q "twitter:card\|twitter:title" "$WORKSPACE/$page" && echo "    ✅ Twitter卡片: 存在" || echo "    ❌ Twitter卡片: 缺失"
    fi
done
echo ""

# 2. 检查技术SEO
echo "2. 技术SEO检查:"
[ -f "$WORKSPACE/robots.txt" ] && echo "  ✅ robots.txt: 存在" || echo "  ❌ robots.txt: 缺失"
[ -f "$WORKSPACE/sitemap.xml" ] && echo "  ✅ sitemap.xml: 存在" || echo "  ❌ sitemap.xml: 缺失"

# 检查结构化数据
schema_count=$(find "$WORKSPACE" -name "*.html" -type f -exec grep -l "schema\|ld+json" {} \; | wc -l)
echo "  📊 结构化数据: $schema_count 个页面包含"
echo ""

# 3. 检查页面优化
echo "3. 页面优化检查:"
for page in index.html pages/tools/index.html; do
    if [ -f "$WORKSPACE/$page" ]; then
        h1_count=$(grep -c "<h1" "$WORKSPACE/$page")
        echo "  $(basename $page): H1标签数量: $h1_count"
        img_count=$(grep -c "<img" "$WORKSPACE/$page")
        img_alt_count=$(grep -c "alt=" "$WORKSPACE/$page")
        echo "    图片数量: $img_count, 有alt文本: $img_alt_count"
    fi
done
echo ""

# 4. 检查速度优化
echo "4. 速度优化检查:"
if [ -d "$WORKSPACE/css" ]; then
    css_size=$(du -sh "$WORKSPACE/css" | cut -f1)
    echo "  CSS文件夹大小: $css_size"
fi
echo ""

# 5. 关键词优化
echo "5. 关键词优化检查:"
if [ -f "$WORKSPACE/config/seo_keywords.json" ]; then
    echo "  ✅ SEO关键词配置文件: 存在"
    primary_count=$(grep -c '"primary_keywords"' "$WORKSPACE/config/seo_keywords.json")
    echo "    主要关键词数量: $primary_count"
else
    echo "  ❌ SEO关键词配置文件: 缺失"
fi
echo ""

echo "=== SEO优化建议 ==="
echo "1. 立即执行:"
echo "   • 创建robots.txt和sitemap.xml"
echo "   • 添加Open Graph和Twitter卡片标签"
echo "   • 为所有工具页面添加结构化数据"
echo ""
echo "2. 短期优化:"
echo "   • 压缩CSS文件"
echo "   • 为所有图片添加alt文本"
echo "   • 基于关键词配置文件优化页面内容"
echo ""
echo "3. 长期优化:"
echo "   • 实现自动SEO检查和优化"
echo "   • 添加页面加载优化 (懒加载、延迟加载)"
echo "   • 创建内容更新计划"