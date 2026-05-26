#!/bin/bash

# AI.link.cn 网站更新部署脚本
# 用于测试和部署网站优化功能

echo "🚀 AI.link.cn 网站优化更新部署脚本"
echo "=========================================="

# 检查必要的文件
echo "📋 检查更新文件..."
FILES=(
    "/root/.openclaw/workspace/index.html"
    "/root/.openclaw/workspace/config/ai_tools_enhanced.json"
    "/root/.openclaw/workspace/pages/quick-input/index.html"
    "/root/.openclaw/workspace/README_WEBSITE_UPDATE.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
        exit 1
    fi
done

# 显示更新摘要
echo ""
echo "📊 更新内容摘要："
echo "------------------"
echo "1. 智能分类导航系统"
echo "   - 按场景、类型、预算筛选"
echo "   - 实时结果计数和排序"
echo "   - 工作流智能推荐"
echo ""
echo "2. 一键输入功能页面"
echo "   - 位置: /pages/quick-input/"
echo "   - 支持多工具模板"
echo "   - 实时编辑和预览"
echo ""
echo "3. 商业化架构准备"
echo "   - 免费增值服务模型"
echo "   - 分层功能设计"
echo ""

# 验证HTML语法
echo "🔍 验证HTML语法..."
if command -v tidy &> /dev/null; then
    tidy -q -errors /root/.openclaw/workspace/index.html 2>&1 | head -20
    echo "✅ HTML语法检查完成"
else
    echo "⚠️  tidy未安装，跳过HTML语法检查"
fi

# 检查文件大小
echo ""
echo "📏 文件大小检查："
ls -lh /root/.openclaw/workspace/index.html
ls -lh /root/.openclaw/workspace/pages/quick-input/index.html

# 检查关键功能点
echo ""
echo "🔧 关键功能点检查："
echo "------------------"

# 检查分类导航元素
echo "检查分类导航元素..."
if grep -q "category-navigation" /root/.openclaw/workspace/index.html; then
    echo "✅ 分类导航组件已集成"
else
    echo "❌ 分类导航组件未找到"
fi

# 检查一键输入链接
echo "检查一键输入链接..."
if grep -q "/pages/quick-input/" /root/.openclaw/workspace/index.html; then
    echo "✅ 一键输入链接已添加"
else
    echo "❌ 一键输入链接未找到"
fi

# 检查增强的工具数据
echo "检查工具数据库..."
if [ -f "/root/.openclaw/workspace/config/ai_tools_enhanced.json" ]; then
    TOOL_COUNT=$(grep -c '"name"' /root/.openclaw/workspace/config/ai_tools_enhanced.json)
    echo "✅ 工具数据库包含 $TOOL_COUNT 个工具"
else
    echo "❌ 工具数据库未找到"
fi

# 创建测试页面
echo ""
echo "🧪 创建测试页面..."
cat > /tmp/test_website_update.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>AI.link.cn 更新测试</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .test-result { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .warning { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <h1>AI.link.cn 网站更新测试</h1>
    <div id="testResults"></div>
    
    <script>
        const tests = [
            { name: "主页面可访问", url: "/", type: "page" },
            { name: "一键输入页面", url: "/pages/quick-input/", type: "page" },
            { name: "分类导航功能", url: "/", check: "category-navigation", type: "element" },
            { name: "工具数据", url: "/config/ai_tools_enhanced.json", type: "data" }
        ];
        
        const results = [];
        
        async function runTests() {
            const resultsDiv = document.getElementById('testResults');
            
            for (const test of tests) {
                const resultDiv = document.createElement('div');
                resultDiv.className = 'test-result';
                resultDiv.innerHTML = `<strong>${test.name}:</strong> 测试中...`;
                resultsDiv.appendChild(resultDiv);
                
                try {
                    if (test.type === 'page') {
                        const response = await fetch(test.url);
                        if (response.ok) {
                            resultDiv.innerHTML = `<strong>${test.name}:</strong> ✅ 通过`;
                            resultDiv.className = 'test-result success';
                        } else {
                            throw new Error(`HTTP ${response.status}`);
                        }
                    } else if (test.type === 'element') {
                        // 检查元素是否存在
                        if (document.querySelector('.category-navigation')) {
                            resultDiv.innerHTML = `<strong>${test.name}:</strong> ✅ 通过`;
                            resultDiv.className = 'test-result success';
                        } else {
                            throw new Error('元素未找到');
                        }
                    } else if (test.type === 'data') {
                        const response = await fetch(test.url);
                        if (response.ok) {
                            const data = await response.json();
                            resultDiv.innerHTML = `<strong>${test.name}:</strong> ✅ 通过 (${Object.keys(data.categories || {}).length}个分类)`;
                            resultDiv.className = 'test-result success';
                        } else {
                            throw new Error(`HTTP ${response.status}`);
                        }
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<strong>${test.name}:</strong> ❌ 失败 (${error.message})`;
                    resultDiv.className = 'test-result error';
                }
            }
        }
        
        // 运行测试
        if (window.location.pathname === '/test_website_update.html') {
            runTests();
        }
    </script>
</body>
</html>
EOF

echo "✅ 测试页面已创建: /tmp/test_website_update.html"

# 部署建议
echo ""
echo "🚀 部署建议："
echo "------------------"
echo "1. 本地测试：在浏览器中打开 /tmp/test_website_update.html"
echo "2. 功能验证：手动测试分类筛选和一键输入功能"
echo "3. Git提交：将更新提交到Git仓库"
echo "4. Vercel部署：推送到GitHub触发自动部署"
echo "5. 用户测试：收集早期用户反馈"

echo ""
echo "✅ 网站更新准备完成！"
echo ""
echo "📝 下一步："
echo "   1. 测试更新功能"
echo "   2. 提交代码到Git"
echo "   3. 部署到生产环境"
echo "   4. 监控用户反馈"