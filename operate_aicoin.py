#!/usr/bin/env python3
"""
操作AiCoin桌面程序
"""

import sys
import os

# 设置DISPLAY环境变量连接到本地GUI
os.environ['DISPLAY'] = ':0'

# 导入桌面控制技能
skill_path = os.path.join(os.path.expanduser("~/.openclaw/workspace"), "skills/desktop-control")
sys.path.insert(0, skill_path)

try:
    from __init__ import DesktopController
    print("Desktop Controller导入成功")
except ImportError as e:
    print(f"导入失败: {e}")
    print("需要安装PyAutoGUI等依赖")
    sys.exit(1)

# 初始化控制器
dc = DesktopController(failsafe=True)

print(f"屏幕分辨率: {dc.get_screen_size()}")
print(f"鼠标当前位置: {dc.get_mouse_position()}")

# 查找AiCoin窗口
windows = dc.get_all_windows()
print(f"当前打开的窗口数量: {len(windows)}")

# 查找AiCoin窗口
aicoin_window = None
for window_title in windows:
    if window_title:
        if "AiCoin" in window_title or "AI Coin" in window_title or "aicoin" in window_title.lower():
            print(f"找到AiCoin窗口: {window_title}")
            aicoin_window = window_title
            break

if aicoin_window:
    # 激活AiCoin窗口
    success = dc.activate_window(aicoin_window)
    if success:
        print(f"已激活AiCoin窗口: {aicoin_window}")
        
        # 等待程序响应
        import time
        time.sleep(1)
        
        # 现在你可以执行操作，比如：
        # 1. 点击某些按钮
        # 2. 输入文本
        # 3. 截图
        
        print("AiCoin窗口已激活，可以进行后续操作")
    else:
        print("无法激活AiCoin窗口")
else:
    print("没有找到AiCoin窗口")
    print("正在尝试在窗口列表中查找:")
    for i, title in enumerate(windows):
        if title:  # 过滤空标题
            print(f"  [{i+1}] {title}")
    
    print("\n请告诉我AiCoin窗口的标题是什么？或者窗口列表中哪一个可能是AiCoin？")
    
    # 尝试一些常见的窗口操作
    # 获取当前活动窗口
    active_window = dc.get_active_window()
    if active_window:
        print(f"当前活动窗口: {active_window}")
        
        # 截图当前窗口
        try:
            screenshot = dc.screenshot(filename="/tmp/current_window.png")
            print(f"已截图保存到: /tmp/current_window.png")
        except Exception as e:
            print(f"截图失败: {e}")

# 提供一些有用的功能
print("\n可用的操作:")
print("1. dc.move_mouse(x, y) - 移动鼠标")
print("2. dc.click(x, y) - 点击")
print("3. dc.type_text('text') - 输入文本")
print("4. dc.hotkey('ctrl', 'c') - 快捷键")
print("5. dc.screenshot(filename='screenshot.png') - 截图")
print("6. dc.get_all_windows() - 获取所有窗口列表")
print("7. dc.activate_window('窗口标题') - 激活窗口")