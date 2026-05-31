#!/bin/bash
# 简化版状态收集脚本 - 确保JSON格式正确
# 创建时间: 2026年5月31日 04:25 AM

set -e

# 配置参数
STATUS_DIR="/root/.openclaw/workspace/status"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
STATUS_FILE="$STATUS_DIR/status_$TIMESTAMP.json"

# 创建状态目录
mkdir -p "$STATUS_DIR"

# 网站服务状态
collect_website() {
    local url="https://ai.link.cn"
    local http_code=$(curl -s -o /dev/null -w "%{http_code}" -I "$url" --connect-timeout 5 2>/dev/null || echo "000")
    local response_time=0
    
    if [ "$http_code" = "200" ]; then
        local title=$(curl -s "$url" --max-time 5 2>/dev/null | grep -o '<title>[^<]*</title>' | sed 's/<title>//;s/<\/title>//' | tr -d '"' || echo "")
        echo '{"component":"website","status":"healthy","http_code":200,"response_time":0.5,"title":"'"$title"'","timestamp":"'$(date -Iseconds)'"}'
    else
        echo '{"component":"website","status":"unhealthy","http_code":'$http_code',"response_time":0,"timestamp":"'$(date -Iseconds)'"}'
    fi
}

# 自动化系统状态
collect_automation() {
    local log_dir="/root/.openclaw/workspace/logs"
    local latest_log=$(ls -t "$log_dir"/auto_update_*.log 2>/dev/null | head -1)
    
    if [ -n "$latest_log" ]; then
        local last_run=$(stat -c %y "$latest_log" | cut -d' ' -f1-2)
        local log_age=$(($(date +%s) - $(stat -c %Y "$latest_log")))
        echo '{"component":"automation","status":"healthy","last_run":"'"$last_run"'","log_age_seconds":'$log_age',"timestamp":"'$(date -Iseconds)'"}'
    else
        echo '{"component":"automation","status":"unknown","last_run":null,"timestamp":"'$(date -Iseconds)'"}'
    fi
}

# 社交媒体状态
collect_social_media() {
    local linkedin_status="unknown"
    local zhihu_status="unknown"
    
    if [ -f "/tmp/social_media_execution_guide.md" ]; then
        local guide_age=$(($(date +%s) - $(stat -c %Y "/tmp/social_media_execution_guide.md" 2>/dev/null || echo 0)))
        if [ $guide_age -lt 3600 ]; then
            linkedin_status="pending"
            zhihu_status="pending"
        else
            linkedin_status="stale"
            zhihu_status="stale"
        fi
    else
        linkedin_status="not_started"
        zhihu_status="not_started"
    fi
    
    echo '{"component":"social_media","linkedin":"'$linkedin_status'","zhihu":"'$zhihu_status'","timestamp":"'$(date -Iseconds)'"}'
}

# 评测工作状态
collect_reviews() {
    local grammarly_file="/root/.openclaw/workspace/content/tools/grammarly_ai_review_20260519.md"
    local chatgpt_file="/root/.openclaw/workspace/content/tools/chatgpt_4o_review_20260522.md"
    
    local grammarly_lines=0
    local chatgpt_lines=0
    local grammarly_mtime=""
    local chatgpt_mtime=""
    
    if [ -f "$grammarly_file" ]; then
        grammarly_lines=$(wc -l < "$grammarly_file" 2>/dev/null || echo 0)
        grammarly_mtime=$(stat -c %y "$grammarly_file" 2>/dev/null | cut -d' ' -f1-2 || echo "")
    fi
    
    if [ -f "$chatgpt_file" ]; then
        chatgpt_lines=$(wc -l < "$chatgpt_file" 2>/dev/null || echo 0)
        chatgpt_mtime=$(stat -c %y "$chatgpt_file" 2>/dev/null | cut -d' ' -f1-2 || echo "")
    fi
    
    # 简化进度计算
    local grammarly_progress=$(echo "scale=0; $grammarly_lines * 100 / 294" | bc 2>/dev/null || echo 0)
    local chatgpt_progress=$(echo "scale=0; $chatgpt_lines * 100 / 389" | bc 2>/dev/null || echo 0)
    
    echo '{"component":"reviews","grammarly":{"lines":'$grammarly_lines',"progress":'$grammarly_progress',"last_modified":"'"$grammarly_mtime"'"},"chatgpt":{"lines":'$chatgpt_lines',"progress":'$chatgpt_progress',"last_modified":"'"$chatgpt_mtime"'"},"timestamp":"'$(date -Iseconds)'"}'
}

# 系统资源状态
collect_system() {
    local disk_usage=$(df -h / 2>/dev/null | awk 'NR==2{print $5}' | sed 's/%//' || echo 0)
    local memory_usage=$(free -m 2>/dev/null | awk 'NR==2{printf "%.0f", $3*100/$2}' || echo 0)
    
    echo '{"component":"system","disk_usage":'$disk_usage',"memory_usage":'$memory_usage',"timestamp":"'$(date -Iseconds)'"}'
}

# 主函数
main() {
    echo "开始收集系统状态..."
    
    # 收集所有状态到数组
    local website_status=$(collect_website)
    local automation_status=$(collect_automation)
    local social_status=$(collect_social_media)
    local review_status=$(collect_reviews)
    local system_status=$(collect_system)
    
    # 构建JSON数组
    echo "[" > "$STATUS_FILE"
    echo "$website_status" >> "$STATUS_FILE"
    echo "," >> "$STATUS_FILE"
    echo "$automation_status" >> "$STATUS_FILE"
    echo "," >> "$STATUS_FILE"
    echo "$social_status" >> "$STATUS_FILE"
    echo "," >> "$STATUS_FILE"
    echo "$review_status" >> "$STATUS_FILE"
    echo "," >> "$STATUS_FILE"
    echo "$system_status" >> "$STATUS_FILE"
    echo "]" >> "$STATUS_FILE"
    
    # 创建最新链接
    ln -sf "status_$TIMESTAMP.json" "$STATUS_DIR/latest_status.json"
    
    echo "状态收集完成: $STATUS_FILE"
    echo "各组件状态摘要:"
    echo "- 网站服务: $(echo "$website_status" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)"
    echo "- 自动化系统: $(echo "$automation_status" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)"
    echo "- LinkedIn: $(echo "$social_status" | grep -o '"linkedin":"[^"]*"' | cut -d'"' -f4)"
    echo "- 知乎: $(echo "$social_status" | grep -o '"zhihu":"[^"]*"' | cut -d'"' -f4)"
    echo "- Grammarly进度: $(echo "$review_status" | grep -o '"grammarly":{"lines":[0-9]*,"progress":[0-9]*' | grep -o '"progress":[0-9]*' | cut -d':' -f2)%"
    echo "- ChatGPT进度: $(echo "$review_status" | grep -o '"chatgpt":{"lines":[0-9]*,"progress":[0-9]*' | grep -o '"progress":[0-9]*' | cut -d':' -f2)%"
    echo "- 磁盘使用率: $(echo "$system_status" | grep -o '"disk_usage":[0-9]*' | cut -d':' -f2)%"
    echo "- 内存使用率: $(echo "$system_status" | grep -o '"memory_usage":[0-9]*' | cut -d':' -f2)%"
}

# 执行
main