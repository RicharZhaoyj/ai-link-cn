#!/bin/bash

echo "🚀 开始监控 AI.link.cn 部署状态"
echo "======================================"
echo "提交时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "提交哈希: daa4857"
echo "======================================"

# 等待Vercel开始部署
echo -n "等待Vercel检测更新..."
sleep 30
echo " 完成"

# 测试网站是否可访问
echo "测试网站可访问性..."
for i in {1..5}; do
    echo -n "尝试 $i: "
    if curl -s -o /dev/null -w "%{http_code}" https://ai.link.cn | grep -q "200"; then
        echo "✅ 网站可访问 (HTTP 200)"
        
        # 检查是否包含新的更新时间功能
        echo "检查更新时间功能..."
        if curl -s https://ai.link.cn | grep -q "update-bar"; then
            echo "✅ 发现新的更新时间功能"
            
            # 获取页面中的时间显示
            echo "提取页面中的时间显示..."
            TIME_DISPLAY=$(curl -s https://ai.link.cn | grep -oP '(?<=id="updateTimeDisplay">)[^<]+' | head -1)
            if [ -n "$TIME_DISPLAY" ]; then
                echo "✅ 时间显示: $TIME_DISPLAY"
            else
                echo "⚠️  未找到时间显示元素"
            fi
        else
            echo "⚠️  未找到更新时间功能，可能还在部署中"
        fi
        break
    else
        echo "⏳ 网站暂时不可访问，等待30秒后重试..."
        sleep 30
    fi
done

echo "======================================"
echo "部署状态监控完成"
echo "建议手动访问 https://ai.link.cn 验证更新"