#!/bin/bash

# AI.link.cn 网站自动更新脚本
# 1. 处理新发现工具
# 2. 生成内容页面
# 3. 提交变更到Git
# 4. 触发部署

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/auto_update_$(date +%Y%m%d_%H%M%S).log"
NODE_PATH="/root/.nvm/versions/node/v22.22.1/bin/node"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

# 主函数
main() {
    log "===== AI.link.cn 网站自动更新开始 ====="
    
    cd "$WORKSPACE"
    
    # 1. 检查是否有新发现的工具
    log "1. 检查新发现的工具..."
    NEW_TOOLS_FILE=$(find "discovered_tools" -name "new_tools_*.md" -type f -mtime 0 2>/dev/null | head -1)
    
    if [ -n "$NEW_TOOLS_FILE" ] && [ -f "$NEW_TOOLS_FILE" ]; then
        success "发现新工具报告: $(basename $NEW_TOOLS_FILE)"
        
        # 提取工具名称
        TOOL_NAMES=$(grep "### " "$NEW_TOOLS_FILE" | sed 's/### //g' | head -5)
        
        if [ -n "$TOOL_NAMES" ]; then
            success "找到新工具: $(echo "$TOOL_NAMES" | tr '\n' ', ' | sed 's/, $//')"
            
            # 2. 为每个新工具生成内容
            log "2. 为新工具生成内容..."
            IFS=$'\n'
            for tool_line in $TOOL_NAMES; do
                tool_name=$(echo "$tool_line" | sed 's/^[0-9]*\. //g')
                log "  处理工具: $tool_name"
                
                # 简化URL查找
                tool_url=$(grep -A2 "$tool_name" "$NEW_TOOLS_FILE" | grep "URL" | head -1 | sed 's/.*: //')
                
                if [ -n "$tool_name" ]; then
                    # 生成简单的内容页面
                    generate_tool_page "$tool_name" "$tool_url"
                fi
            done
            
        else
            warn "没有提取到工具名称"
        fi
        
        # 移动已处理的文件到历史目录
        mkdir -p "discovered_tools/processed"
        mv "$NEW_TOOLS_FILE" "discovered_tools/processed/" 2>/dev/null || true
        
    else
        warn "今天没有新发现的工具"
    fi
    
    # 3. 更新时间显示（基于最新Git提交）
    log "3. 更新时间显示..."
    if [ -f "$WORKSPACE/scripts/update_time_display.sh" ]; then
        "$WORKSPACE/scripts/update_time_display.sh"
        success "时间显示已更新"
    else
        warn "时间更新脚本未找到: update_time_display.sh"
    fi
    
    # 4. 生成最新工具列表页面
    log "4. 更新工具列表页面..."
    update_tools_list_page
    
    # 5. 检查是否有变更需要提交
    log "4. 检查Git变更..."
    if git status --porcelain | grep -q "."; then
        success "检测到变更"
        
        # 添加所有变更
        git add .
        
        # 提交变更
        COMMIT_MSG="Auto-update: 添加新工具和更新页面 $(date '+%Y-%m-%d %H:%M:%S')"
        if git commit -m "$COMMIT_MSG" > /dev/null 2>&1; then
            success "提交成功: $COMMIT_MSG"
            
            # 推送到GitHub
            log "6. 推送到GitHub..."
            if git push origin main > /dev/null 2>&1; then
                success "推送成功"
                
                # 7. 触发Vercel部署
                log "7. 触发Vercel部署..."
                trigger_vercel_deploy
            else
                error "推送失败"
            fi
        else
            warn "提交失败或无变更"
        fi
    else
        warn "没有检测到变更"
    fi
    
    log "===== 网站自动更新完成 ====="
}

# 生成工具页面
generate_tool_page() {
    local tool_name="$1"
    local tool_url="$2"
    
    if [ -z "$tool_name" ]; then
        return
    fi
    
    # 创建安全的文件名
    local safe_name=$(echo "$tool_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr -cd 'a-zA-Z0-9_')
    local page_file="pages/tools/${safe_name}.html"
    
    mkdir -p "pages/tools"
    
    # 生成简单的HTML页面
    cat > "$page_file" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$tool_name - AI.link.cn</title>
    <meta name="description" content="$tool_name 评测和详细介绍。AI.link.cn提供专业的AI工具评测和推荐。">
    <meta name="keywords" content="$tool_name, AI工具, 人工智能, 工具评测">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>$tool_name</h1>
            <nav>
                <a href="/">首页</a> | 
                <a href="/pages/tools">所有工具</a> |
                <a href="/pages/about">关于我们</a>
            </nav>
        </header>
        
        <main>
            <article>
                <h2>工具介绍</h2>
                <p><strong>工具名称:</strong> $tool_name</p>
                <p><strong>官方网站:</strong> <a href="$tool_url" target="_blank">$tool_url</a></p>
                
                <h2>功能特点</h2>
                <ul>
                    <li>人工智能驱动</li>
                    <li>易于使用</li>
                    <li>功能强大</li>
                    <li>社区支持良好</li>
                </ul>
                
                <h2>使用场景</h2>
                <ul>
                    <li>内容创作</li>
                    <li>工作效率提升</li>
                    <li>学习与研究</li>
                    <li>创意设计</li>
                </ul>
                
                <h2>如何开始</h2>
                <p>访问官方网站 <a href="$tool_url" target="_blank">$tool_url</a> 注册并开始使用。</p>
                
                <h2>更新时间</h2>
                <p>本页面最后更新于: $(date '+%Y年%m月%d日 %H:%M:%S')</p>
            </article>
        </main>
        
        <footer>
            <p>&copy; 2026 AI.link.cn - 专业的AI工具评测和推荐平台</p>
        </footer>
    </div>
</body>
</html>
EOF
    
    success "   生成页面: $page_file"
}

# 更新工具列表页面
update_tools_list_page() {
    local tools_list_file="pages/tools/index.html"
    mkdir -p "pages/tools"
    
    # 获取所有工具页面
    local tool_pages=$(find "pages/tools" -name "*.html" -type f | grep -v "index.html" | sort)
    
    if [ -n "$tool_pages" ]; then
        # 生成工具列表
        local tool_count=$(echo "$tool_pages" | wc -l)
        
        cat > "$tools_list_file" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI工具列表 - AI.link.cn</title>
    <meta name="description" content="AI.link.cn收录的AI工具列表，包含详细评测和介绍。">
    <meta name="keywords" content="AI工具列表, 人工智能工具, 工具评测, AI推荐">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>AI工具列表</h1>
            <nav>
                <a href="/">首页</a> | 
                <a href="/pages/tools">所有工具</a> |
                <a href="/pages/about">关于我们</a>
            </nav>
        </header>
        
        <main>
            <h2>收录的AI工具 ($tool_count个)</h2>
            <ul class="tools-list">
EOF
        
        # 添加每个工具链接
        for tool_page in $tool_pages; do
            local tool_name=$(basename "$tool_page" .html | tr '_' ' ')
            local tool_name_display=$(echo "$tool_name" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g')
            
            echo "                <li><a href=\"/$(echo $tool_page | sed 's|^\./||')/\">$tool_name_display</a></li>" >> "$tools_list_file"
        done
        
        cat >> "$tools_list_file" << EOF
            </ul>
            
            <div class="update-info">
                <p>页面最后更新: $(date '+%Y年%m月%d日 %H:%M:%S')</p>
                <p>本页面自动更新，每日检查新工具并添加到列表中。</p>
            </div>
        </main>
        
        <footer>
            <p>&copy; 2026 AI.link.cn - 专业的AI工具评测和推荐平台</p>
        </footer>
    </div>
</body>
</html>
EOF
        
        success "   更新工具列表页面: $tools_list_file ($tool_count个工具)"
    else
        warn "   没有找到工具页面，跳过更新"
    fi
}

# 触发Vercel部署
trigger_vercel_deploy() {
    log "   触发Vercel部署..."
    
    # 尝试使用Vercel CLI
    if command -v vercel &> /dev/null; then
        if vercel deploy --preview > /dev/null 2>&1; then
            success "   Vercel预览部署已触发"
        else
            warn "   Vercel CLI执行失败"
        fi
    else
        warn "   Vercel CLI未安装，依赖GitHub Webhook自动部署"
        
        # 记录部署事件
        echo "$(date '+%Y-%m-%d %H:%M:%S') - 代码已推送，等待GitHub Webhook触发Vercel部署" \
            >> "$WORKSPACE/logs/deployment_history.log"
    fi
}

# 执行主函数
main 2>&1 | tee "$LOG_FILE"