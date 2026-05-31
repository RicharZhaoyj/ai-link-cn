#!/bin/bash
# 简化版状态分析脚本
# 创建时间: 2026年5月31日 04:30 AM

set -e

# 配置参数
STATUS_DIR="/root/.openclaw/workspace/status"
ANALYSIS_DIR="/root/.openclaw/workspace/analysis"
LATEST_STATUS="$STATUS_DIR/latest_status.json"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
ANALYSIS_FILE="$ANALYSIS_DIR/analysis_$TIMESTAMP.json"

# 创建目录
mkdir -p "$ANALYSIS_DIR"

# 检查状态文件
if [ ! -f "$LATEST_STATUS" ]; then
    echo "错误: 未找到状态文件 $LATEST_STATUS"
    echo "请先运行 status_collector_simple.sh"
    exit 1
fi

# 分析函数
analyze_status() {
    echo "开始分析系统状态..."
    
    # 读取JSON数据
    local status_data=$(cat "$LATEST_STATUS")
    
    # 初始化数组
    local alerts=()
    local warnings=()
    local suggestions=()
    
    # 1. 分析网站状态
    local website_status=$(echo "$status_data" | jq -r '.[0].status')
    local http_code=$(echo "$status_data" | jq -r '.[0].http_code')
    
    if [ "$website_status" != "healthy" ]; then
        alerts+=("网站服务异常: HTTP状态 $http_code")
    else
        suggestions+=("网站服务运行正常")
    fi
    
    # 2. 分析自动化系统
    local automation_status=$(echo "$status_data" | jq -r '.[1].status')
    local log_age=$(echo "$status_data" | jq -r '.[1].log_age_seconds')
    
    if [ "$automation_status" != "healthy" ]; then
        warnings+=("自动化系统状态异常: $automation_status")
    elif [ $log_age -gt 86400 ]; then
        warnings+=("自动化系统超过24小时未运行")
    else
        suggestions+=("自动化系统运行正常")
    fi
    
    # 3. 分析社交媒体
    local linkedin_status=$(echo "$status_data" | jq -r '.[2].linkedin')
    local zhihu_status=$(echo "$status_data" | jq -r '.[2].zhihu')
    
    if [ "$linkedin_status" = "stale" ] || [ "$zhihu_status" = "stale" ]; then
        alerts+=("社交媒体任务严重延迟: LinkedIn($linkedin_status), 知乎($zhihu_status)")
    elif [ "$linkedin_status" = "not_started" ] || [ "$zhihu_status" = "not_started" ]; then
        alerts+=("社交媒体任务尚未开始")
    else
        warnings+=("社交媒体任务需要关注: LinkedIn($linkedin_status), 知乎($zhihu_status)")
    fi
    
    # 4. 分析评测工作
    local grammarly_progress=$(echo "$status_data" | jq -r '.[3].grammarly.progress')
    local chatgpt_progress=$(echo "$status_data" | jq -r '.[3].chatgpt.progress')
    
    if [ $grammarly_progress -lt 50 ]; then
        warnings+=("Grammarly评测进度较低: ${grammarly_progress}% (目标100%)")
    elif [ $grammarly_progress -lt 80 ]; then
        warnings+=("Grammarly评测需要加速: ${grammarly_progress}% (目标100%)")
    else
        suggestions+=("Grammarly评测进展良好: ${grammarly_progress}%")
    fi
    
    if [ $chatgpt_progress -lt 50 ]; then
        warnings+=("ChatGPT评测进度较低: ${chatgpt_progress}% (目标80%)")
    elif [ $chatgpt_progress -lt 70 ]; then
        warnings+=("ChatGPT评测需要推进: ${chatgpt_progress}% (目标80%)")
    else
        suggestions+=("ChatGPT评测进展良好: ${chatgpt_progress}%")
    fi
    
    # 5. 分析系统资源
    local disk_usage=$(echo "$status_data" | jq -r '.[4].disk_usage')
    local memory_usage=$(echo "$status_data" | jq -r '.[4].memory_usage')
    
    if [ $disk_usage -gt 80 ]; then
        warnings+=("磁盘使用率较高: ${disk_usage}%")
    elif [ $disk_usage -gt 90 ]; then
        alerts+=("磁盘空间严重不足: ${disk_usage}%")
    else
        suggestions+=("磁盘空间充足: ${disk_usage}%")
    fi
    
    if [ $memory_usage -gt 80 ]; then
        warnings+=("内存使用率较高: ${memory_usage}%")
    elif [ $memory_usage -gt 90 ]; then
        alerts+=("内存使用率过高: ${memory_usage}%")
    else
        suggestions+=("内存使用正常: ${memory_usage}%")
    fi
    
    # 计算总体状态
    local overall_status="healthy"
    if [ ${#alerts[@]} -gt 0 ]; then
        overall_status="critical"
    elif [ ${#warnings[@]} -gt 0 ]; then
        overall_status="warning"
    fi
    
    # 生成状态摘要
    local status_summary=""
    if [ "$overall_status" = "critical" ]; then
        status_summary="🚨 有 ${#alerts[@]} 个紧急问题需要立即处理"
    elif [ "$overall_status" = "warning" ]; then
        status_summary="⚠️  有 ${#warnings[@]} 个需要注意的问题"
    else
        status_summary="✅ 所有系统运行正常"
    fi
    
    # 生成分析结果
    local analysis_result=$(cat << EOF
{
    "timestamp": "$(date -Iseconds)",
    "analysis_id": "$TIMESTAMP",
    "overall_status": "$overall_status",
    "status_summary": "$status_summary",
    "total_alerts": ${#alerts[@]},
    "total_warnings": ${#warnings[@]},
    "total_suggestions": ${#suggestions[@]},
    "alerts": $(printf '%s\n' "${alerts[@]}" | jq -R . | jq -s .),
    "warnings": $(printf '%s\n' "${warnings[@]}" | jq -R . | jq -s .),
    "suggestions": $(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .),
    "data_source": "$LATEST_STATUS"
}
EOF
)
    
    # 保存分析结果
    echo "$analysis_result" > "$ANALYSIS_FILE"
    ln -sf "analysis_$TIMESTAMP.json" "$ANALYSIS_DIR/latest_analysis.json"
    
    # 更新HEARTBEAT.md状态
    update_heartbeat_status "$analysis_result"
    
    # 输出结果
    echo "分析完成: $ANALYSIS_FILE"
    echo ""
    echo "📋 系统状态分析报告:"
    echo "===================="
    echo "整体状态: $overall_status"
    echo "状态摘要: $status_summary"
    echo ""
    
    if [ ${#alerts[@]} -gt 0 ]; then
        echo "🚨 紧急告警 (${#alerts[@]}个):"
        for alert in "${alerts[@]}"; do
            echo "  • $alert"
        done
        echo ""
    fi
    
    if [ ${#warnings[@]} -gt 0 ]; then
        echo "⚠️  警告 (${#warnings[@]}个):"
        for warning in "${warnings[@]}"; do
            echo "  • $warning"
        done
        echo ""
    fi
    
    if [ ${#suggestions[@]} -gt 0 ]; then
        echo "💡 建议 (${#suggestions[@]}条):"
        for suggestion in "${suggestions[@]}"; do
            echo "  • $suggestion"
        done
        echo ""
    fi
    
    echo "各组件详细状态:"
    echo "1. 网站服务: $website_status (HTTP $http_code)"
    echo "2. 自动化系统: $automation_status (日志年龄: ${log_age}秒)"
    echo "3. 社交媒体: LinkedIn($linkedin_status), 知乎($zhihu_status)"
    echo "4. 评测工作: Grammarly(${grammarly_progress}%), ChatGPT(${chatgpt_progress}%)"
    echo "5. 系统资源: 磁盘(${disk_usage}%), 内存(${memory_usage}%)"
    echo ""
    echo "分析文件: $ANALYSIS_FILE"
    echo "下次检查建议: 30分钟内"
    
    # 如果有紧急告警，添加特别提醒
    if [ ${#alerts[@]} -gt 0 ]; then
        echo ""
        echo "⏰ 紧急提醒: 请立即处理上述告警问题！"
    fi
}

# 执行分析
analyze_status