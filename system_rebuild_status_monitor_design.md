# 🚨 状态监控系统设计文档
## 子系统：状态监控系统
## 设计时间：2026年5月31日 04:20 AM
## 状态：设计阶段

## 📋 设计概述

### 核心目标
**确保状态不明不超过30分钟**

### 设计原则
1. **实时性**: 状态变化立即检测
2. **可靠性**: 系统故障不影响监控
3. **可扩展性**: 支持新增监控组件
4. **可视化**: 状态信息直观可读
5. **告警性**: 异常状态及时告警

## 🏗️ 系统架构

### 三层架构设计
```
┌─────────────────────────────────────────────────────────┐
│                    监控展示层 (Presentation)             │
├─────────────────────────────────────────────────────────┤
│  HEARTBEAT.md状态更新 │ 实时状态面板 │ 状态报告生成     │
└─────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────┐
│                    监控处理层 (Processing)               │
├─────────────────────────────────────────────────────────┤
│ 状态收集 │ 状态分析 │ 告警判断 │ 状态存储              │
└─────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────┐
│                    监控数据层 (Data)                     │
├─────────────────────────────────────────────────────────┤
│ 网站服务 │ 自动化系统 │ 社交媒体 │ 评测工作 │ 其他组件 │
└─────────────────────────────────────────────────────────┘
```

### 监控组件清单
1. **网站服务监控** (优先级: 高)
   - HTTP状态码 (200正常，其他异常)
   - 响应时间 (<1秒正常，>3秒警告，>5秒异常)
   - 网站标题验证

2. **自动化系统监控** (优先级: 高)
   - 定时任务执行状态
   - Git提交状态
   - Vercel部署状态
   - 脚本执行日志

3. **社交媒体状态监控** (优先级: 中)
   - LinkedIn账号存在性
   - 知乎专栏存在性
   - 内容更新频率
   - 互动状态

4. **评测工作进度监控** (优先级: 高)
   - 文件修改时间
   - 内容长度变化
   - 进度百分比计算
   - 任务状态切换

5. **系统资源监控** (优先级: 中)
   - 磁盘使用率
   - 内存使用率
   - CPU使用率
   - 网络连通性

## 🛠️ 技术实现

### 1. 状态收集脚本 (`status_collector.sh`)
```bash
#!/bin/bash
# 文件名: status_collector.sh
# 功能: 收集所有组件的状态信息
# 输出: JSON格式状态数据

# 配置参数
STATUS_DIR="/root/.openclaw/workspace/status"
LOG_DIR="/root/.openclaw/workspace/logs"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")

# 创建状态目录
mkdir -p "$STATUS_DIR"

# 收集状态函数
collect_website_status() {
    local url="https://ai.link.cn"
    local start_time=$(date +%s.%N)
    local http_code=$(curl -s -o /dev/null -w "%{http_code}" -I "$url" --connect-timeout 5)
    local end_time=$(date +%s.%N)
    local response_time=$(echo "$end_time - $start_time" | bc | awk '{printf "%.3f", $1}')
    
    if [ "$http_code" = "200" ]; then
        local title=$(curl -s "$url" | grep -o '<title>[^<]*</title>' | sed 's/<title>//;s/<\/title>//')
        echo '{"component":"website","status":"healthy","http_code":200,"response_time":'$response_time',"title":"'"$title"'","timestamp":"'$(date -Iseconds)'"}'
    else
        echo '{"component":"website","status":"unhealthy","http_code":'$http_code',"response_time":'$response_time',"timestamp":"'$(date -Iseconds)'"}'
    fi
}

collect_automation_status() {
    # 检查自动化系统日志
    local latest_log=$(ls -t "$LOG_DIR"/auto_update_*.log 2>/dev/null | head -1)
    local last_run=""
    
    if [ -n "$latest_log" ]; then
        last_run=$(stat -c %y "$latest_log" | cut -d' ' -f1-2)
        local log_content=$(tail -5 "$latest_log")
        
        if echo "$log_content" | grep -q "成功\|success\|正常"; then
            echo '{"component":"automation","status":"healthy","last_run":"'$last_run'","timestamp":"'$(date -Iseconds)'"}'
        else
            echo '{"component":"automation","status":"warning","last_run":"'$last_run'","timestamp":"'$(date -Iseconds)'"}'
        fi
    else
        echo '{"component":"automation","status":"unhealthy","last_run":null,"timestamp":"'$(date -Iseconds)'"}'
    fi
}

collect_social_media_status() {
    # 检查社交媒体状态
    local linkedin_status="unknown"
    local zhihu_status="unknown"
    
    # 检查执行指南是否存在
    if [ -f "/tmp/social_media_execution_guide.md" ]; then
        local guide_age=$(($(date +%s) - $(stat -c %Y "/tmp/social_media_execution_guide.md")))
        
        if [ $guide_age -lt 3600 ]; then
            linkedin_status="pending"
            zhihu_status="pending"
        else
            linkedin_status="stale"
            zhihu_status="stale"
        fi
    fi
    
    echo '{"component":"social_media","linkedin_status":"'$linkedin_status'","zhihu_status":"'$zhihu_status'","timestamp":"'$(date -Iseconds)'"}'
}

collect_review_status() {
    # 检查评测工作状态
    local grammarly_file="/root/.openclaw/workspace/content/tools/grammarly_ai_review_20260519.md"
    local chatgpt_file="/root/.openclaw/workspace/content/tools/chatgpt_4o_review_20260522.md"
    
    local grammarly_lines=0
    local chatgpt_lines=0
    local grammarly_mtime=""
    local chatgpt_mtime=""
    
    if [ -f "$grammarly_file" ]; then
        grammarly_lines=$(wc -l < "$grammarly_file")
        grammarly_mtime=$(stat -c %y "$grammarly_file" | cut -d' ' -f1-2)
    fi
    
    if [ -f "$chatgpt_file" ]; then
        chatgpt_lines=$(wc -l < "$chatgpt_file")
        chatgpt_mtime=$(stat -c %y "$chatgpt_file" | cut -d' ' -f1-2)
    fi
    
    # 计算进度百分比 (基于目标294行和389行)
    local grammarly_progress=$(echo "scale=2; $grammarly_lines / 294 * 100" | bc)
    local chatgpt_progress=$(echo "scale=2; $chatgpt_lines / 389 * 100" | bc)
    
    echo '{"component":"reviews","grammarly":{"lines":'$grammarly_lines',"progress":'$grammarly_progress',"last_modified":"'$grammarly_mtime'"},{"chatgpt":{"lines":'$chatgpt_lines',"progress":'$chatgpt_progress',"last_modified":"'$chatgpt_mtime'"},"timestamp":"'$(date -Iseconds)'"}'
}

collect_system_status() {
    # 收集系统资源状态
    local disk_usage=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//')
    local mem_info=$(free -m | awk 'NR==2{printf "%.1f", $3*100/$2}')
    local load_avg=$(cat /proc/loadavg | awk '{print $1}')
    
    echo '{"component":"system","disk_usage":'$disk_usage',"memory_usage":'$mem_info',"load_average":'$load_avg',"timestamp":"'$(date -Iseconds)'"}'
}

# 主收集函数
collect_all_status() {
    echo "[" > "$STATUS_DIR/status_$TIMESTAMP.json"
    
    # 收集所有状态
    collect_website_status >> "$STATUS_DIR/status_$TIMESTAMP.json"
    echo "," >> "$STATUS_DIR/status_$TIMESTAMP.json"
    
    collect_automation_status >> "$STATUS_DIR/status_$TIMESTAMP.json"
    echo "," >> "$STATUS_DIR/status_$TIMESTAMP.json"
    
    collect_social_media_status >> "$STATUS_DIR/status_$TIMESTAMP.json"
    echo "," >> "$STATUS_DIR/status_$TIMESTAMP.json"
    
    collect_review_status >> "$STATUS_DIR/status_$TIMESTAMP.json"
    echo "," >> "$STATUS_DIR/status_$TIMESTAMP.json"
    
    collect_system_status >> "$STATUS_DIR/status_$TIMESTAMP.json"
    
    echo "]" >> "$STATUS_DIR/status_$TIMESTAMP.json"
    
    # 创建最新的状态文件链接
    ln -sf "status_$TIMESTAMP.json" "$STATUS_DIR/latest_status.json"
}

# 执行状态收集
collect_all_status
```

### 2. 状态分析脚本 (`status_analyzer.sh`)
```bash
#!/bin/bash
# 文件名: status_analyzer.sh
# 功能: 分析状态数据，生成告警和建议
# 输入: latest_status.json
# 输出: analysis_results.json

STATUS_DIR="/root/.openclaw/workspace/status"
ANALYSIS_DIR="/root/.openclaw/workspace/analysis"
LATEST_STATUS="$STATUS_DIR/latest_status.json"

mkdir -p "$ANALYSIS_DIR"

analyze_status() {
    local timestamp=$(date +"%Y-%m-%d_%H%M%S")
    local analysis_file="$ANALYSIS_DIR/analysis_$timestamp.json"
    
    # 检查状态文件是否存在
    if [ ! -f "$LATEST_STATUS" ]; then
        echo '{"error":"No status data found","timestamp":"'$(date -Iseconds)'"}' > "$analysis_file"
        return 1
    fi
    
    # 读取状态数据
    local status_data=$(cat "$LATEST_STATUS")
    
    # 分析各个组件
    local alerts=()
    local warnings=()
    local suggestions=()
    
    # 分析网站状态
    local website_status=$(echo "$status_data" | jq -r '.[0].status')
    local website_response_time=$(echo "$status_data" | jq -r '.[0].response_time')
    
    if [ "$website_status" != "healthy" ]; then
        alerts+=("网站服务异常: HTTP状态 $website_status")
    elif [ "$(echo "$website_response_time > 3" | bc)" -eq 1 ]; then
        warnings+=("网站响应时间较慢: ${website_response_time}秒")
    fi
    
    # 分析自动化系统
    local automation_status=$(echo "$status_data" | jq -r '.[1].status')
    local automation_last_run=$(echo "$status_data" | jq -r '.[1].last_run')
    
    if [ "$automation_status" != "healthy" ]; then
        alerts+=("自动化系统异常: $automation_status")
    fi
    
    # 分析社交媒体状态
    local linkedin_status=$(echo "$status_data" | jq -r '.[2].linkedin_status')
    local zhihu_status=$(echo "$status_data" | jq -r '.[2].zhihu_status')
    
    if [ "$linkedin_status" = "stale" ] || [ "$zhihu_status" = "stale" ]; then
        warnings+=("社交媒体状态陈旧，可能任务停滞")
    fi
    
    # 分析评测工作状态
    local grammarly_progress=$(echo "$status_data" | jq -r '.[3].grammarly.progress')
    local chatgpt_progress=$(echo "$status_data" | jq -r '.[3].chatgpt.progress')
    
    if [ "$(echo "$grammarly_progress < 50" | bc)" -eq 1 ]; then
        suggestions+=("Grammarly评测进度较低 ($grammarly_progress%)，需要加速")
    fi
    
    if [ "$(echo "$chatgpt_progress < 50" | bc)" -eq 1 ]; then
        suggestions+=("ChatGPT评测进度较低 ($chatgpt_progress%)，需要加速")
    fi
    
    # 分析系统资源
    local disk_usage=$(echo "$status_data" | jq -r '.[4].disk_usage')
    local memory_usage=$(echo "$status_data" | jq -r '.[4].memory_usage')
    
    if [ "$(echo "$disk_usage > 80" | bc)" -eq 1 ]; then
        warnings+=("磁盘使用率较高: ${disk_usage}%")
    fi
    
    if [ "$(echo "$memory_usage > 80" | bc)" -eq 1 ]; then
        warnings+=("内存使用率较高: ${memory_usage}%")
    fi
    
    # 生成分析结果
    local analysis_result=$(cat << EOF
{
    "timestamp": "$(date -Iseconds)",
    "overall_status": "${#alerts[@]} > 0 ? "critical" : (${#warnings[@]} > 0 ? "warning" : "healthy")}",
    "alerts": $(printf '%s\n' "${alerts[@]}" | jq -R . | jq -s .),
    "warnings": $(printf '%s\n' "${warnings[@]}" | jq -R . | jq -s .),
    "suggestions": $(printf '%s\n' "${suggestions[@]}" | jq -R . | jq -s .),
    "component_count": 5,
    "analysis_duration": "$(date +%s)"
}
EOF
)
    
    echo "$analysis_result" > "$analysis_file"
    ln -sf "analysis_$timestamp.json" "$ANALYSIS_DIR/latest_analysis.json"
    
    # 更新HEARTBEAT.md状态
    update_heartbeat_status "$analysis_result"
}

update_heartbeat_status() {
    local analysis_result="$1"
    local heartbeat_file="/root/.openclaw/workspace/HEARTBEAT.md"
    
    # 提取关键信息
    local overall_status=$(echo "$analysis_result" | jq -r '.overall_status')
    local alert_count=$(echo "$analysis_result" | jq -r '.alerts | length')
    local warning_count=$(echo "$analysis_result" | jq -r '.warnings | length')
    
    # 创建状态摘要
    local status_summary=""
    if [ "$alert_count" -gt 0 ]; then
        status_summary="🚨 有 $alert_count 个紧急告警"
    elif [ "$warning_count" -gt 0 ]; then
        status_summary="⚠️  有 $warning_count 个警告"
    else
        status_summary="✅ 所有系统正常"
    fi
    
    # 在HEARTBEAT.md中添加状态摘要
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local status_entry="\n### 📊 实时状态监控 (更新于: $timestamp)\n- **整体状态**: $status_summary\n- **详细报告**: 查看最新分析报告\n"
    
    # 这里需要实际更新HEARTBEAT.md文件
    # 注意：这个函数需要在HEARTBEAT.md中有固定位置插入内容
}

# 执行分析
analyze_status
```

### 3. 状态数据库 (`status_database.json`结构)
```json
{
  "database_version": "1.0",
  "last_updated": "2026-05-31T04:20:00+08:00",
  "components": {
    "website": {
      "check_interval": 300,
      "alert_threshold": 600,
      "critical_threshold": 1800,
      "history": []
    },
    "automation": {
      "check_interval": 3600,
      "alert_threshold": 7200,
      "critical_threshold": 86400,
      "history": []
    },
    "social_media": {
      "check_interval": 1800,
      "alert_threshold": 3600,
      "critical_threshold": 7200,
      "history": []
    },
    "reviews": {
      "check_interval": 3600,
      "alert_threshold": 7200,
      "critical_threshold": 172800,
      "history": []
    },
    "system": {
      "check_interval": 1800,
      "alert_threshold": 3600,
      "critical_threshold": 7200,
      "history": []
    }
  },
  "alert_history": [],
  "configuration": {
    "enabled": true,
    "notification_channels": ["heartbeat", "log"],
    "retention_days": 7
  }
}
```

## 🚨 告警机制

### 告警级别定义
1. **正常 (Normal)**: 所有组件状态正常
2. **警告 (Warning)**: 单个组件轻微异常，不影响核心功能
3. **告警 (Alert)**: 关键组件异常，需要关注
4. **紧急 (Critical)**: 多个组件异常，影响核心功能

### 告警触发条件
1. **网站服务**:
   - HTTP状态码非200 → 警告
   - 响应时间>3秒 → 警告
   - 响应时间>5秒 → 告警
   - 无法访问 → 紧急

2. **自动化系统**:
   - 24小时无更新 → 警告
   - 48小时无更新 → 告警
   - 脚本执行失败 → 紧急

3. **社交媒体**:
   - 状态不明>30分钟 → 警告
   - 状态不明>1小时 → 告警
   - 状态不明>2小时 → 紧急

4. **评测工作**:
   - 24小时无进展 → 警告
   - 48小时无进展 → 告警
   - 72小时无进展 → 紧急

## 📊 监控仪表板

### 实时状态面板设计
```
┌─────────────────────────────────────────────────────┐
│              AI.link.cn 系统状态监控面板            │
├─────────────────────────────────────────────────────┤
│ 更新时间: 2026-05-31 04:20:00                       │
│ 整体状态: 🟢 正常                                   │
├─────────────────────────────────────────────────────┤
│ 组件              状态       最后检查     详情       │
├─────────────────────────────────────────────────────┤
│ 网站服务         🟢 正常    04:20:00     HTTP 200   │
│ 自动化系统       🟢 正常    04:20:00     已运行     │
│ LinkedIn         🟡 警告    04:20:00     状态不明   │
│ 知乎             🟡 警告    04:20:00     状态不明   │
│ Grammarly评测    🟡 警告    04:20:00     72%进度    │
│ ChatGPT评测      🟡 警告    04:20:00     62%进度    │
│ 系统资源         🟢 正常    04:20:00     正常       │
└─────────────────────────────────────────────────────┘
```

### 状态颜色编码
- 🟢 绿色: 正常 (所有检查通过)
- 🟡 黄色: 警告 (轻微问题，需要关注)
- 🟠 橙色: 告警 (需要立即处理)
- 🔴 红色: 紧急 (系统功能受影响)

## 📈 历史数据分析

### 数据保留策略
1. **实时数据**: 保留24小时
2. **日度汇总**: 保留7天
3. **周度汇总**: 保留4周
4. **月度报告**: 永久保留

### 分析维度
1. **可用性分析**: 系统整体可用时间百分比
2. **性能趋势**: 响应时间变化趋势
3. **故障分析**: 故障类型和频率统计
4. **改进建议**: 基于历史数据的优化建议

## 🔧 部署与维护

### 部署步骤
1. **创建目录结构** (04:20-04:30)
   ```
   mkdir -p /root/.openclaw/workspace/{status,analysis,logs}
   ```

2. **安装依赖** (04:30-04:35)
   ```
   apt-get install -y jq bc curl
   ```

3. **部署脚本** (04:35-04:45)
   ```
   cp status_collector.sh /root/.openclaw/workspace/scripts/
   cp status_analyzer.sh /root/.openclaw/workspace/scripts/
   chmod +x /root/.openclaw/workspace/scripts/status_*.sh
   ```

4. **配置定时任务** (04:45-04:50)
   ```
   # 每5分钟收集一次状态
   */5 * * * * /root/.openclaw/workspace/scripts/status_collector.sh
   
   # 每10分钟分析一次状态
   */10 * * * * /root/.openclaw/workspace/scripts/status_analyzer.sh
   ```

5. **初始化数据库** (04:50-04:55)
   ```
   echo '{"database_version":"1.0","last_updated":"'$(date -Iseconds)'"}' > /root/.openclaw/workspace/status/status_database.json
   ```

### 维护任务
1. **每日维护**:
   - 清理过期状态文件
   - 生成日度状态报告
   - 验证监控系统运行状态

2. **每周维护**:
   - 分析周度趋势
   - 优化监控阈值
   - 更新组件列表

3. **每月维护**:
   - 生成月度可用性报告
   - 评估监控系统效果
   - 制定改进计划

## ✅ 验证标准

### 功能验证清单
- [ ] 状态收集脚本能够正常运行
- [ ] 状态分析脚本能够生成正确报告
- [ ] 告警机制能够正确触发
- [ ] HEARTBEAT.md能够自动更新状态
- [ ] 历史数据能够正确保存和查询

### 性能验证清单
- [ ] 状态收集时间<10秒
- [ ] 状态分析时间<5秒
- [ ] 数据库查询响应时间<1秒
- [ ] 系统资源占用<1% CPU, <50MB内存

### 可靠性验证清单
- [ ] 监控系统自身故障不影响主系统
- [ ] 网络中断时能够优雅降级
- [ ] 磁盘满时能够自动清理旧数据
- [ ] 脚本错误时能够记录日志并恢复

## 🎯 实施时间表

### 今日实施计划 (2026年5月31日)
1. **04:20-04:30**: 完成设计文档
2. **04:30-04:45**: 创建状态收集脚本
3. **04:45-05:00**: 创建状态分析脚本
4. **05:00-05:15**: 配置定时任务
5. **05:15-05:30**: 验证系统功能
6. **05:30-05:45**: 集成到HEARTBEAT.md
7. **05:45-06:00**: 生成初始状态报告

### 验收标准
1. 状态监控系统能够每5分钟收集一次状态
2. 状态分析系统能够每10分钟生成一次报告
3. HEARTBEAT.md能够显示实时状态
4. 所有组件状态能够正确监控

---

**设计完成时间**: 2026年5月31日 04:20 AM
**设计者**: AI.link.cn 系统重建团队
**状态**: 设计完成，等待实施