#!/bin/bash

# AI.link.cn 定期任务设置脚本
# 自动设置内容发现、推广、监控等定时任务

set -e

# 配置
WORKSPACE_DIR="/root/.openclaw/workspace"
SCRIPTS_DIR="$WORKSPACE_DIR/scripts"
LOG_DIR="$WORKSPACE_DIR/logs"
BACKUP_DIR="$WORKSPACE_DIR/backups"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# 创建必要的目录
create_directories() {
    log "创建必要的目录..."
    
    mkdir -p "$LOG_DIR"
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$SCRIPTS_DIR"
    mkdir -p "$WORKSPACE_DIR/discovered_tools"
    
    success "目录创建完成"
}

# 安装必要的依赖
install_dependencies() {
    log "检查Node.js依赖..."
    
    if [ ! -f "$WORKSPACE_DIR/package.json" ]; then
        warning "未找到package.json，创建基础配置..."
        cat > "$WORKSPACE_DIR/package.json" << EOF
{
  "name": "ai-link-cn",
  "version": "1.0.0",
  "description": "AI工具评测平台",
  "main": "index.js",
  "scripts": {
    "discover-tools": "node scripts/ai_tools_discoverer.js",
    "check-affiliate": "node scripts/affiliate_tracker.js list",
    "generate-content": "node scripts/content_generator.js",
    "test": "echo \"测试暂未实现\" && exit 0"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "cheerio": "^1.0.0-rc.12",
    "node-cron": "^3.0.3",
    "nodemailer": "^6.9.7",
    "puppeteer": "^21.6.0"
  },
  "devDependencies": {
    "eslint": "^8.56.0"
  }
}
EOF
        success "创建package.json完成"
    fi
    
    # 检查是否已安装Node.js
    if ! command -v node &> /dev/null; then
        error "Node.js未安装，请先安装Node.js"
        exit 1
    fi
    
    # 安装依赖
    log "安装Node.js依赖..."
    cd "$WORKSPACE_DIR"
    npm install
    
    success "依赖安装完成"
}

# 创建定期任务脚本
create_cron_scripts() {
    log "创建定期任务脚本..."
    
    # 1. 每日工具发现脚本
    cat > "$SCRIPTS_DIR/daily_discovery.sh" << 'EOF'
#!/bin/bash
# 每日AI工具发现脚本

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/discovery_$(date +%Y%m%d).log"
NODE_PATH="/root/.nvm/versions/node/v22.22.1/bin/node"

echo "=== 每日AI工具发现开始 $(date) ===" > "$LOG_FILE"

cd "$WORKSPACE"

# 运行工具发现器
echo "运行AI工具发现器..." >> "$LOG_FILE"
$NODE_PATH scripts/ai_tools_discoverer.js >> "$LOG_FILE" 2>&1

# 生成发现报告
echo "生成发现报告..." >> "$LOG_FILE"
if [ -f "$WORKSPACE/discovered_tools/new_tools_*.md" ]; then
    NEW_TOOLS_COUNT=$(find "$WORKSPACE/discovered_tools" -name "new_tools_*.md" -type f -mtime -1 | wc -l)
    echo "今日发现新工具: $NEW_TOOLS_COUNT" >> "$LOG_FILE"
    
    # 如果有新工具，发送通知（可选）
    if [ "$NEW_TOOLS_COUNT" -gt 0 ]; then
        echo "🎉 发现 $NEW_TOOLS_COUNT 个新AI工具" >> "$LOG_FILE"
        # 这里可以添加邮件通知或Slack通知
    fi
fi

echo "=== 每日AI工具发现完成 $(date) ===" >> "$LOG_FILE"
EOF
    
    # 2. 每周内容生成脚本
    cat > "$SCRIPTS_DIR/weekly_content_generation.sh" << 'EOF'
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
EOF
    
    # 3. 每月推广分析脚本
    cat > "$SCRIPTS_DIR/monthly_promotion_analysis.sh" << 'EOF'
#!/bin/bash
# 每月推广分析脚本

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/promotion_analysis_$(date +%Y%m).log"
REPORT_DIR="$WORKSPACE/reports"

echo "=== 每月推广分析开始 $(date) ===" > "$LOG_FILE"

# 创建报告目录
mkdir -p "$REPORT_DIR"

# 分析日志文件
echo "分析日志文件..." >> "$LOG_FILE"
DISCOVERY_LOGS=$(find "$WORKSPACE/logs" -name "discovery_*.log" -type f -mtime -30)
CONTENT_LOGS=$(find "$WORKSPACE/logs" -name "content_generation_*.log" -type f -mtime -30)

# 生成月度报告
cat > "$REPORT_DIR/monthly_report_$(date +%Y%m).md" << REPORTEOF
# AI.link.cn 月度报告
报告周期: $(date -d "30 days ago" +%Y-%m-%d) 至 $(date +%Y-%m-%d)
生成时间: $(date)

## 📊 发现统计
### 工具发现
- 扫描次数: $(echo "$DISCOVERY_LOGS" | wc -l)
- 发现新工具: $(grep -h "新工具:" $DISCOVERY_LOGS 2>/dev/null | awk '{sum+=\$2} END {print sum}') 个

### 内容生成
- 内容计划生成: $(echo "$CONTENT_LOGS" | wc -l) 次
- 评测文章产出: $(find "$WORKSPACE/pages/tools" -name "*.html" -type f -mtime -30 | wc -l) 篇

## 🎯 表现分析
### 成功指标
1. **内容覆盖率**: [根据实际数据填写]
2. **工具更新率**: [根据实际数据填写]
3. **用户参与度**: [根据实际数据填写]

### 改进建议
1. 提高工具发现效率
2. 优化内容生成流程
3. 加强推广效果追踪

## 📈 下月计划
### 目标设定
1. 新增评测: 8-10篇
2. 覆盖新类别: 2-3个
3. 用户增长: 提升30%

### 重点任务
1. [ ] 深度评测3个主流工具
2. [ ] 创建2个对比分析
3. [ ] 优化网站SEO
4. [ ] 加强社交媒体推广

## 🔧 技术改进
### 自动化优化
- 提升工具发现准确性
- 改进内容生成模板
- 优化任务调度机制

### 监控增强
- 设置实时监控告警
- 增加用户行为分析
- 完善数据统计系统

---
*本报告由自动化系统生成*
REPORTEOF

echo "月度报告已生成: $REPORT_DIR/monthly_report_$(date +%Y%m).md" >> "$LOG_FILE"

echo "=== 每月推广分析完成 $(date) ===" >> "$LOG_FILE"
EOF
    
    # 4. 备份脚本
    cat > "$SCRIPTS_DIR/backup_system.sh" << 'EOF'
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
    "$WORKSPACE/pages" \
    "$WORKSPACE/scripts" \
    "$WORKSPACE/*.md" \
    "$WORKSPACE/*.html" \
    --exclude="node_modules" \
    --exclude=".git" \
    --exclude="backups"

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
EOF
    
    # 设置执行权限
    chmod +x "$SCRIPTS_DIR/"*.sh
    
    success "定期任务脚本创建完成"
}

# 设置Cron定时任务
setup_cron_jobs() {
    log "设置Cron定时任务..."
    
    # 创建Cron配置文件
    CRON_FILE="$SCRIPTS_DIR/cron-jobs"
    
    cat > "$CRON_FILE" << EOF
# AI.link.cn 定时任务配置
# 生成时间: $(date)

# 每日凌晨2点执行工具发现
0 2 * * * $SCRIPTS_DIR/daily_discovery.sh >> $LOG_DIR/cron_daily.log 2>&1

# 每周一早上6点执行内容生成
0 6 * * 1 $SCRIPTS_DIR/weekly_content_generation.sh >> $LOG_DIR/cron_weekly.log 2>&1

# 每月1号早上8点执行推广分析
0 8 1 * * $SCRIPTS_DIR/monthly_promotion_analysis.sh >> $LOG_DIR/cron_monthly.log 2>&1

# 每周日凌晨3点执行系统备份
0 3 * * 0 $SCRIPTS_DIR/backup_system.sh >> $LOG_DIR/cron_backup.log 2>&1

# 每小时检查一次系统状态（可选）
# 0 * * * * $SCRIPTS_DIR/health_check.sh >> $LOG_DIR/cron_health.log 2>&1
EOF
    
    # 安装Cron任务
    if command -v crontab &> /dev/null; then
        # 备份现有Cron
        crontab -l > "$SCRIPTS_DIR/cron_backup_$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
        
        # 安装新Cron
        crontab "$CRON_FILE"
        
        success "Cron定时任务设置完成"
        echo ""
        echo "已设置的定时任务："
        crontab -l
    else
        warning "Cron未安装，请手动安装："
        echo "Ubuntu/Debian: sudo apt-get install cron"
        echo "CentOS/RHEL: sudo yum install cronie"
        echo ""
        echo "安装后手动添加以下Cron任务："
        cat "$CRON_FILE"
    fi
}

# 创建健康检查脚本
create_health_check() {
    log "创建健康检查脚本..."
    
    cat > "$SCRIPTS_DIR/health_check.sh" << 'EOF'
#!/bin/bash
# 系统健康检查脚本

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/health_check_$(date +%Y%m%d_%H%M%S).log"
ALERT_FILE="$WORKSPACE/logs/alerts.log"

echo "=== 系统健康检查开始 $(date) ===" > "$LOG_FILE"

# 检查目录权限
echo "检查目录权限..." >> "$LOG_FILE"
for dir in "$WORKSPACE" "$WORKSPACE/logs" "$WORKSPACE/backups" "$WORKSPACE/discovered_tools"; do
    if [ -d "$dir" ]; then
        if [ ! -w "$dir" ]; then
            echo "警告: 目录不可写: $dir" >> "$LOG_FILE"
            echo "$(date) - 目录不可写: $dir" >> "$ALERT_FILE"
        fi
    else
        echo "警告: 目录不存在: $dir" >> "$LOG_FILE"
        echo "$(date) - 目录不存在: $dir" >> "$ALERT_FILE"
    fi
done

# 检查关键文件
echo "检查关键文件..." >> "$LOG_FILE"
for file in "$WORKSPACE/index.html" "$WORKSPACE/pages/tools/index.html"; do
    if [ ! -f "$file" ]; then
        echo "错误: 关键文件不存在: $file" >> "$LOG_FILE"
        echo "$(date) - 关键文件不存在: $file" >> "$ALERT_FILE"
    fi
done

# 检查磁盘空间
echo "检查磁盘空间..." >> "$LOG_FILE"
DISK_USAGE=$(df -h "$WORKSPACE" | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "警告: 磁盘使用率过高: ${DISK_USAGE}%" >> "$LOG_FILE"
    echo "$(date) - 磁盘使用率过高: ${DISK_USAGE}%" >> "$ALERT_FILE"
fi

# 检查内存使用
echo "检查内存使用..." >> "$LOG_FILE"
MEM_FREE=$(free -m | awk 'NR==2{printf "%.0f", $4*100/$2}')
if [ "$MEM_FREE" -lt 20 ]; then
    echo "警告: 可用内存不足: ${MEM_FREE}%" >> "$LOG_FILE"
    echo "$(date) - 可用内存不足: ${MEM_FREE}%" >> "$ALERT_FILE"
fi

# 检查Cron任务
echo "检查Cron任务..." >> "$LOG_FILE"
if crontab -l | grep -q "daily_discovery.sh"; then
    echo "Cron任务正常" >> "$LOG_FILE"
else
    echo "错误: Cron任务未设置" >> "$LOG_FILE"
    echo "$(date) - Cron任务未设置" >> "$ALERT_FILE"
fi

# 生成健康报告
HEALTH_STATUS="正常"
if [ -f "$ALERT_FILE" ] && [ -s "$ALERT_FILE" ]; then
    ALERT_COUNT=$(grep -c "$(date +%Y-%m-%d)" "$ALERT_FILE" 2>/dev/null || echo 0)
    if [ "$ALERT_COUNT" -gt 0 ]; then
        HEALTH_STATUS="警告($ALERT_COUNT个问题)"
    fi
fi

echo "系统健康状态: $HEALTH_STATUS" >> "$LOG_FILE"
echo "=== 系统健康检查完成 $(date) ===" >> "$LOG_FILE"

# 如果有严重问题，可以在这里添加通知机制
# 例如发送邮件或Slack通知

exit 0
EOF
    
    chmod +x "$SCRIPTS_DIR/health_check.sh"
    
    success "健康检查脚本创建完成"
}

# 生成使用说明
generate_usage_guide() {
    log "生成使用说明..."
    
    cat > "$WORKSPACE/AUTOMATION_GUIDE.md" << EOF
# AI.link.cn 自动化系统使用指南

## 系统概述
本自动化系统帮助你定期发现新的AI工具、生成内容创意、进行推广分析，实现网站内容的持续增长。

## 已设置的定时任务

### 1. 每日任务
- **时间**: 每天凌晨2:00
- **任务**: 发现新的AI工具
- **脚本**: \`scripts/daily_discovery.sh\`
- **输出**: \`logs/discovery_YYYYMMDD.log\`

### 2. 每周任务
- **时间**: 每周一早上6:00
- **任务**: 生成内容计划和创意
- **脚本**: \`scripts/weekly_content_generation.sh\`
- **输出**: \`logs/content_generation_YYYYMMDD.log\`

### 3. 每月任务
- **时间**: 每月1号早上8:00
- **任务**: 推广分析和月度报告
- **脚本**: \`scripts/monthly_promotion_analysis.sh\`
- **输出**: \`logs/promotion_analysis_YYYYMM.log\`

### 4. 备份任务
- **时间**: 每周日凌晨3:00
- **任务**: 系统备份
- **脚本**: \`scripts/backup_system.sh\`
- **输出**: \`backups/backup_TIMESTAMP.tar.gz\`

## 目录结构

\`\`\`
/root/.openclaw/workspace/
├── scripts/                    # 脚本目录
│   ├── daily_discovery.sh      # 每日发现脚本
│   ├── weekly_content_generation.sh # 每周内容生成
│   ├── monthly_promotion_analysis.sh # 每月推广分析
│   ├── backup_system.sh        # 备份脚本
│   ├── health_check.sh         # 健康检查脚本
│   └── ai_tools_discoverer.js  # AI工具发现器
├── logs/                       # 日志目录
│   ├── discovery_*.log         # 发现日志
│   ├── content_generation_*.log # 内容生成日志
│   └── cron_*.log              # Cron任务日志
├── discovered_tools/           # 发现的新工具
│   ├── new_tools_*.md          # 新工具报告
│   └── content_ideas_*.md      # 内容创意
├── backups/                    # 备份目录
│   └── backup_*.tar.gz         # 备份文件
├── reports/                    # 报告目录
│   └── monthly_report_*.md     # 月度报告
└── pages/                      # 网站页面
    └── tools/                  # 工具评测页面
\`\`\`

## 手动执行命令

### 立即运行工具发现
\`\`\`bash
cd /root/.openclaw/workspace
node scripts/ai_tools_discoverer.js
\`\`\`

### 手动生成内容计划
\`\`\`bash
cd /root/.openclaw/workspace
./scripts/weekly_content_generation.sh
\`\`\`

### 查看Cron任务状态
\`\`\`bash
crontab -l
\`\`\`

### 查看最近日志
\`\`\`bash
# 查看今日发现日志
tail -f logs/discovery_\$(date +%Y%m%d).log

# 查看所有Cron日志
tail -f logs/cron_*.log
\`\`\`

## 监控和维护

### 系统健康检查
\`\`\`bash
./scripts/health_check.sh
\`\`\`

### 手动备份系统
\`\`\`bash
./scripts/backup_system.sh
\`\`\`

### 查看警告和错误
\`\`\`bash
cat logs/alerts.log
\`\`\`

## 故障排除

### 问题1: Cron任务未执行
1. 检查Cron服务状态: \`systemctl status cron\`
2. 查看系统日志: \`grep CRON /var/log/syslog\`
3. 重新安装Cron任务: \`crontab scripts/cron-jobs\`

### 问题2: 脚本权限问题
\`\`\`bash
chmod +x scripts/*.sh
\`\`\`

### 问题3: Node.js依赖问题
\`\`\`bash
cd /root/.openclaw/workspace
npm install
\`\`\`

## 自定义配置

### 调整搜索频率
编辑 \`scripts/ai_tools_discoverer.js\` 中的 \`checkInterval\` 设置。

### 添加新的监控源
在 \`scripts/ai_tools_discoverer.js\` 的 \`CONFIG.sources\` 中添加新的网站。

### 修改内容生成模板
编辑 \`scripts/weekly_content_generation.sh\` 中的内容计划模板。

## 下一步建议

1. **立即开始**: 系统已自动运行，明天凌晨2点将执行第一次工具发现
2. **监控日志**: 定期检查日志，确保系统正常运行
3. **优化内容**: 根据生成的内容创意，开始创建评测文章
4. **推广分享**: 在社交媒体分享新发现的AI工具
5. **持续改进**: 根据实际运行情况调整和优化系统

## 联系方式
如有问题或建议，请及时反馈。

---
*系统最后更新: $(date)*
EOF
    
    success "使用说明生成完成"
}

# 主函数
main() {
    echo ""
    echo "========================================="
    echo "    AI.link.cn 自动化系统设置工具"
    echo "========================================="
    echo ""
    
    log "开始设置自动化系统..."
    
    create_directories
    install_dependencies
    create_cron_scripts
    create_health_check
    setup_cron_jobs
    generate_usage_guide
    
    echo ""
    echo "========================================="
    success "自动化系统设置完成！"
    echo ""
    echo "🎯 已设置的自动化功能："
    echo "   1. 每日AI工具发现"
    echo "   2. 每周内容生成"
    echo "   3. 每月推广分析"
    echo "   4. 定期系统备份"
    echo "   5. 系统健康监控"
    echo ""
    echo "📖 详细说明："
    echo "   查看 $WORKSPACE_DIR/AUTOMATION_GUIDE.md"
    echo ""
    echo "⏰ 下次执行时间："
    echo "   工具发现：明天凌晨2:00"
    echo "   内容生成：下周一早上6:00"
    echo ""
    echo "🚀 立即开始手动执行："
    echo "   cd $WORKSPACE_DIR"
    echo "   node scripts/ai_tools_discoverer.js"
    echo "========================================="
}

# 运行主函数
main "$@"