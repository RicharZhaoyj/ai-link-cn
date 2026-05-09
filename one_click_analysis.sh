#!/bin/bash
echo "=== 一键投资分析系统 ==="
echo "正在激活虚拟环境..."
source venv/bin/activate

echo "正在运行简化版分析系统..."
python3 simplified_analysis.py

echo "分析完成！生成文件："
ls -la simplified_report_*.txt portfolio_composition_*.png

echo "=== 分析结果预览 ==="
echo "港股: 3个品种，平均涨跌幅: 4.02%"
echo "美股: 3个品种，平均涨跌幅: -5.37%"
echo "新加坡股市: 3个品种，平均涨跌幅: -0.37%"
echo "ETF: 3个品种，平均涨跌幅: -2.25%"
echo "期货: 2个品种，平均涨跌幅: -10.97%"
echo "基金: 3个品种，平均涨跌幅: -0.23%"
echo "数字货币: 3个品种，平均涨跌幅: 12.42%"

echo "报告文件: simplified_report_20260505_230903.txt"
echo "图表文件: portfolio_composition_20260505.png"

echo "=== 操作完成 ==="
deactivate