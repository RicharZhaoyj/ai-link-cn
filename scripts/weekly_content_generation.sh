#!/bin/bash
# 每周内容生成脚本

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/content_generation_$(date +%Y%m%d).log"
NODE_PATH="/root/.nvm/versions/node/v22.22.1/bin/node"

echo "=== 每周内容生成开始 $(date) ===" > "$LOG_FILE"

cd "$WORKSPACE"

# 检查新工具数据
echo "检查新工具数据..." >> "$LOG_FILE"
NEW_TOOLS_DIR="$WORKSPACE/discovered_tools"
RECENT_REPORTS=$(find "$NEW_TOOLS_DIR" -name "new_tools_*.md" -type f -mtime -7 | head -5)

if [ -n "$RECENT_REPORTS" ]; then
    echo "找到近期工具报告:" >> "$LOG_FILE"
    echo "$RECENT_REPORTS" >> "$LOG_FILE"
    
    # 生成内容创意
    echo "生成内容创意..." >> "$LOG_FILE"
    $NODE_PATH -e "
        const fs = require('fs');
        const path = require('path');
        
        const reports = \`$RECENT_REPORTS\`.split('\\n').filter(r => r.trim());
        let allTools = [];
        
        reports.forEach(reportPath => {
            try {
                const content = fs.readFileSync(reportPath, 'utf8');
                const toolsMatch = content.match(/#### ([^\n]+)/g) || [];
                toolsMatch.forEach(match => {
                    const toolName = match.replace('#### ', '').trim();
                    if (toolName && !allTools.includes(toolName)) {
                        allTools.push(toolName);
                    }
                });
            } catch (error) {
                console.error('读取报告失败:', reportPath, error.message);
            }
        });
        
        console.log('本周可评测工具:', allTools);
        
        // 生成内容计划
        const contentPlan = \`# 本周内容计划
生成时间: \${new Date().toLocaleString('zh-CN')}

## 可用工具 (\${allTools.length}个)
\${allTools.map((tool, i) => \`\${i+1}. \${tool}\`).join('\\n')}

## 内容创意
1. 选择3-5个工具进行深度评测
2. 创建工具对比文章
3. 制作实用技巧教程
4. 分享行业应用案例

## 执行建议
- 周一: 确定本周评测工具
- 周二-周四: 撰写评测内容
- 周五: 优化和发布
- 周末: 社交媒体推广

---\`;
        
        const planPath = path.join('$WORKSPACE', 'content_plans', \`weekly_plan_\${Date.now()}.md\`);
        fs.mkdirSync(path.dirname(planPath), { recursive: true });
        fs.writeFileSync(planPath, contentPlan, 'utf8');
        console.log('内容计划已保存:', planPath);
    " >> "$LOG_FILE" 2>&1
else
    echo "本周没有新工具报告" >> "$LOG_FILE"
fi

echo "=== 每周内容生成完成 $(date) ===" >> "$LOG_FILE"
