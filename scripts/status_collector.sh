#!/bin/bash
# 状态监控系统 - 状态收集脚本
# 版本: 1.0 (紧急重建版本)
# 创建时间: 2026年5月31日 04:30 AM
# 功能: 收集AI.link.cn所有关键组件的状态信息

set -e

# 配置参数
STATUS_DIR="/root/.openclaw/workspace/status"
LOG_DIR="/root/.openclaw/workspace/logs"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
STATUS_FILE="$STATUS_DIR/status_$TIMESTAMP.json"

# 创建状态目录
mkdir -p "$STATUS_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/status_monitor.log"
}

# 错误处理函数
handle_error() {
    local component="$1"
    local error_msg="$2"
    log "❌ $component 状态收集失败: $error_msg"
    echo '{"component":"'$component'","status":"error","error":"'$error_msg'","timestamp":"'$(date -Iseconds)'"}'
}

# 1. 收集网站服务状态
collect_website_status() {
    log "🔍 收集网站服务状态..."
    local url="https://ai.link.cn"
    
    # 检查HTTP状态码
    local start_time=$(date +%s.%N)
    local http_code=$(curl -s -o /dev/null -w "%{http_code}" -I "$url" --connect-timeout 10 --max-time 15 2>/dev/null || echo "000")
    local end_time=$(date +%s.%N)
    local response_time=$(echo "$end_time - $start_time" | bc 2>/dev/null | awk '{printf "%.3f", $1}' || echo "0.000")
    
    if [ "$http_code" = "200" ]; then
        # 获取网站标题
        local title=$(curl -s "$url" --max-time 10 2>/dev/null | grep -o '<title>[^<]*</title>' | sed 's/<title>//;s/<\/title>//' || echo "无法获取标题")
        
        # 检查标题是否正确
        local title_check="unknown"
        if [[ "$title" == *"AI.link.cn"* ]]; then
            title_check="correct"
        elif [ -n "$title" ]; then
            title_check="different"
        fi
        
        log "✅ 网站服务正常 (HTTP 200, 响应时间: ${response_time}秒)"
        echo '{"component":"website","status":"healthy","http_code":200,"response_time":'$response_time',"title":"'$title'","title_check":"'$title_check'","timestamp":"'$(date -Iseconds)'"}'
    else
        log "⚠️  网站服务异常 (HTTP $http_code)"
        echo '{"component":"website","status":"unhealthy","http_code":'$http_code',"response_time":'$response_time',"timestamp":"'$(date -Iseconds)'"}'
    fi
}

# 2. 收集自动化系统状态
collect_automation_status() {
    log "🔍 收集自动化系统状态..."
    
    # 检查最新的自动化日志
    local latest_log=$(ls -t "$LOG_DIR"/auto_update_*.log 2>/dev/null | head -1)
    
    if [ -n "$latest_log" ]; then
        local last_run=$(stat -c %y "$latest_log" | cut -d' ' -f1-2)
        local log_age=$(($(date +%s) - $(stat -c %Y "$latest_log")))
        
        # 检查日志内容
        local last_lines=$(tail -3 "$latest_log" 2>/dev/null || echo "")
        local status="unknown"
        
        if echo "$last_lines" | grep -q "成功\|success\|正常\|====="; then
            status="healthy"
            log "✅ 自动化系统正常 (最后运行: $last_run)"
        elif echo "$last_lines" | grep -q "错误\|error\|失败\|失败\|⚠️"; then
            status="warning"
            log "⚠️  自动化系统有警告 (最后运行: $last_run)"
        else
            status="unknown"
            log "❓ 自动化系统状态未知 (最后运行: $last_run)"
        fi
        
        # 检查是否超过24小时未运行
        if [ $log_age -gt 86400 ]; then
            status="critical"
            log "🚨 自动化系统超过24小时未运行!"
        fi
        
        echo '{"component":"automation","status":"'$status'","last_run":"'$last_run'","log_age_seconds":'$log_age',"timestamp":"'$(date -Iseconds)'"}'
    else
        echo '{"component":"automation","status":"critical","last_run":null,"error":"未找到自动化日志","timestamp":"'$(date -Iseconds)'"}'
        log "🚨 未找到自动化系统日志"
    fi
}

# 3. 收集社交媒体状态
collect_social_media_status() {
    log "🔍 收集社交媒体状态..."
    
    local linkedin_status="unknown"
    local zhihu_status="unknown"
    local twitter_status="unknown"
    
    # 检查Twitter状态
    if [ -f "/root/.openclaw/workspace/x_twitter_promotion.md" ]; then
        twitter_status="configured"
    else
        twitter_status="not_configured"
    fi
    
    # 检查LinkedIn和知乎执行指南
    if [ -f "/tmp/social_media_execution_guide.md" ]; then
        local guide_age=$(($(date +%s) - $(stat -c %Y "/tmp/social_media_execution_guide.md" 2>/dev/null || echo 0)))
        
        if [ $guide_age -lt 3600 ]; then
            linkedin_status="pending"
            zhihu_status="pending"
            log "📝 社交媒体执行指南存在 (<1小时)"
        elif [ $guide_age -lt 86400 ]; then
            linkedin_status="stale"
            zhihu_status="stale"
            log "⚠️  社交媒体执行指南陈旧 (<24小时)"
        else
            linkedin_status="very_stale"
            zhihu_status="very_stale"
            log "🚨 社交媒体执行指南非常陈旧 (>24小时)"
        fi
    else
        linkedin_status="not_started"
        zhihu_status="not_started"
        log "❌ 未找到社交媒体执行指南"
    fi
    
    echo '{"component":"social_media","twitter":"'$twitter_status'","linkedin":"'$linkedin_status'","zhihu":"'$zhihu_status'","timestamp":"'$(date -Iseconds)'"}'
}

# 4. 收集评测工作状态
collect_review_status() {
    log "🔍 收集评测工作状态..."
    
    local grammarly_file="/root/.openclaw/workspace/content/tools/grammarly_ai_review_20260519.md"
    local chatgpt_file="/root/.openclaw/workspace/content/tools/chatgpt_4o_review_20260522.md"
    
    local grammarly_lines=0
    local chatgpt_lines=0
    local grammarly_mtime=""
    local chatgpt_mtime=""
    local grammarly_age=0
    local chatgpt_age=0
    
    # Grammarly评测
    if [ -f "$grammarly_file" ]; then
        grammarly_lines=$(wc -l < "$grammarly_file" 2>/dev/null || echo 0)
        grammarly_mtime=$(stat -c %y "$grammarly_file" 2>/dev/null | cut -d' ' -f1-2 || echo "unknown")
        grammarly_age=$(($(date +%s) - $(stat -c %Y "$grammarly_file" 2>/dev/null || echo 0)))
    fi
    
    # ChatGPT评测
    if [ -f "$chatgpt_file" ]; then
        chatgpt_lines=$(wc -l < "$chatgpt_file" 2>/dev/null || echo 0)
        chatgpt_mtime=$(stat -c %y "$chatgpt_file" 2>/dev/null | cut -d' ' -f1-2 || echo "unknown")
        chatgpt_age=$(($(date +%s) - $(stat -c %Y "$chatgpt_file" 2>/dev/null || echo 0)))
    fi
    
    # 计算进度百分比 (目标: Grammarly 294行, ChatGPT 389行)
    local grammarly_progress=0
    local chatgpt_progress=0
    
    if [ $grammarly_lines -gt 0 ]; then
        grammarly_progress=$(echo "scale=2; $grammarly_lines / 294 * 100" | bc 2>/dev/null || echo 0)
    fi
    
    if [ $chatgpt_lines -gt 0 ]; then
        chatgpt_progress=$(echo "scale=2; $chatgpt_lines / 389 * 100" | bc 2>/dev/null || echo 0)
    fi
    
    # 状态评估
    local grammarly_status="unknown"
    local chatgpt_status="unknown"
    
    if [ $grammarly_age -lt 86400 ]; then
        grammarly_status="recent"
    elif [ $grammarly_age -lt 172800 ]; then
        grammarly_status="stale"
    else
        grammarly_status="very_stale"
    fi
    
    if [ $chatgpt_age -lt 86400 ]; then
        chatgpt_status="recent"
    elif [ $chatgpt_age -lt 172800 ]; then
        chatgpt_status="stale"
    else
        chatgpt_status="very_stale"
    fi
    
    log "📊 Grammarly评测: ${grammarly_lines}行 (${grammarly_progress}%), 最后修改: $grammarly_mtime"
    log "📊 ChatGPT评测: ${chatgpt_lines}行 (${chatgpt_progress}%), 最后修改: $chatgpt_mtime"
    
    echo '{"component":"reviews","grammarly":{"lines":'$grammarly_lines',"progress":'$grammarly_progress',"last_modified":"'$grammarly_mtime'","status":"'$grammarly_status'","age_seconds":'$grammarly_age'},"chatgpt":{"lines":'$chatgpt_lines',"progress":'$chatgpt_progress',"last_modified":"'$chatgpt_mtime'","status":"'$chatgpt_status'","age_seconds":'$chatgpt_age'},"timestamp":"'$(date -Iseconds)'"}'
}

# 5. 收集系统资源状态
collect_system_status() {
    log "🔍 收集系统资源状态..."
    
    local disk_usage=0
    local memory_usage=0
    local load_avg=0
    
    # 磁盘使用率
    disk_usage=$(df -h / 2>/dev/null | awk 'NR==2{print $5}' | sed 's/%//' || echo 0)
    
    # 内存使用率
    memory_usage=$(free -m 2>/dev/null | awk 'NR==2{printf "%.1f", $3*100/$2}' || echo 0)
    
    # 系统负载
    load_avg=$(cat /proc/loadavg 2>/dev/null | awk '{print $1}' || echo 0)
    
    # 状态评估
    local disk_status="healthy"
    local memory_status="healthy"
    
    if [ $disk_usage -gt 80 ]; then
        disk_status="warning"
    elif [ $disk_usage -gt 90 ]; then
        disk_status="critical"
    fi
    
    if [ $(echo "$memory_usage > 80" | bc 2>/dev/null || echo 0) -eq 1 ]; then
        memory_status="warning"
    elif [ $(echo "$memory_usage > 90" | bc 2>/dev/null || echo 0) -eq 1 ]; then
        memory_status="critical"
    fi
    
    log "💾 磁盘使用率: ${disk_usage}%, 内存使用率: ${memory_usage}%, 系统负载: $load_avg"
    
    echo '{"component":"system","disk_usage":'$disk_usage',"memory_usage":'$memory_usage',"load_average":'$load_avg',"disk_status":"'$disk_status'","memory_status":"'$memory_status'","timestamp":"'$(date -Iseconds)'"}'
}

# 主函数
main() {
    log "🚀 开始收集系统状态..."
    
    # 创建状态数组 - 重定向所有日志输出到日志文件，不污染JSON
    {
        echo "["
        
        # 收集所有状态，只输出JSON
        collect_website_status
        echo ","
        
        collect_automation_status
        echo ","
        
        collect_social_media_status
        echo ","
        
        collect_review_status
        echo ","
        
        collect_system_status
        
        echo "]"
    } > "$STATUS_FILE" 2>/dev/null
    
    # 创建最新的状态文件链接
    ln -sf "status_$TIMESTAMP.json" "$STATUS_DIR/latest_status.json"
    
    # 记录成功
    local file_size=$(stat -c%s "$STATUS_FILE" 2>/dev/null || echo 0)
    log "✅ 状态收集完成: $STATUS_FILE (${file_size}字节)"
    
    # 输出摘要
    echo ""
    echo "📊 状态收集摘要:"
    echo "----------------"
    echo "• 网站服务: $(grep -o '"status":"[^"]*"' "$STATUS_FILE" | head -1 | cut -d'"' -f4)"
    echo "• 自动化系统: $(grep -o '"status":"[^"]*"' "$STATUS_FILE" | head -2 | tail -1 | cut -d'"' -f4)"
    echo "• Grammarly评测: $(tail -50 "$STATUS_FILE" | grep -o '"progress":[0-9.]*' | head -1 | cut -d':' -f2)%"
    echo "• ChatGPT评测: $(tail -50 "$STATUS_FILE" | grep -o '"progress":[0-9.]*' | tail -1 | cut -d':' -f2)%"
    echo "• 系统资源: 磁盘$(grep -o '"disk_usage":[0-9]*' "$STATUS_FILE" | cut -d':' -f2)%, 内存$(grep -o '"memory_usage":[0-9.]*' "$STATUS_FILE" | cut -d':' -f2)%"
    echo ""
    echo "状态文件: $STATUS_FILE"
    echo "最新链接: $STATUS_DIR/latest_status.json"
}

# 执行主函数
main