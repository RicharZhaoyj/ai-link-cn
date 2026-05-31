# 🚨 任务依赖关系系统设计文档
## 子系统：任务依赖关系系统
## 设计时间：2026年5月31日 04:50 AM
## 状态：紧急设计阶段

## 📋 设计概述

### 核心目标
**使评测工作能够独立执行，解除对社交媒体的依赖**

### 问题背景
1. **当前问题**: Grammarly和ChatGPT评测完全依赖于社交媒体任务完成
2. **灾难影响**: 社交媒体延迟6天 → 所有评测工作完全停滞
3. **系统风险**: 单一依赖点导致整个系统瘫痪

### 设计原则
1. **独立性**: 每个任务应尽可能独立执行
2. **容错性**: 主路径失败时应有备用路径
3. **进度跟踪**: 实时监控任务进度和状态
4. **优先级管理**: 紧急任务优先执行

## 🏗️ 系统架构

### 当前依赖关系 (问题状态)
```
社交媒体建立 → Grammarly评测 → ChatGPT评测
     ↓
   阻塞6天 → 评测完全停滞
```

### 目标依赖关系 (重建后)
```
社交媒体建立 (并行任务)
     ↘
Grammarly评测 (独立任务) → 可独立执行
     ↗
ChatGPT评测 (独立任务)   → 可独立执行
```

### 三层架构设计
```
┌─────────────────────────────────────────────────────────┐
│                 任务调度层 (Scheduler)                   │
├─────────────────────────────────────────────────────────┤
│ 任务优先级 │ 依赖关系解析 │ 资源分配 │ 执行调度          │
└─────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────┐
│                 任务执行层 (Executor)                    │
├─────────────────────────────────────────────────────────┤
│ 独立任务执行 │ 依赖任务执行 │ 并行执行 │ 错误恢复        │
└─────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────┐
│                 任务定义层 (Definition)                  │
├─────────────────────────────────────────────────────────┤
│ Grammarly评测 │ ChatGPT评测 │ 社交媒体 │ 其他任务        │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ 技术实现

### 1. 任务定义文件 (`task_definitions.json`)
```json
{
  "version": "1.0",
  "tasks": {
    "grammarly_review": {
      "id": "task_001",
      "name": "Grammarly AI评测完成",
      "description": "完成Grammarly AI评测文章，从212行增加到294行",
      "type": "content_creation",
      "priority": "high",
      "status": "pending",
      "progress": 72,
      "target_progress": 100,
      "dependencies": [],
      "independent": true,
      "estimated_time": "4小时",
      "start_condition": "immediate",
      "completion_criteria": "文件达到294行",
      "file_path": "/root/.openclaw/workspace/content/tools/grammarly_ai_review_20260519.md",
      "created_at": "2026-05-19",
      "last_updated": "2026-05-27"
    },
    "chatgpt_review": {
      "id": "task_002",
      "name": "ChatGPT-4o评测推进",
      "description": "推进ChatGPT-4o评测，从302行增加到389行",
      "type": "content_creation",
      "priority": "high",
      "status": "pending",
      "progress": 77,
      "target_progress": 80,
      "dependencies": [],
      "independent": true,
      "estimated_time": "3小时",
      "start_condition": "immediate",
      "completion_criteria": "文件达到389行",
      "file_path": "/root/.openclaw/workspace/content/tools/chatgpt_4o_review_20260522.md",
      "created_at": "2026-05-22",
      "last_updated": "2026-05-27"
    },
    "linkedin_setup": {
      "id": "task_003",
      "name": "LinkedIn专业页面创建",
      "description": "创建LinkedIn专业页面，建立品牌形象",
      "type": "social_media",
      "priority": "critical",
      "status": "blocked",
      "progress": 0,
      "target_progress": 100,
      "dependencies": [],
      "independent": true,
      "estimated_time": "2小时",
      "start_condition": "manual",
      "completion_criteria": "页面创建成功并发布",
      "execution_guide": "/tmp/social_media_execution_guide.md",
      "blocked_since": "2026-05-24",
      "blocked_days": 6
    },
    "zhihu_setup": {
      "id": "task_004",
      "name": "知乎专栏创建",
      "description": "创建知乎专栏，发布深度内容",
      "type": "social_media",
      "priority": "critical",
      "status": "blocked",
      "progress": 0,
      "target_progress": 100,
      "dependencies": [],
      "independent": true,
      "estimated_time": "2小时",
      "start_condition": "manual",
      "completion_criteria": "专栏创建成功并发布文章",
      "execution_guide": "/tmp/social_media_execution_guide.md",
      "blocked_since": "2026-05-24",
      "blocked_days": 6
    }
  },
  "dependency_rules": {
    "enable_parallel_execution": true,
    "allow_independent_tasks": true,
    "critical_path_override": true,
    "failover_strategy": "continue_others"
  }
}
```

### 2. 任务管理器脚本 (`task_manager.sh`)
```bash
#!/bin/bash
# 任务依赖关系管理系统
# 版本: 1.0 (紧急重建版本)

set -e

# 配置参数
TASK_DIR="/root/.openclaw/workspace/tasks"
TASK_DEF_FILE="$TASK_DIR/task_definitions.json"
TASK_STATUS_FILE="$TASK_DIR/task_status.json"
LOG_DIR="/root/.openclaw/workspace/logs"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")

# 创建目录
mkdir -p "$TASK_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/task_manager.log"
}

# 初始化任务系统
init_task_system() {
    log "初始化任务依赖关系系统..."
    
    if [ ! -f "$TASK_DEF_FILE" ]; then
        log "创建初始任务定义文件..."
        cat > "$TASK_DEF_FILE" << 'EOF'
{
  "version": "1.0",
  "last_updated": "$(date -Iseconds)",
  "tasks": {},
  "dependency_rules": {
    "enable_parallel_execution": true,
    "allow_independent_tasks": true,
    "critical_path_override": true
  }
}
EOF
    fi
    
    log "✅ 任务系统初始化完成"
}

# 分析任务依赖关系
analyze_dependencies() {
    log "分析任务依赖关系..."
    
    local task_defs=$(cat "$TASK_DEF_FILE" 2>/dev/null || echo "{}")
    local blocked_tasks=0
    local independent_tasks=0
    local total_tasks=0
    
    # 分析每个任务
    echo "$task_defs" | jq -r '.tasks | keys[]' 2>/dev/null | while read task_id; do
        total_tasks=$((total_tasks + 1))
        
        local status=$(echo "$task_defs" | jq -r ".tasks.\"$task_id\".status")
        local independent=$(echo "$task_defs" | jq -r ".tasks.\"$task_id\".independent")
        
        if [ "$status" = "blocked" ]; then
            blocked_tasks=$((blocked_tasks + 1))
            log "⚠️  任务阻塞: $task_id"
        fi
        
        if [ "$independent" = "true" ]; then
            independent_tasks=$((independent_tasks + 1))
        fi
    done
    
    # 生成分析报告
    local analysis_report=$(cat << EOF
{
    "timestamp": "$(date -Iseconds)",
    "total_tasks": $total_tasks,
    "blocked_tasks": $blocked_tasks,
    "independent_tasks": $independent_tasks,
    "dependency_health": "$(calculate_dependency_health $blocked_tasks $total_tasks)",
    "recommendations": "$(generate_recommendations $blocked_tasks $independent_tasks)"
}
EOF
)
    
    echo "$analysis_report" > "$TASK_DIR/dependency_analysis_$TIMESTAMP.json"
    log "依赖关系分析完成: $TASK_DIR/dependency_analysis_$TIMESTAMP.json"
}

calculate_dependency_health() {
    local blocked=$1
    local total=$2
    
    if [ $total -eq 0 ]; then
        echo "unknown"
    elif [ $blocked -eq 0 ]; then
        echo "healthy"
    elif [ $blocked -eq $total ]; then
        echo "critical"
    else
        echo "warning"
    fi
}

generate_recommendations() {
    local blocked=$1
    local independent=$2
    
    if [ $blocked -gt 0 ]; then
        echo "有$blocked个任务被阻塞，建议启用独立执行模式"
    elif [ $independent -eq 0 ]; then
        echo "所有任务都有依赖，建议增加独立任务"
    else
        echo "依赖关系健康，继续当前策略"
    fi
}

# 解除任务依赖
enable_independent_execution() {
    log "启用任务独立执行模式..."
    
    local task_defs=$(cat "$TASK_DEF_FILE")
    
    # 修改Grammarly评测为独立任务
    task_defs=$(echo "$task_defs" | jq '.tasks.grammarly_review.independent = true')
    task_defs=$(echo "$task_defs" | jq '.tasks.grammarly_review.dependencies = []')
    task_defs=$(echo "$task_defs" | jq '.tasks.grammarly_review.start_condition = "immediate"')
    
    # 修改ChatGPT评测为独立任务
    task_defs=$(echo "$task_defs" | jq '.tasks.chatgpt_review.independent = true')
    task_defs=$(echo "$task_defs" | jq '.tasks.chatgpt_review.dependencies = []')
    task_defs=$(echo "$task_defs" | jq '.tasks.chatgpt_review.start_condition = "immediate"')
    
    # 更新依赖规则
    task_defs=$(echo "$task_defs" | jq '.dependency_rules.enable_parallel_execution = true')
    task_defs=$(echo "$task_defs" | jq '.dependency_rules.allow_independent_tasks = true')
    task_defs=$(echo "$task_defs" | jq '.dependency_rules.critical_path_override = true')
    
    # 保存更新
    echo "$task_defs" > "$TASK_DEF_FILE"
    
    log "✅ 已启用任务独立执行模式"
    log "Grammarly和ChatGPT评测现在可以独立执行，不再依赖社交媒体"
}

# 生成执行计划
generate_execution_plan() {
    log "生成任务执行计划..."
    
    local task_defs=$(cat "$TASK_DEF_FILE")
    local execution_plan=""
    
    # 获取所有独立任务
    local independent_tasks=$(echo "$task_defs" | jq -r '.tasks | to_entries[] | select(.value.independent == true) | .key')
    
    if [ -n "$independent_tasks" ]; then
        execution_plan="## 🎯 独立任务执行计划\n\n"
        
        for task_id in $independent_tasks; do
            local task_name=$(echo "$task_defs" | jq -r ".tasks.\"$task_id\".name")
            local progress=$(echo "$task_defs" | jq -r ".tasks.\"$task_id\".progress")
            local target=$(echo "$task_defs" | jq -r ".tasks.\"$task_id\".target_progress")
            
            execution_plan+="### $task_name\n"
            execution_plan+="- 当前进度: ${progress}% (目标: ${target}%)\n"
            execution_plan+="- 状态: 可立即执行\n"
            execution_plan+="- 建议: 立即开始\n\n"
        done
        
        execution_plan+="## 📋 执行指令\n"
        execution_plan+="1. 立即开始Grammarly评测: 目标今日完成100%\n"
        execution_plan+="2. 并行推进ChatGPT评测: 目标今日达到80%\n"
        execution_plan+="3. 社交媒体任务: 作为独立任务处理，不影响评测工作\n"
    else
        execution_plan="## ⚠️ 警告\n没有找到可独立执行的任务"
    fi
    
    echo "$execution_plan" > "$TASK_DIR/execution_plan_$TIMESTAMP.md"
    log "执行计划生成完成: $TASK_DIR/execution_plan_$TIMESTAMP.md"
    
    # 输出摘要
    echo ""
    echo "📋 任务执行计划摘要:"
    echo "===================="
    echo "$execution_plan"
}

# 更新任务状态
update_task_status() {
    local task_id="$1"
    local status="$2"
    local progress="$3"
    
    log "更新任务状态: $task_id -> $status (进度: ${progress}%)"
    
    local task_defs=$(cat "$TASK_DEF_FILE")
    task_defs=$(echo "$task_defs" | jq ".tasks.\"$task_id\".status = \"$status\"")
    task_defs=$(echo "$task_defs" | jq ".tasks.\"$task_id\".progress = $progress")
    task_defs=$(echo "$task_defs" | jq ".tasks.\"$task_id\".last_updated = \"$(date -Iseconds)\"")
    
    echo "$task_defs" > "$TASK_DEF_FILE"
    
    # 更新状态文件
    local task_status=$(cat << EOF
{
    "task_id": "$task_id",
    "status": "$status",
    "progress": $progress,
    "updated_at": "$(date -Iseconds)",
    "action": "status_update"
}
EOF
)
    
    echo "$task_status" >> "$TASK_STATUS_FILE"
    log "✅ 任务状态更新完成"
}

# 主函数
main() {
    log "🚀 启动任务依赖关系管理系统..."
    
    # 初始化
    init_task_system
    
    # 分析依赖关系
    analyze_dependencies
    
    # 启用独立执行
    enable_independent_execution
    
    # 生成执行计划
    generate_execution_plan
    
    # 输出总结
    echo ""
    echo "✅ 任务依赖关系重建完成!"
    echo ""
    echo "📊 重建成果:"
    echo "1. ✅ 解除评测工作对社交媒体的依赖"
    echo "2. ✅ Grammarly评测可立即独立执行"
    echo "3. ✅ ChatGPT评测可立即独立执行"
    echo "4. ✅ 启用并行执行模式"
    echo "5. ✅ 生成详细执行计划"
    echo ""
    echo "📁 重要文件:"
    echo "• 任务定义: $TASK_DEF_FILE"
    echo "• 执行计划: $TASK_DIR/execution_plan_$TIMESTAMP.md"
    echo "• 依赖分析: $TASK_DIR/dependency_analysis_$TIMESTAMP.json"
    echo ""
    echo "🎯 下一步行动:"
    echo "1. 立即开始Grammarly评测 (目标: 今日完成100%)"
    echo "2. 并行推进ChatGPT评测 (目标: 今日达到80%)"
    echo "3. 社交媒体任务作为独立项目处理"
    echo ""
    echo "⚠️  注意: 任务依赖关系已重建，评测工作不再受社交媒体阻塞!"
}

# 执行主函数
main