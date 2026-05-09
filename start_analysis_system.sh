#!/bin/bash
# 全方位投资分析系统启动脚本

echo "=== 全方位投资分析系统 ==="
echo "选择操作模式："

echo "1. 运行完整分析"
echo "2. 启动实时监控"
echo "3. 优化投资组合"
echo "4. 生成每日报告"
echo "5. 更新系统配置"
echo "6. 测试系统功能"

read -p "请输入选项 (1-6): " choice

case $choice in
    1)
        echo "运行完整分析..."
        python3 multi_market_analysis_system.py run
        ;;
    2)
        read -p "请输入监控间隔分钟数 (默认30): " interval
        if [ -z "$interval" ]; then
            interval=30
        fi
        echo "启动实时监控，每$interval分钟监控一次..."
        python3 multi_market_analysis_system.py monitor $interval
        ;;
    3)
        echo "优化投资组合..."
        python3 multi_market_analysis_system.py optimize
        ;;
    4)
        echo "生成每日报告..."
        python3 multi_market_analysis_system.py daily
        ;;
    5)
        read -p "请输入总投资额 (默认1000000): " investment
        if [ -z "$investment" ]; then
            investment=1000000
        fi
        
        echo "1. conservative (保守)"
        echo "2. moderate (平衡)"
        echo "3. aggressive (激进)"
        read -p "请输入风险级别 (1-3): " risk_input
        
        case $risk_input in
            1)
                risk="conservative"
                ;;
            2)
                risk="moderate"
                ;;
            3)
                risk="aggressive"
                ;;
            *)
                risk="moderate"
                ;;
        esac
        
        echo "更新配置：总投资额 ${investment}, 风险级别 ${risk}"
        python3 multi_market_analysis_system.py config $investment $risk
        ;;
    6)
        echo "测试系统功能..."
        python3 simple_test.py
        ;;
    *)
        echo "无效选项"
        ;;
esac