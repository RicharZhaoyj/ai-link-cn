#!/bin/bash

# AI.link.cn 部署状态检查脚本

echo "🚀 AI.link.cn 部署状态检查"
echo "================================"
echo "检查时间: $(date)"
echo ""

# 1. 检查Git状态
echo "📊 1. Git状态检查"
echo "------------------"
echo "当前分支: $(git branch --show-current 2>/dev/null || echo '未知')"
echo "最后提交: $(git log --oneline -1 2>/dev/null || echo '无提交记录')"
echo "未提交的更改: $(git status --porcelain | wc -l) 个文件"
echo ""

# 2. 检查更新文件
echo "📋 2. 更新文件检查"
echo "------------------"
FILES=(
    "index.html"
    "pages/quick-input/index.html"
    "config/ai_tools_enhanced.json"
    "README_WEBSITE_UPDATE.md"
    "components/category_navigation.html"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        echo "✅ $file ($size)"
    else
        echo "❌ $file (缺失)"
    fi
done
echo ""

# 3. 检查网站功能
echo "🔧 3. 功能检查"
echo "------------------"

# 检查主页面功能
if grep -q "category-navigation" index.html; then
    echo "✅ 主页面包含分类导航"
else
    echo "❌ 主页面缺少分类导航"
fi

if grep -q "/pages/quick-input/" index.html; then
    echo "✅ 主页面包含一键输入链接"
else
    echo "❌ 主页面缺少一键输入链接"
fi

# 检查一键输入页面
if [ -f "pages/quick-input/index.html" ]; then
    if grep -q "tool-selector" pages/quick-input/index.html; then
        echo "✅ 一键输入页面功能完整"
    else
        echo "❌ 一键输入页面结构不完整"
    fi
fi

# 4. 检查文件结构
echo ""
echo "📁 4. 文件结构检查"
echo "------------------"
find . -name "*.html" -type f | grep -E "(index\.html|quick-input)" | head -10 | while read file; do
    echo "  📄 $file"
done
echo ""

# 5. 部署建议
echo "🚀 5. 部署建议"
echo "------------------"
echo "如果Git状态正常，可以执行以下命令："
echo ""
echo "1. 推送到GitHub:"
echo "   git push origin main"
echo ""
echo "2. 检查Vercel部署:"
echo "   - Vercel会自动检测到推送并开始部署"
echo "   - 部署完成后访问: https://project-f5cf8.vercel.app/"
echo "   - 检查部署日志: Vercel控制台 → Deployments"
echo ""
echo "3. 测试部署后的网站:"
echo "   主页面: https://project-f5cf8.vercel.app/"
echo "   一键输入: https://project-f5cf8.vercel.app/pages/quick-input/"
echo ""
echo "4. 验证功能:"
echo "   - 测试分类导航筛选功能"
echo "   - 测试一键输入模板功能"
echo "   - 检查移动端响应式设计"
echo ""

# 6. 检查网络连接
echo "🌐 6. 网络连接检查"
echo "------------------"
echo "检查是否可以访问GitHub和Vercel:"

# 检查GitHub连接
if timeout 3 curl -s https://github.com > /dev/null; then
    echo "✅ GitHub可访问"
else
    echo "❌ GitHub无法访问"
fi

# 检查Vercel连接
if timeout 3 curl -s https://vercel.com > /dev/null; then
    echo "✅ Vercel可访问"
else
    echo "❌ Vercel无法访问"
fi

# 7. 创建部署检查清单
echo ""
echo "📝 7. 部署检查清单"
echo "------------------"
cat > /tmp/deployment_checklist.md << 'EOF'
# AI.link.cn 部署检查清单

## ✅ 已完成的步骤
- [x] 更新主页面 (index.html)
- [x] 创建一键输入页面 (pages/quick-input/)
- [x] 创建增强工具数据库 (config/ai_tools_enhanced.json)
- [x] 创建更新文档 (README_WEBSITE_UPDATE.md)
- [x] 提交更改到本地Git仓库

## ⏳ 待完成的步骤
- [ ] 推送到GitHub远程仓库
- [ ] 等待Vercel自动部署完成
- [ ] 验证生产环境功能
- [ ] 收集用户反馈

## 🔧 功能验证清单
### 主页面
- [ ] 分类导航组件正常显示
- [ ] 筛选功能正常工作
- [ ] 一键输入链接正确
- [ ] 响应式设计适配

### 一键输入页面
- [ ] 页面正常加载
- [ ] 工具选择器工作
- [ ] 模板加载正常
- [ ] 编辑功能正常
- [ ] 导出功能正常

### 数据库
- [ ] JSON格式正确
- [ ] 工具数据完整
- [ ] 分类结构合理

## 🚀 部署命令
```bash
# 推送到GitHub
git push origin main

# 验证部署
curl -I https://project-f5cf8.vercel.app/

# 测试功能
# 主页面: https://project-f5cf8.vercel.app/
# 一键输入: https://project-f5cf8.vercel.app/pages/quick-input/
```

## 📞 故障排除
1. **部署失败**: 检查Vercel部署日志
2. **功能异常**: 检查浏览器控制台错误
3. **样式问题**: 检查CSS加载
4. **数据问题**: 检查JSON格式

## 📊 成功指标
- 网站正常访问 (HTTP 200)
- 所有功能正常工作
- 无JavaScript错误
- 响应时间合理 (<3秒)
EOF

echo "检查清单已保存到: /tmp/deployment_checklist.md"
echo ""
echo "✅ 部署检查完成！"
echo ""
echo "下一步建议:"
echo "1. 执行 'git push origin main' 推送更改"
echo "2. 等待几分钟让Vercel完成部署"
echo "3. 访问 https://project-f5cf8.vercel.app/ 验证更新"