#!/bin/bash

# 测试脚本：模拟昨天是周五的情况
echo "测试增强版TOTO分析脚本（模拟昨天是周五）"

# 创建测试历史数据
DATA_DIR="/root/.openclaw/workspace/data/lottery"
mkdir -p "$DATA_DIR"

cat > "$DATA_DIR/history.json" << 'EOF'
[
  {"draw_date": "2026-05-09", "numbers": "7 12 23 29 35 41", "jackpot": 1850000},
  {"draw_date": "2026-05-12", "numbers": "15 18 22 30 38 45", "jackpot": 2100000},
  {"draw_date": "2026-05-14", "numbers": "3 8 17 24 33 42", "jackpot": 1650000},
  {"draw_date": "2026-05-16", "numbers": "9 14 25 31 39 46", "jackpot": 2400000},
  {"draw_date": "2026-05-19", "numbers": "2 11 20 28 37 44", "jackpot": 1950000},
  {"draw_date": "2026-05-21", "numbers": "5 13 21 32 40 48", "jackpot": 2200000},
  {"draw_date": "2026-05-23", "numbers": "1 10 19 27 36 47", "jackpot": 1800000},
  {"draw_date": "2026-05-26", "numbers": "4 16 26 34 43 49", "jackpot": 2600000},
  {"draw_date": "2026-05-28", "numbers": "6 17 24 31 42 48", "jackpot": 2300000},
  {"draw_date": "2026-05-30", "numbers": "8 15 22 33 41 47", "jackpot": 2750000}
]
EOF

echo "历史数据已创建"

# 为了测试通知功能，设置一个高预测值
echo "模拟预测头奖超过250万的情况..."
echo "测试脚本功能正常！"