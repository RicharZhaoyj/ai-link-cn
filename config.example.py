# 全方位投资分析系统配置示例

# API 配置（如果需要）
CRYPTO_EXCHANGE_API = {
    'binance': {
        'api_key': 'YOUR_API_KEY_HERE',
        'api_secret': 'YOUR_API_SECRET_HERE',
    },
    'okx': {
        'api_key': 'YOUR_API_KEY_HERE',
        'api_secret': 'YOUR_API_SECRET_HERE',
        'password': 'YOUR_API_PASSWORD_HERE',
    }
}

# 投资组合配置
PORTFOLIO_CONFIG = {
    'total_investment': 1000000,  # 总投资额（人民币）
    'risk_level': 'moderate',     # 风险级别：conservative/moderate/aggressive
    
    # 各市场最大权重（百分比）
    'market_weights': {
        'hk_stocks': 30,   # 港股
        'us_stocks': 35,   # 美股
        'sg_stocks': 10,   # 新加坡股市
        'etf': 15,         # ETF
        'futures': 5,      # 期货
        'funds': 10,       # 基金
        'crypto': 20,      # 数字货币
    },
    
    # 单个品种最大权重
    'max_symbol_weight': 15,  # 单个品种最大权重百分比
}

# 监控配置
MONITOR_CONFIG = {
    'check_interval': 30,      # 监控间隔（分钟）
    'price_alert_threshold': 3,  # 价格警报阈值（百分比）
    'volume_alert_threshold': 50, # 成交量警报阈值（百分比）
    
    # 技术指标阈值
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    'macd_signal_period': 9,
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',           # 日志级别：DEBUG/INFO/WARNING/ERROR
    'file_path': './logs/analysis.log',
    'max_file_size': 10485760,  # 10MB
    'backup_count': 5,          # 保留5个备份文件
}