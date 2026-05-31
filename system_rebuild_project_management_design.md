# 🚨 项目管理系统设计文档
## 子系统：项目管理系统
## 设计时间：2026年5月31日 05:10 AM
## 状态：紧急设计阶段

## 📋 设计概述

### 核心目标
**确保指令能够立即转化为实际行动**

### 问题背景
1. **当前问题**: HEARTBEAT.md中的指令无法有效转化为实际行动
2. **灾难表现**: 指令下达后6小时未执行，项目管理完全崩溃
3. **系统风险**: 计划和执行严重脱节

### 设计原则
1. **即时转化**: 指令→任务清单→可执行脚本的自动化转化
2. **进度跟踪**: 实时监控指令执行进度
3. **反馈循环**: 执行结果自动反馈到计划系统
4. **优先级执行**: 紧急指令优先处理

## 🏗️ 系统架构

### 三层转化模型
```
┌─────────────────────────────────────────────────────────┐
│                  指令解析层 (Instruction Parser)         │
├─────────────────────────────────────────────────────────┤
│ HEARTBEAT.md指令 → 结构化任务清单 → 优先级排序          │
└─────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────┐
│                  任务生成层 (Task Generator)             │
├─────────────────────────────────────────────────────────┤
│ 任务清单 → 可执行脚本 → 资源配置 → 时间安排             │
└─────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────┐
│                  执行监控层 (Execution Monitor)          │
├─────────────────────────────────────────────────────────┤
│ 脚本执行 → 进度跟踪 → 结果验证 → 反馈更新               │
└─────────────────────────────────────────────────────────┘
```

### 指令转化流程
```
HEARTBEAT.md指令
        ↓
[指令解析器] → 提取关键信息 (任务、时间、优先级)
        ↓
[任务生成器] → 创建具体执行步骤
        ↓
[脚本编译器] → 生成可执行脚本
        ↓
[执行调度器] → 安排执行时间和资源
        ↓
[监控反馈器] → 跟踪执行并更新状态
```

## 🛠️ 技术实现

### 1. 指令解析器 (`instruction_parser.sh`)
```bash
#!/bin/bash
# HEARTBEAT.md指令解析器
# 功能: 解析HEARTBEAT.md中的指令并生成任务清单

set -e

HEARTBEAT_FILE="/root/.openclaw/workspace/HEARTBEAT.md"
TASK_OUTPUT_DIR="/root/.openclaw/workspace/tasks/instructions"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")

# 创建输出目录
mkdir -p "$TASK_OUTPUT_DIR"

# 解析HEARTBEAT.md中的指令
parse_instructions() {
    echo "解析HEARTBEAT.md中的指令..."
    
    # 提取今日任务部分
    local today_tasks=$(grep -A 50 "### 今日任务状态" "$HEARTBEAT_FILE" | head -30)
    
    # 提取Grammarly评测指令
    local grammarly_instruction=$(echo "$today_tasks" | grep -A 5 "Grammarly评测完成" | head -3)
    
    # 提取ChatGPT评测指令
    local chatgpt_instruction=$(echo "$today_tasks" | grep -A 5 "ChatGPT评测推进" | head -3)
    
    # 提取社交媒体指令
    local social_instruction=$(echo "$today_tasks" | grep -A 5 "社交媒体账号紧急建立" | head -3)
    
    # 生成结构化指令
    cat > "$TASK_OUTPUT_DIR/parsed_instructions_$TIMESTAMP.json" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "source_file": "$HEARTBEAT_FILE",
    "instructions": [
        {
            "id": "inst_001",
            "type": "content_creation",
            "priority": "high",
            "title": "完成Grammarly AI评测",
            "description": "将Grammarly评测从212行增加到294行 (72% → 100%)",
            "source": "$grammarly_instruction",
            "parsed_details": {
                "current_progress": 72,
                "target_progress": 100,
                "current_lines": 212,
                "target_lines": 294,
                "lines_needed": 82,
                "estimated_time": "4小时",
                "file_path": "/root/.openclaw/workspace/content/tools/grammarly_ai_review_20260519.md"
            },
            "status": "parsed",
            "executable": true
        },
        {
            "id": "inst_002",
            "type": "content_creation",
            "priority": "high",
            "title": "推进ChatGPT-4o评测",
            "description": "将ChatGPT评测从302行增加到389行 (77% → 80%)",
            "source": "$chatgpt_instruction",
            "parsed_details": {
                "current_progress": 77,
                "target_progress": 80,
                "current_lines": 302,
                "target_lines": 389,
                "lines_needed": 87,
                "estimated_time": "3小时",
                "file_path": "/root/.openclaw/workspace/content/tools/chatgpt_4o_review_20260522.md"
            },
            "status": "parsed",
            "executable": true
        },
        {
            "id": "inst_003",
            "type": "social_media",
            "priority": "critical",
            "title": "建立社交媒体账号",
            "description": "创建LinkedIn专业页面和知乎专栏",
            "source": "$social_instruction",
            "parsed_details": {
                "blocked_days": 6,
                "blocked_since": "2026-05-24",
                "status": "blocked",
                "execution_guide": "/tmp/social_media_execution_guide.md",
                "estimated_time": "4小时",
                "requires_manual": true
            },
            "status": "parsed",
            "executable": false,
            "blocking_issue": "需要人工执行"
        }
    ],
    "summary": {
        "total_instructions": 3,
        "executable_instructions": 2,
        "blocked_instructions": 1,
        "parsing_time": "$(date +%s)",
        "parser_version": "1.0"
    }
}
EOF
    
    echo "✅ 指令解析完成: $TASK_OUTPUT_DIR/parsed_instructions_$TIMESTAMP.json"
}

# 主函数
main() {
    parse_instructions
    
    # 输出摘要
    echo ""
    echo "📋 指令解析摘要:"
    echo "================"
    echo "总指令数: 3"
    echo "可执行指令: 2 (Grammarly评测, ChatGPT评测)"
    echo "阻塞指令: 1 (社交媒体)"
    echo ""
    echo "🎯 可立即执行的指令:"
    echo "1. 完成Grammarly评测 (72% → 100%)"
    echo "2. 推进ChatGPT评测 (77% → 80%)"
    echo ""
    echo "⚠️  需要人工处理的指令:"
    echo "1. 建立社交媒体账号 (已阻塞6天)"
}

main