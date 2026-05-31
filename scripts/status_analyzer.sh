#!/bin/bash
# 状态监控系统 - 状态分析脚本
# 版本: 1.0 (紧急重建版本)
# 创建时间: 2026年5月31日 04:35 AM
# 功能: 分析状态数据，生成告警和建议

set -e

# 配置参数
STATUS_DIR="/root/.openclaw/workspace/status"
ANALYSIS_DIR="/root/.openclaw/workspace/analysis"
LOG_DIR="/root/.openclaw/workspace/logs"
LATEST_STATUS="$STATUS_DIR/latest_status.json"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
ANALYSIS_FILE="$ANALYSIS_DIR/analysis_$TIMESTAMP.json"

# 创建目录
mkdir -p "$ANALYSIS_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/status_analyzer.log"
}

# 检查依赖
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        log "❌ 错误: 需要安装 jq 工具"
        log "安装命令: apt-get install -y jq"
        exit 1
    fi
    
    if ! command -v bc &> /dev/null; then
        log "❌ 错误: 需要安装 bc 工具"
        log "安装命令: apt-get install -y bc"
        exit 1
    fi
    
    log "✅ 依赖检查通过"
}

# 读取状态数据
read_status_data() {
    if [ ! -f "$LATEST_STATUS" ]; then
        log "❌ 错误: 未找到最新的状态文件: $LATEST_STATUS"
        log "请先运行 status_collector.sh"
        exit 1
    fi
    
    # 验证JSON格式
    if ! jq empty "$LATEST_STATUS" 2>/dev/null; then
        log "❌ 错误: 状态文件格式无效"
        exit 1
    fi
    
    log "✅ 加载状态数据: $LATEST_STATUS"
    cat "$LATEST_STATUS"
}

# 分析网站状态
analyze_website() {
    local website_data="$1"
    local alerts=()
    local warnings=()
    local suggestions=()
    
    local status=$(echo "$website_data" | jq -r '.status')
    local http_code=$(echo "$website_data" | jq -r '.http_code')
    local response_time=$(echo "$website_data" | jq -r '.response_time')
    local title_check=$(echo "$website_data" | jq -r '.title_check')
    
    if [ "$status" != "healthy" ]; then
        alerts+=("网站服务异常: HTTP状态 $http_code")
    fi
    
    if [ "$(echo "$response_time > 3" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
        warnings+=("网站响应时间较慢: ${response_time}秒 (建议优化)")
    fi
    
    if [ "$title_check" = "different" ]; then
        warnings+=("网站标题与预期不同，请检查配置")
    elif [ "$title_check" = "unknown" ]; then
        warnings+=("无法获取网站标题，可能存在访问问题")
    fi
    
    if [ "$status" = "healthy" ] && [ "$(echo "$response_time < 1" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
        suggestions+=("网站性能优秀，响应时间${response_time}秒")
    fi
    
    echo "website_alerts=$(printf '%s\n' "${alerts[@]}" | jq -R . | jq -s .)"
    echo "website_warnings=$(printf '%s\n' "${warnings[@]}" | jq -R . | jq -s .)"
    echo "website_suggestions=$(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .)"
    echo "website_status=$status"
}

# 分析自动化系统
analyze_automation() {
    local automation_data="$1"
    local alerts=()
    local warnings=()
    local suggestions=()
    
    local status=$(echo "$automation_data" | jq -r '.status')
    local log_age=$(echo "$automation_data" | jq -r '.log_age_seconds')
    
    if [ "$status" = "critical" ]; then
        alerts+=("自动化系统严重异常: 超过24小时未运行")
    elif [ "$status" = "warning" ]; then
        warnings+=("自动化系统有警告，请检查日志")
    elif [ "$status" = "unknown" ]; then
        warnings+=("自动化系统状态未知")
    fi
    
    if [ "$log_age" -gt 43200 ]; then  # 12小时
        warnings+=("自动化系统超过12小时未更新日志")
    fi
    
    if [ "$status" = "healthy" ] && [ "$log_age" -lt 3600 ]; then
        suggestions+=("自动化系统运行正常，最近1小时内已执行")
    fi
    
    echo "automation_alerts=$(printf '%s\n' "${alerts[@]}" | jq -R . | jq -s .)"
    echo "automation_warnings=$(printf '%s\n' "${warnings[@]}" | jq -R . | jq -s .)"
    echo "automation_suggestions=$(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .)"
    echo "automation_status=$status"
}

# 分析社交媒体状态
analyze_social_media() {
    local social_data="$1"
    local alerts=()
    local warnings=()
    local suggestions=()
    
    local twitter=$(echo "$social_data" | jq -r '.twitter')
    local linkedin=$(echo "$social_data" | jq -r '.linkedin')
    local zhihu=$(echo "$social_data" | jq -r '.zhihu')
    
    if [ "$twitter" = "not_configured" ]; then
        warnings+=("Twitter账号未配置")
    fi
    
    if [ "$linkedin" = "very_stale" ] || [ "$zhihu" = "very_stale" ]; then
        alerts+=("社交媒体任务严重延迟: 超过24小时未处理")
    elif [ "$linkedin" = "stale" ] || [ "$zhihu" = "stale" ]; then
        warnings+=("社交媒体任务延迟: 超过1小时未处理")
    elif [ "$linkedin" = "not_started" ] || [ "$zhihu" = "not_started" ]; then
        alerts+=("社交媒体任务尚未开始")
    fi
    
    if [ "$twitter" = "configured" ] && [ "$linkedin" = "pending" ] && [ "$zhihu" = "pending" ]; then
        suggestions+=("社交媒体矩阵已规划，等待执行")
    fi
    
    echo "social_alerts=$(printf '%s\n' "${alerts[@]}" | jq -R . | jq -s .)"
    echo "social_warnings=$(printf '%s\n' "${warnings[@]}" | jq -R . | jq -s .)"
    echo "social_suggestions=$(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .)"
    
    # 计算社交媒体状态
    local social_status="healthy"
    if [ ${#alerts[@]} -gt 0 ]; then
        social_status="critical"
    elif [ ${#warnings[@]} -gt 0 ]; then
        social_status="warning"
    fi
    echo "social_status=$social_status"
}

# 分析评测工作状态
analyze_reviews() {
    local reviews_data="$1"
    local alerts=()
    local warnings=()
    local suggestions=()
    
    local grammarly_lines=$(echo "$reviews_data" | jq -r '.grammarly.lines')
    local grammarly_progress=$(echo "$reviews_data" | jq -r '.grammarly.progress')
    local grammarly_status=$(echo "$reviews_data" | jq -r '.grammarly.status')
    local grammarly_age=$(echo "$reviews_data" | jq -r '.grammarly.age_seconds')
    
    local chatgpt_lines=$(echo "$reviews_data" | jq -r '.chatgpt.lines')
    local chatgpt_progress=$(echo "$reviews_data" | jq -r '.chatgpt.progress')
    local chatgpt_status=$(echo "$reviews_data" | jq -r '.chatgpt.status')
    local chatgpt_age=$(echo "$reviews_data" | jq -r '.chatgpt.age_seconds')
    
    # Grammarly评测分析
    if [ "$grammarly_status" = "very_stale" ]; then
        alerts+=("Grammarly评测严重停滞: 超过48小时无进展 (当前进度: ${grammarly_progress}%)")
    elif [ "$grammarly_status" = "stale" ]; then
        warnings+=("Grammarly评测停滞: 超过24小时无进展 (当前进度: ${grammarly_progress}%)")
    fi
    
    if [ "$(echo "$grammarly_progress < 50" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
        warnings+=("Grammarly评测进度较低: ${grammarly_progress}% (目标100%)")
    fi
    
    if [ "$(echo "$grammarly_progress > 90" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
        suggestions+=("Grammarly评测接近完成: ${grammarly_progress}%，建议今日完成")
    fi
    
    # ChatGPT评测分析
    if [ "$chatgpt_status" = "very_stale" ]; then
        alerts+=("ChatGPT评测严重停滞: 超过48小时无进展 (当前进度: ${chatgpt_progress}%)")
    elif [ "$chatgpt_status" = "stale" ]; then
        warnings+=("ChatGPT评测停滞: 超过24小时无进展 (当前进度: ${chatgpt_progress}%)")
    fi
    
    if [ "$(echo "$chatgpt_progress < 50" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
        warnings+=("ChatGPT评测进度较低: ${chatgpt_progress}% (目标80%)")
    fi
    
    if [ "$(echo "$chatgpt_progress > 70" | bc 2>/dev/null || echo 0)" -eq 1 ]; then
        suggestions+=("ChatGPT评测进展良好: ${chatgpt_progress}%，接近目标")
    fi
    
    # 综合建议
    if [ "$grammarly_status" = "recent" ] && [ "$chatgpt_status" = "recent" ]; then
        suggestions+=("评测工作正常进行中，保持当前节奏")
    fi
    
    echo "review_alerts=$(printf '%s\n' "${alerts[@]}" | jq -R . | jq -s .)"
    echo "review_warnings=$(printf '%s\n' "${warnings[@]}" | jq -R . | jq -s .)"
    echo "review_suggestions=$(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .)"
    
    # 计算评测状态
    local review_status="healthy"
    if [ ${#alerts[@]} -gt 0 ]; then
        review_status="critical"
    elif [ ${#warnings[@]} -gt 0 ]; then
        review_status="warning"
    fi
    echo "review_status=$review_status"
}

# 分析系统资源状态
analyze_system() {
    local system_data="$1"
    local alerts=()
    local warnings=()
    local suggestions=()
    
    local disk_usage=$(echo "$system_data" | jq -r '.disk_usage')
    local memory_usage=$(echo "$system_data" | jq -r '.memory_usage')
    local disk_status=$(echo "$system_data" | jq -r '.disk_status')
    local memory_status=$(echo "$system_data" | jq -r '.memory_status')
    
    if [ "$disk_status" = "critical" ]; then
        alerts+=("磁盘空间严重不足: ${disk_usage}% (建议立即清理)")
    elif [ "$disk_status" = "warning" ]; then
        warnings+=("磁盘空间紧张: ${disk_usage}% (建议关注)")
    fi
    
    if [ "$memory_status" = "critical" ]; then
        alerts+=("内存使用率过高: ${memory_usage}% (可能影响性能)")
    elif [ "$memory_status" = "warning" ]; then
        warnings+=("内存使用率较高: ${memory_usage}% (建议监控)")
    fi
    
    if [ "$disk_status" = "healthy" ] && [ "$memory_status" = "healthy" ]; then
        suggestions+=("系统资源充足: 磁盘${disk_usage}%，内存${memory_usage}%")
    fi
    
    echo "system_alerts=$(printf '%s\n' "${alerts[@]}" | jq -R . | jq -s .)"
    echo "system_warnings=$(printf '%s\n' "${warnings[@]}" | jq -R . | jq -s .)"
    echo "system_suggestions=$(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .)"
    
    # 计算系统状态
    local system_status="healthy"
    if [ ${#alerts[@]} -gt 0 ]; then
        system_status="critical"
    elif [ ${#warnings[@]} -gt 0 ]; then
        system_status="warning"
    fi
    echo "system_status=$system_status"
}

# 生成总体分析
generate_overall_analysis() {
    local website_status="$1"
    local automation_status="$2"
    local social_status="$3"
    local review_status="$4"
    local system_status="$5"
    
    local total_alerts=0
    local total_warnings=0
    
    # 统计各组件告警和警告数量
    for status_var in "website_alerts" "automation_alerts" "social_alerts" "review_alerts" "system_alerts"; do
        local count=$(eval "echo \${#${status_var}[@]}" 2>/dev/null || echo 0)
        total_alerts=$((total_alerts + count))
    done
    
    for status_var in "website_warnings" "automation_warnings" "social_warnings" "review_warnings" "system_warnings"; do
        local count=$(eval "echo \${#${status_var}[@]}" 2>/dev/null || echo 0)
        total_warnings=$((total_warnings + count))
    done
    
    # 确定整体状态
    local overall_status="healthy"
    if [ $total_alerts -gt 0 ]; then
        overall_status="critical"
    elif [ $total_warnings -gt 0 ]; then
        overall_status="warning"
    fi
    
    # 生成状态摘要
    local status_summary=""
    if [ "$overall_status" = "critical" ]; then
        status_summary="🚨 系统有 $total_alerts 个紧急问题需要立即处理"
    elif [ "$overall_status" = "warning" ]; then
        status_summary="⚠️  系统有 $total_warnings 个需要注意的问题"
    else
        status_summary="✅ 所有系统运行正常"
    fi
    
    echo "overall_status=$overall_status"
    echo "total_alerts=$total_alerts"
    echo "total_warnings=$total_warnings"
    echo "status_summary=\"$status_summary\""
}

# 更新HEARTBEAT.md状态
update_heartbeat_status() {
    local analysis_data="$1"
    
    # 从分析数据中提取信息
    local overall_status=$(echo "$analysis_data" | jq -r '.overall_status')
    local status_summary=$(echo "$analysis_data" | jq -r '.status_summary')
    local total_alerts=$(echo "$analysis_data" | jq -r '.total_alerts')
    local total_warnings=$(echo "$analysis_data" | jq -r '.total_warnings')
    
    # 生成状态更新内容
    local update_time=$(date +"%Y-%m-%d %H:%M:%S")
    local heartbeat_update="\n### 📊 实时状态监控 (更新于: $update_time)\n"
    heartbeat_update+="- **整体状态**: $status_summary\n"
    
    if [ $total_alerts -gt 0 ]; then
        local alerts=$(echo "$analysis_data" | jq -r '.alerts | join(", ")')
        heartbeat_update+="- **紧急告警 ($total_alerts个)**: $alerts\n"
    fi
    
    if [ $total_warnings -gt 0 ]; then
        local warnings=$(echo "$analysis_data" | jq -r '.warnings | join(", ")')
        heartbeat_update+="- **警告 ($total_warnings个)**: $warnings\n"
    fi
    
    local suggestions=$(echo "$analysis_data" | jq -r '.suggestions | join(", ")')
    if [ -n "$suggestions" ] && [ "$suggestions" != "null" ]; then
        heartbeat_update+="- **建议**: $suggestions\n"
    fi
    
    heartbeat_update+="- **详细报告**: 查看最新分析报告: $ANALYSIS_FILE\n"
    
    # 记录到日志
    log "📝 生成HEARTBEAT.md更新: $status_summary"
    
    # 这里可以添加实际更新HEARTBEAT.md的代码
    # 注意: 由于时间限制，先输出到日志，后续可以集成
    echo "$heartbeat_update" >> "$LOG_DIR/heartbeat_updates.log"
    
    echo "heartbeat_update_generated=true"
}

# 主分析函数
analyze_all() {
    log "🧠 开始分析系统状态..."
    
    # 检查依赖
    check_dependencies
    
    # 读取状态数据
    local status_data=$(read_status_data)
    
    # 提取各组件数据
    local website_data=$(echo "$status_data" | jq -r '.[0]')
    local automation_data=$(echo "$status_data" | jq -r '.[1]')
    local social_data=$(echo "$status_data" | jq -r '.[2]')
    local review_data=$(echo "$status_data" | jq -r '.[3]')
    local system_data=$(echo "$status_data" | jq -r '.[4]')
    
    # 分析各组件
    log "📊 分析网站服务状态..."
    eval "$(analyze_website "$website_data")"
    
    log "📊 分析自动化系统状态..."
    eval "$(analyze_automation "$automation_data")"
    
    log "📊 分析社交媒体状态..."
    eval "$(analyze_social_media "$social_data")"
    
    log "📊 分析评测工作状态..."
    eval "$(analyze_reviews "$review_data")"
    
    log "📊 分析系统资源状态..."
    eval "$(analyze_system "$system_data")"
    
    # 生成总体分析
    log "📈 生成总体分析..."
    eval "$(generate_overall_analysis "$website_status" "$automation_status" "$social_status" "$review_status" "$system_status")"
    
    # 合并所有告警、警告和建议
    local all_alerts=("${website_alerts[@]}" "${automation_alerts[@]}" "${social_alerts[@]}" "${review_alerts[@]}" "${system_alerts[@]}")
    local all_warnings=("${website_warnings[@]}" "${automation_warnings[@]}" "${social_warnings[@]}" "${review_warnings[@]}" "${system_warnings[@]}")
    local all_suggestions=("${website_suggestions[@]}" "${automation_suggestions[@]}" "${social_suggestions[@]}" "${review_suggestions[@]}" "${system_suggestions[@]}")
    
    # 生成分析结果
    local analysis_result=$(cat << EOF
{
    "timestamp": "$(date -Iseconds)",
    "analysis_id": "$TIMESTAMP",
    "overall_status": "$overall_status",
    "status_summary": "$status_summary",
    "total_alerts": $total_alerts,
    "total_warnings": $total_warnings,
    "total_suggestions": ${#all_suggestions[@]},
    "component_statuses": {
        "website": "$website_status",
        "automation": "$automation_status",
        "social_media": "$social_status",
        "reviews": "$review_status",
        "system": "$system_status"
    },
    "alerts": $(printf '%s\n' "${all_alerts[@]}" | jq -R . | jq -s .),
    "warnings": $(printf '%s\n' "${all_warnings[@]}" | jq -R . | jq -s .),
    "suggestions": $(printf '%s\n' "${all_suggestions[@]}" | jq -R . | jq -s .),
    "data_source": "$LATEST_STATUS"
}
EOF
)
    
    # 保存分析结果
    echo "$analysis_result" > "$ANALYSIS_FILE"
    ln -sf "analysis_$TIMESTAMP.json" "$ANALYSIS_DIR/latest_analysis.json"
    
    # 更新HEARTBEAT.md状态
    eval "$(update_heartbeat_status "$analysis_result")"
    
    # 输出摘要
    log "✅ 分析完成: $ANALYSIS_FILE"
    echo ""
    echo "📋 分析摘要:"
    echo "------------"
    echo "整体状态: $overall_status"
    echo "状态摘要: $status_summary"
    echo "紧急告警: $total_alerts 个"
    echo "警告: $total_warnings 个"
    echo "建议: ${#all_suggestions[@]} 条"
    echo ""
    echo "各组件状态:"
    echo "• 网站服务: $website_status"
    echo "• 自动化系统: $automation_status"
    echo "• 社交媒体: $social_status"
    echo "• 评测工作: $review_status"
    echo "• 系统资源: $system_status"
    echo ""
    echo "分析文件: $ANALYSIS_FILE"
    echo "最新链接: $ANALYSIS_DIR/latest_analysis.json"
    
    # 如果有紧急告警，特别提示
    if [ $total_alerts -gt 0 ]; then
        echo ""
        echo "🚨 紧急告警详情:"
        for alert in "${all_alerts[@]}"; do
            echo "  • $alert"
        done
    fi
}

# 执行主函数
analyze_all