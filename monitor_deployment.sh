#!/bin/bash

# AI.link.cn 部署监控脚本
# 监控Vercel部署进度

echo "🚀 AI.link.cn 部署监控"
echo "========================"
echo "监控开始时间: $(date)"
echo ""

# 部署信息
COMMIT_HASH="e7192c7"
COMMIT_MESSAGE="feat: 添加智能分类导航和一键输入功能"
DEPLOY_URL="https://project-f5cf8.vercel.app/"
GITHUB_URL="https://github.com/RicharZhaoyj/ai-link-cn"

echo "📊 部署信息"
echo "-----------"
echo "提交哈希: $COMMIT_HASH"
echo "提交内容: $COMMIT_MESSAGE"
echo "部署地址: $DEPLOY_URL"
echo "GitHub仓库: $GITHUB_URL"
echo ""

# 检查GitHub推送状态
echo "🔍 检查GitHub推送状态"
echo "---------------------"
if curl -s "https://api.github.com/repos/RicharZhaoyj/ai-link-cn/commits/$COMMIT_HASH" | grep -q "sha"; then
    echo "✅ 提交已成功推送到GitHub"
    echo "   可访问: $GITHUB_URL/commit/$COMMIT_HASH"
else
    echo "⏳ GitHub API可能需要几秒钟同步"
fi
echo ""

# Vercel部署监控
echo "📡 Vercel部署监控"
echo "-----------------"
echo "注意: Vercel通常会在1-3分钟内自动检测到推送并开始部署"
echo ""

# 部署状态检查循环
echo "🔄 开始部署状态检查（每30秒检查一次）"
echo "--------------------------------------"

CHECK_COUNT=0
MAX_CHECKS=20  # 最多检查10分钟（20次×30秒）

while [ $CHECK_COUNT -lt $MAX_CHECKS ]; do
    CHECK_COUNT=$((CHECK_COUNT + 1))
    CURRENT_TIME=$(date "+%H:%M:%S")
    
    echo ""
    echo "[$CURRENT_TIME] 第 $CHECK_COUNT 次检查"
    echo "----------------------------"
    
    # 尝试访问网站
    echo "检查网站可访问性..."
    if timeout 5 curl -s -o /dev/null -w "%{http_code}" "$DEPLOY_URL" > /tmp/http_code.txt 2>/dev/null; then
        HTTP_CODE=$(cat /tmp/http_code.txt)
        if [ "$HTTP_CODE" = "200" ]; then
            echo "✅ 网站可访问 (HTTP 200)"
            
            # 检查新功能
            echo "检查新功能..."
            if timeout 10 curl -s "$DEPLOY_URL" | grep -q "category-navigation"; then
                echo "✅ 智能分类导航功能已部署"
                
                if timeout 10 curl -s "$DEPLOY_URL" | grep -q "/pages/quick-input/"; then
                    echo "✅ 一键输入功能入口已部署"
                    
                    echo ""
                    echo "🎉 部署完成！"
                    echo "==============="
                    echo "✅ 所有新功能已成功部署到生产环境"
                    echo ""
                    echo "🔗 测试链接："
                    echo "   主页面: $DEPLOY_URL"
                    echo "   一键输入: ${DEPLOY_URL}pages/quick-input/"
                    echo ""
                    echo "📱 功能验证："
                    echo "   1. 打开主页面查看分类导航"
                    echo "   2. 测试不同的筛选条件"
                    echo "   3. 点击'一键输入'测试模板功能"
                    echo "   4. 检查移动端响应式设计"
                    echo ""
                    echo "⏱️ 总耗时: $((CHECK_COUNT * 30)) 秒"
                    exit 0
                else
                    echo "⏳ 一键输入功能尚未完全部署"
                fi
            else
                echo "⏳ 分类导航功能尚未完全部署"
            fi
        else
            echo "⚠️ 网站返回 HTTP $HTTP_CODE"
        fi
    else
        echo "⏳ 网站暂时无法访问或正在部署中"
    fi
    
    # 如果不是最后一次检查，等待30秒
    if [ $CHECK_COUNT -lt $MAX_CHECKS ]; then
        echo "等待30秒后再次检查..."
        sleep 30
    fi
done

echo ""
echo "⏰ 部署监控超时（10分钟）"
echo "========================"
echo "Vercel部署可能需要更多时间。建议："
echo ""
echo "1. 手动访问: $DEPLOY_URL"
echo "2. 检查Vercel控制台: https://vercel.com/dashboard"
echo "3. 查看部署日志确认状态"
echo ""
echo "如果部署失败，常见原因："
echo "   - 构建错误（检查控制台日志）"
echo "   - 环境配置问题"
echo "   - 依赖安装失败"
echo ""
echo "可以稍后再运行此脚本检查部署状态。"

# 创建部署完成检查清单
cat > /tmp/deployment_complete_checklist.md << 'EOF'
# AI.link.cn 部署完成检查清单

## ✅ 部署状态
- [ ] 网站可访问 (HTTP 200)
- [ ] 智能分类导航功能正常
- [ ] 一键输入页面可访问
- [ ] 所有新功能正常工作

## 🔗 测试链接
- 主页面: https://project-f5cf8.vercel.app/
- 一键输入: https://project-f5cf8.vercel.app/pages/quick-input/

## 🧪 功能测试
### 主页面
- [ ] 分类导航组件显示正常
- [ ] 筛选功能工作正常
- [ ] 工具卡片显示完整
- [ ] 一键输入链接正确

### 一键输入页面
- [ ] 页面加载正常
- [ ] 工具选择器工作
- [ ] 模板加载正常
- [ ] 编辑功能正常
- [ ] 导出功能正常

## 📱 兼容性测试
- [ ] Chrome浏览器
- [ ] Firefox浏览器
- [ ] Safari浏览器
- [ ] 移动端响应式

## 📊 性能检查
- [ ] 页面加载速度 (<3秒)
- [ ] 无JavaScript错误
- [ ] 无控制台警告
- [ ] 图片和资源加载正常

## 📝 后续行动
1. 收集用户反馈
2. 监控网站访问统计
3. 准备社交媒体宣传
4. 开始内容创作计划
EOF

echo ""
echo "检查清单已保存到: /tmp/deployment_complete_checklist.md"