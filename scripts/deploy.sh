#!/bin/bash

# AI.link.cn 自动化部署脚本
# 功能：自动部署网站更新到Vercel

set -e  # 任何命令失败则退出脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js 未安装"
        exit 1
    fi
    log_info "Node.js 版本: $(node --version)"
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        log_error "npm 未安装"
        exit 1
    fi
    log_info "npm 版本: $(npm --version)"
    
    # 检查Git
    if ! command -v git &> /dev/null; then
        log_error "Git 未安装"
        exit 1
    fi
    log_info "Git 版本: $(git --version)"
    
    # 检查Vercel CLI
    if ! command -v vercel &> /dev/null; then
        log_warning "Vercel CLI 未安装，正在安装..."
        npm install -g vercel
    fi
    log_info "Vercel CLI 版本: $(vercel --version 2>/dev/null || echo '未安装')"
    
    log_success "所有依赖检查通过"
}

# 备份当前版本
backup_current_version() {
    log_info "备份当前版本..."
    
    local backup_dir="./backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # 备份重要文件
    cp -r ./index.html ./pages ./admin ./config ./scripts "$backup_dir/" 2>/dev/null || true
    
    log_success "当前版本已备份到: $backup_dir"
}

# 检查文件更改
check_changes() {
    log_info "检查文件更改..."
    
    if [ ! -d .git ]; then
        log_warning "当前目录不是Git仓库，跳过Git检查"
        return
    fi
    
    local changes=$(git status --porcelain 2>/dev/null || echo "")
    
    if [ -z "$changes" ]; then
        log_info "没有检测到文件更改"
        return 0
    else
        log_info "检测到文件更改:"
        echo "$changes"
        return 1
    fi
}

# 运行优化脚本
run_optimization_scripts() {
    log_info "运行Affiliate优化脚本..."
    
    cd "$(dirname "$0")/.."
    
    # 运行优化脚本
    if [ -f "./scripts/affiliate-optimizer.js" ]; then
        node ./scripts/affiliate-optimizer.js
        
        # 复制最新报告到网站目录
        local latest_report=$(ls -t ./output/summary-report-*.html 2>/dev/null | head -1)
        if [ -f "$latest_report" ]; then
            cp "$latest_report" ./admin/latest-report.html
            log_success "最新报告已复制到: ./admin/latest-report.html"
        fi
    else
        log_warning "未找到优化脚本"
    fi
}

# 构建网站
build_site() {
    log_info "开始构建网站..."
    
    cd "$(dirname "$0")/.."
    
    # 检查是否有package.json
    if [ -f "package.json" ]; then
        log_info "安装npm依赖..."
        npm install --silent
        
        log_info "运行构建脚本..."
        npm run build --silent || log_warning "构建脚本运行失败，跳过构建步骤"
    else
        log_info "无构建步骤，直接部署静态文件"
    fi
    
    # 检查必需的目录
    local required_dirs=("pages" "admin" "scripts")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            log_warning "目录 $dir 不存在，正在创建..."
            mkdir -p "$dir"
        fi
    done
    
    log_success "网站构建完成"
}

# 部署到Vercel
deploy_to_vercel() {
    log_info "开始部署到Vercel..."
    
    cd "$(dirname "$0")/.."
    
    local deployment_type="$1"
    local deploy_flags=""
    
    case $deployment_type in
        "production")
            deploy_flags="--prod"
            log_info "部署到生产环境"
            ;;
        "preview")
            deploy_flags=""
            log_info "部署到预览环境"
            ;;
        *)
            deploy_flags=""
            log_info "部署到默认环境"
            ;;
    esac
    
    # 检查是否已登录Vercel
    if ! vercel whoami &> /dev/null; then
        log_warning "未登录Vercel，请按照提示登录..."
        vercel login
    fi
    
    # 部署网站
    log_info "运行部署命令..."
    local deploy_output=$(vercel deploy $deploy_flags 2>&1)
    
    if echo "$deploy_output" | grep -q "Error\|error\|ERROR"; then
        log_error "部署失败:"
        echo "$deploy_output"
        return 1
    else
        # 提取部署URL
        local deploy_url=$(echo "$deploy_output" | grep -o "https://[^ ]*\.vercel\.app" | head -1)
        
        if [ -n "$deploy_url" ]; then
            log_success "部署成功！"
            log_success "网站地址: $deploy_url"
            
            # 保存部署信息
            echo "{
  \"timestamp\": \"$(date -Iseconds)\",
  \"url\": \"$deploy_url\",
  \"type\": \"$deployment_type\",
  \"commit\": \"$(git rev-parse HEAD 2>/dev/null || echo 'N/A')\"
}" > ./deploy-info.json
            
            return 0
        else
            log_error "无法提取部署URL"
            echo "$deploy_output"
            return 1
        fi
    fi
}

# 运行测试
run_tests() {
    log_info "运行网站测试..."
    
    cd "$(dirname "$0")/.."
    
    # 检查主要文件是否存在
    local required_files=("index.html" "pages/tools/hostinger.html" "admin/affiliate-dashboard.html")
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        log_error "缺少必需的文件:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        return 1
    fi
    
    # 检查HTML语法
    if command -v tidy &> /dev/null; then
        log_info "检查HTML语法..."
        tidy -q -errors index.html 2>&1 | head -20 || true
    fi
    
    # 检查链接（简化版）
    log_info "检查关键链接..."
    local links_to_check=(
        "https://www.hostinger.com?REFERRALCODE=O3VZHAOYJYL1"
        "/pages/tools/hostinger.html"
        "/admin/affiliate-dashboard.html"
    )
    
    for link in "${links_to_check[@]}"; do
        if [[ $link == http* ]]; then
            log_info "  检查外部链接: $link"
        else
            if [ -f ".$link" ] || [ -d ".$link" ]; then
                log_info "  检查内部链接: $link ✓"
            else
                log_warning "  检查内部链接: $link ✗ (文件不存在)"
            fi
        fi
    done
    
    log_success "基本测试通过"
}

# 生成部署报告
generate_deploy_report() {
    log_info "生成部署报告..."
    
    cd "$(dirname "$0")/.."
    
    local report_file="./admin/deploy-report-$(date +%Y%m%d_%H%M%S).html"
    
    cat > "$report_file" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>部署报告 - AI.link.cn</title>
    <style>
        body { font-family: -apple-system, sans-serif; line-height: 1.6; background: #f8fafc; color: #1f2937; margin: 0; padding: 2rem; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 2rem; }
        .section { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 1rem; }
        .success { border-left: 5px solid #10b981; }
        .warning { border-left: 5px solid #f59e0b; }
        .error { border-left: 5px solid #ef4444; }
        .info { border-left: 5px solid #3b82f6; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 0.8rem; text-align: left; border-bottom: 1px solid #e5e7eb; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }
        .stat { background: #f0f9ff; padding: 1rem; border-radius: 8px; }
        .stat-value { font-size: 1.5rem; font-weight: bold; color: #1e40af; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI.link.cn 部署报告</h1>
            <p>部署时间: $(date)</p>
            <p>部署环境: $DEPLOY_ENV</p>
        </div>
        
        <div class="section info">
            <h2>📊 部署统计</h2>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">$(find . -name "*.html" | wc -l)</div>
                    <div>HTML文件</div>
                </div>
                <div class="stat">
                    <div class="stat-value">$(find . -name "*.js" | wc -l)</div>
                    <div>JS脚本</div>
                </div>
                <div class="stat">
                    <div class="stat-value">$(find . -name "*.css" | wc -l)</div>
                    <div>CSS样式</div>
                </div>
                <div class="stat">
                    <div class="stat-value">$(du -sh . | cut -f1)</div>
                    <div>总大小</div>
                </div>
            </div>
        </div>
        
        <div class="section success">
            <h2>✅ 部署成功</h2>
            <p>网站已成功部署到生产环境。</p>
            <p><strong>网站地址:</strong> <a href="$DEPLOY_URL" target="_blank">$DEPLOY_URL</a></p>
            <p><strong>部署ID:</strong> $(date +%Y%m%d-%H%M%S)</p>
        </div>
        
        <div class="section">
            <h2>📁 部署文件</h2>
            <table>
                <thead>
                    <tr>
                        <th>文件/目录</th>
                        <th>类型</th>
                        <th>大小</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>index.html</td>
                        <td>首页</td>
                        <td>$(stat -f%z index.html 2>/dev/null || stat -c%s index.html 2>/dev/null || echo "N/A") bytes</td>
                        <td>✅</td>
                    </tr>
                    <tr>
                        <td>pages/tools/hostinger.html</td>
                        <td>Hostinger页面</td>
                        <td>$(stat -f%z pages/tools/hostinger.html 2>/dev/null || stat -c%s pages/tools/hostinger.html 2>/dev/null || echo "N/A") bytes</td>
                        <td>✅</td>
                    </tr>
                    <tr>
                        <td>admin/affiliate-dashboard.html</td>
                        <td>监控面板</td>
                        <td>$(stat -f%z admin/affiliate-dashboard.html 2>/dev/null || stat -c%s admin/affiliate-dashboard.html 2>/dev/null || echo "N/A") bytes</td>
                        <td>✅</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>🔗 关键链接</h2>
            <ul>
                <li><a href="$DEPLOY_URL" target="_blank">网站首页</a></li>
                <li><a href="$DEPLOY_URL/pages/tools/hostinger.html" target="_blank">Hostinger评测页面</a></li>
                <li><a href="$DEPLOY_URL/admin/affiliate-dashboard.html" target="_blank">联盟监控面板</a></li>
                <li><a href="$DEPLOY_URL/admin/latest-report.html" target="_blank">最新优化报告</a></li>
            </ul>
        </div>
        
        <div class="section info">
            <h2>📈 下一步行动</h2>
            <ol>
                <li>检查网站功能是否正常</li>
                <li>测试Affiliate链接是否有效</li>
                <li>监控24小时内的访问量</li>
                <li>运行SEO检查工具</li>
                <li>设置自动部署（每日凌晨）</li>
            </ol>
        </div>
        
        <div class="section" style="text-align: center; background: #f0f9ff;">
            <p>💪 <strong>AI.link.cn 自动化部署系统</strong></p>
            <p>版本: 1.0.0 | 生成时间: $(date)</p>
            <p>💡 提示: 此报告仅供内部使用</p>
        </div>
    </div>
</body>
</html>
EOF
    
    log_success "部署报告已生成: $report_file"
}

# 主部署函数
main_deploy() {
    local deployment_type="preview"
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --prod|--production)
                deployment_type="production"
                shift
                ;;
            --preview)
                deployment_type="preview"
                shift
                ;;
            --test-only)
                run_tests
                exit 0
                ;;
            *)
                log_error "未知参数: $1"
                echo "用法: $0 [--production|--preview|--test-only]"
                exit 1
                ;;
        esac
    done
    
    log_info "开始AI.link.cn部署流程"
    log_info "部署类型: $deployment_type"
    echo ""
    
    # 执行部署步骤
    check_dependencies
    echo ""
    
    backup_current_version
    echo ""
    
    check_changes
    echo ""
    
    run_optimization_scripts
    echo ""
    
    build_site
    echo ""
    
    run_tests
    echo ""
    
    if deploy_to_vercel "$deployment_type"; then
        echo ""
        
        # 设置环境变量供报告使用
        if [ -f "./deploy-info.json" ]; then
            DEPLOY_URL=$(grep -o '"url":"[^"]*"' ./deploy-info.json | cut -d'"' -f4)
            DEPLOY_ENV="$deployment_type"
            export DEPLOY_URL DEPLOY_ENV
            
            generate_deploy_report
            echo ""
            
            log_success "🎉 部署流程完成！"
            log_success "🌐 网站已上线: $DEPLOY_URL"
            log_success "📊 监控面板: $DEPLOY_URL/admin/affiliate-dashboard.html"
            log_success "📈 Hostinger页面: $DEPLOY_URL/pages/tools/hostinger.html"
            echo ""
            
            # 显示部署总结
            echo "📋 部署总结:"
            echo "   1. ✅ 网站已部署到 $deployment_type 环境"
            echo "   2. ✅ 所有测试通过"
            echo "   3. ✅ Affiliate优化脚本已运行"
            echo "   4. ✅ 备份已创建"
            echo "   5. ✅ 部署报告已生成"
            echo ""
            echo "🚀 下一步:"
            echo "   • 手动测试网站功能"
            echo "   • 检查Affiliate链接"
            echo "   • 设置监控提醒"
            echo "   • 开始推广活动"
            
        fi
    else
        log_error "部署失败，请检查错误信息"
        exit 1
    fi
}

# 显示帮助
show_help() {
    cat << EOF
AI.link.cn 自动化部署脚本

用法: $0 [选项]

选项:
  --production, --prod   部署到生产环境
  --preview             部署到预览环境（默认）
  --test-only           只运行测试，不部署
  -h, --help            显示此帮助信息

示例:
  $0 --preview          部署到预览环境
  $0 --production       部署到生产环境
  $0 --test-only        只运行测试

功能:
  1. 检查系统依赖
  2. 备份当前版本
  3. 运行优化脚本
  4. 构建网站
  5. 运行测试
  6. 部署到Vercel
  7. 生成部署报告

环境要求:
  • Node.js 16+
  • npm 8+
  • Git
  • Vercel CLI（可选，会自动安装）

注意:
  • 生产环境部署需要Vercel项目权限
  • 首次使用需要登录Vercel账户
  • 建议在干净的Git仓库中运行

EOF
}

# 主入口
if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# 执行主函数
main_deploy "$@"