"""
AiCoin自动化配置文件
根据你的AiCoin界面调整这些坐标
"""

# 默认坐标（可能需要调整）
coordinates = {
    # 主窗口位置
    "window_top": (100, 100),        # 窗口左上角
    "window_center": (800, 450),      # 窗口中心
    
    # 菜单栏
    "menu_market": (100, 50),         # 行情选项卡
    "menu_trade": (200, 50),          # 交易选项卡
    "menu_account": (300, 50),        # 账户选项卡
    "menu_settings": (400, 50),       # 设置选项卡
    
    # 搜索框
    "search_box": (500, 100),         # 搜索框
    "search_button": (700, 100),      # 搜索按钮
    
    # 技术指标
    "tech_indicator": (300, 200),     # 技术指标按钮
    "ma_button": (350, 250),          # MA按钮
    "rsi_button": (400, 250),         # RSI按钮
    "macd_button": (450, 250),        # MACD按钮
    "bb_button": (500, 250),          # BB按钮
    
    # 图表操作
    "chart_zoom": (800, 300),         # 图表放大
    "chart_reset": (850, 300),        # 图表重置
    "chart_time": (900, 300),         # 时间周期
    
    # 价格警报
    "alert_button": (600, 50),        # 警报按钮
    "alert_create": (650, 100),       # 创建警报
    "alert_buy": (700, 150),          # 买入警报
    "alert_sell": (750, 150),         # 卖出警报
    
    # 交易操作
    "trade_buy": (500, 400),          # 买入按钮
    "trade_sell": (550, 400),         # 卖出按钮
    "trade_amount": (600, 400),       # 数量输入
    "trade_price": (650, 400),        # 价格输入
    "trade_submit": (700, 400),       # 提交按钮
    
    # 其他功能
    "export_button": (900, 50),       # 导出按钮
    "screenshot_button": (950, 50),    # 截图按钮
    "help_button": (1000, 50),        # 帮助按钮
}

# 颜色和识别模式（可选）
colors = {
    "market_tab": (255, 0, 0),        # 行情选项卡颜色
    "search_box": (255, 255, 255),     # 搜索框颜色
    "button_active": (0, 255, 0),     # 按钮激活颜色
    "button_disabled": (128, 128, 128), # 按钮禁用颜色
}

# 等待时间配置
timing = {
    "window_open": 3,                  # 窗口打开时间
    "search_wait": 2,                  # 搜索等待时间
    "chart_load": 3,                   # 图表加载时间
    "alert_set": 1,                    # 警报设置时间
    "trade_complete": 2,               # 交易完成时间
}

# AiCoin相关配置
aicoin_config = {
    "default_crypto": "BTC/USDT",      # 默认加密货币
    "secondary_crypto": "ETH/USDT",    # 第二加密货币
    "alert_thresholds": {
        "btc_buy": 65000,              # BTC买入价格
        "btc_sell": 75000,             # BTC卖出价格
        "eth_buy": 3500,               # ETH买入价格
        "eth_sell": 4200,              # ETH卖出价格
    },
    "technical_indices": ["MA", "RSI", "MACD", "BB"], # 技术指标列表
    "chart_types": ["Line", "Candle", "Bar"],         # 图表类型列表
    "time_frames": ["1D", "1W", "1M"],                # 时间周期列表
}

# 调试模式
debug = True

def get_coordinate(key):
    """获取坐标"""
    return coordinates[key]

def get_color(key):
    """获取颜色"""
    return colors[key]

def get_timing(key):
    """获取等待时间"""
    return timing[key]

def get_config(key):
    """获取配置"""
    return aicoin_config[key]

# 示例使用方法
if __name__ == "__main__":
    print("AiCoin配置文件")
    print(f"行情选项卡坐标: {get_coordinate('menu_market')}")
    print(f"默认加密货币: {get_config('default_crypto')}")
    print(f"BTC买入价格: {get_config('alert_thresholds')['btc_buy']}")
    print(f"技术指标: {get_config('technical_indices')}")
    
    # 调试信息
    if debug:
        print("调试模式: 开启")
        print("坐标数据:")
        for key, pos in coordinates.items():
            print(f"  {key}: {pos}")
    
    print("\n=== 修改说明 ===")
    print("1. 运行 coordinate_calibration.py 校准坐标")
    print("2. 更新本文件中的坐标")
    print("3. 使用 calibrate() 函数获取精确坐标")