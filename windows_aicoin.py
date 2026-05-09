#!/usr/bin/env python3
"""
Windows 10上的AiCoin自动化脚本
需要在Windows电脑上安装Python和PyAutoGUI
"""

import pyautogui
import time
import subprocess
import os

def open_aicoin():
    """打开或激活AiCoin"""
    print("正在查找AiCoin窗口...")
    
    # 获取所有窗口
    all_windows = pyautogui.getAllWindows()
    print(f"发现 {len(all_windows)} 个窗口")
    
    # 查找AiCoin窗口
    aicoin_window = None
    for window in all_windows:
        title = window.title
        if title:
            if "AiCoin" in title or "AI Coin" in title or "aicoin" in title.lower():
                print(f"找到AiCoin窗口: '{title}'")
                aicoin_window = window
                break
    
    if aicoin_window:
        print("激活AiCoin窗口...")
        aicoin_window.activate()
        time.sleep(1)
        return True
    else:
        print("未找到AiCoin窗口，尝试启动程序...")
        
        # 可能的AiCoin启动路径
        possible_paths = [
            r"C:\Program Files\AiCoin\AiCoin.exe",
            r"C:\Program Files (x86)\AiCoin\AiCoin.exe",
            r"%LOCALAPPDATA%\AiCoin\AiCoin.exe",
            r"%APPDATA%\AiCoin\AiCoin.exe",
            r"%USERPROFILE%\Desktop\AiCoin.exe",
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                print(f"找到AiCoin: {expanded_path}")
                subprocess.Popen([expanded_path])
                print("AiCoin已启动，等待程序打开...")
                time.sleep(3)
                return True
        
        print("AiCoin未找到，请手动打开")
        return False

def operate_aicoin():
    """操作AiCoin的基本功能"""
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕尺寸: {screen_width} x {screen_height}")
    
    # 获取鼠标位置
    mouse_x, mouse_y = pyautogui.position()
    print(f"鼠标位置: ({mouse_x}, {mouse_y})")
    
    # 尝试操作AiCoin
    success = open_aicoin()
    if not success:
        return
    
    print("AiCoin已打开，可以执行以下操作:")
    
    # 示例操作：截图
    screenshot = pyautogui.screenshot()
    screenshot.save("aicoin_screenshot.png")
    print(f"截图保存为: aicoin_screenshot.png")
    
    # 示例操作：移动到屏幕中心并点击
    center_x = screen_width // 2
    center_y = screen_height // 2
    pyautogui.moveTo(center_x, center_y, duration=0.5)
    print(f"移动鼠标到屏幕中心: ({center_x}, {center_y})")
    
    # 示例操作：双击
    pyautogui.doubleClick()
    print("双击执行")
    
    # 示例操作：键盘输入
    time.sleep(1)
    pyautogui.write("BTC")
    print("输入了: BTC")
    
    # 示例操作：快捷键
    time.sleep(1)
    pyautogui.hotkey('ctrl', 's')  # 保存
    print("执行快捷键: Ctrl+S")
    
    print("基础操作完成")

def crypto_operations():
    """加密货币交易相关操作"""
    print("加密货币交易操作示例:")
    
    # 1. 选择交易品种
    pyautogui.write("BTC/USDT")
    pyautogui.press('enter')
    time.sleep(1)
    
    # 2. 买入操作示例
    pyautogui.write("100")  # 输入数量
    pyautogui.press('tab')
    pyautogui.write("50000")  # 输入价格
    pyautogui.press('tab')
    pyautogui.write("BUY")  # 选择买入
    pyautogui.press('enter')
    print("买入操作示例完成")
    
    # 3. 卖出操作示例
    time.sleep(2)
    pyautogui.write("50")  # 输入数量
    pyautogui.press('tab')
    pyautogui.write("51000")  # 输入价格
    pyautogui.press('tab')
    pyautogui.write("SELL")  # 选择卖出
    pyautogui.press('enter')
    print("卖出操作示例完成")

def main():
    """主程序"""
    print("=== AiCoin加密货币交易自动化脚本 ===")
    print("适用于Windows 10系统")
    print("请确保:")
    print("1. AiCoin程序已安装")
    print("2. Python已安装 (pip install pyautogui)")
    print("3. 运行前关闭其他干扰程序")
    print("")
    
    # 安全检查
    pyautogui.FAILSAFE = True
    print("安全模式已启用：将鼠标移动到角落可中断程序")
    
    try:
        # 基础操作
        operate_aicoin()
        
        # 加密货币操作（可选）
        crypto_operations()
        
        print("\n脚本执行完成！")
        print("注意：实际交易请谨慎操作")
        
    except Exception as e:
        print(f"发生错误: {e}")
        print("请检查环境配置")

if __name__ == "__main__":
    main()

# 安装说明
print("\n==== 安装指南 ====")
print("在Windows 10上安装Python和PyAutoGUI:")
print("")
print("1. 安装Python:")
print("   - 访问 https://www.python.org/downloads/")
print("   - 下载Python 3.x")
print("   - 安装时勾选 'Add Python to PATH'")
print("")
print("2. 安装PyAutoGUI:")
print("   - 打开命令提示符或PowerShell")
print("   - 运行: pip install pyautogui")
print("")
print("3. 运行脚本:")
print("   - 保存此脚本为 windows_aicoin.py")
print("   - 打开命令提示符")
print("   - 运行: python windows_aicoin.py")
print("")
print("4. 定制脚本:")
print("   - 根据你的AiCoin界面调整坐标")
print("   - 添加更多交易逻辑")