# QUICK_START.md - 全方位投资分析系统快速开始指南

## 系统概述

这是一个整合了港股、美股、新加坡股市、基金、ETF、期货和数字货币分析的完整系统。基于Richard Zhao现有的AI Coin自动化架构扩展而来。

## 快速开始

### 1. 安装依赖

```bash
# 使用已有的虚拟环境
source venv/bin/activate
```

### 2. 测试系统

```bash
python3 simple_test.py
```

### 3. 运行完整分析

```bash
python3 multi_market_analysis_system.py run
```

这会执行：
- 获取所有市场数据
- 监控市场状态
- 优化投资组合
- 生成综合报告

### 4. 使用启动脚本

```bash
./start_analysis_system.sh
```

## 核心功能说明

### **数据源**

1. **港股** - yfinance API
   - 腾讯控股 (00700.HK)
   - 建设银行 (00939.HK)
   - 汇丰控股 (00005.HK)
   - 盈富基金 (02800.HK)

2. **美股** - yfinance API
   - 苹果 (AAPL)
   - 微软 (MSFT)
   - 谷歌 (GOOGL)
   - 亚马逊 (AMZN)

3. **新加坡股市** - yfinance API
   - DBS Bank (D05.SI)
   - UOB Bank (U11.SI)
   - Singtel (Z74.SI)

4. **ETF** - yfinance API
   - SPDR S&P 500 ETF (SPY)
   - Invesco QQQ ETF (QQQ)
   - Vanguard Total Stock Market ETF (VTI)

5. **期货** - yfinance API
   - 黄金期货 (GC=F)
   - 原油期货 (CL=F)

6. **基金** - yfinance API
   - Vanguard S&P 500 ETF (VOO)
   - Vanguard FTSE Europe ETF (VGK)

7. **数字货币** - ccxt API
   - 比特币 (BTC/USDT)
   - 以太坊 (ETH/USDT)
   - Solana (SOL/USDT)

### **技术分析**

系统为每个品种计算：
- **RSI** - 相对强度指数，判断超买超卖
- **MACD** - 移动平均收敛发散，趋势判断
- **移动平均线** - MA7和MA30，趋势分析
- **布林带** - 价格突破分析
- **成交量** - 成交量变化分析

### **投资建议**

基于以下生成投资建议：
1. **技术指标评分** - RSI/MACD信号
2. **回报率评分** - 7天/30天回报率
3. **风险评分** - 波动率和相关性
4. **市场健康度** - 市场整体评分

### **风险管理**

不同市场的止损位：
- 港股/美股: 10%
- ETF/基金: 8%
- 期货: 15%
- 数字货币: 20%

## 个性化调整

### 修改品种列表

编辑 `market_data_collector.py`:
- `self.stock_markets['hk']['symbols']` - 港股
- `self.stock_markets['us']['symbols']` - 美股
- `self.stock_markets['sg']['symbols']` - 新加坡
- `self.etf_symbols` - ETF
- `self.futures_symbols` - 期货
- `self.fund_symbols` - 基金
- `self.crypto_symbols` - 数字货币

### 修改投资参数

编辑 `portfolio_optimizer.py`:
- `self.portfolio_config['total_investment']` - 总投资额
- `self.portfolio_config['risk_level']` - 风险级别
- `self.portfolio_config['asset_classes']` - 市场权重
- `self.risk_params` - 风险参数

### 修改警报阈值

编辑 `market_monitor.py`:
- `self.alert_thresholds` - 技术指标阈值
- `self.price_alerts_config` - 价格警报配置

## 自动化监控

系统支持定时监控，可以设置：
- **实时监控**: 每30分钟检查市场状态
- **价格警报**: 突破预设价位自动警报
- **技术警报**: RSI/MACD异常自动警报
- **成交量警报**: 成交量放大自动警报

```bash
python3 multi_market_analysis_system.py monitor 30
```

## 输出文件

系统会自动生成以下文件：
1. **market_report_YYYYMMDD_HHMMSS.txt** - 市场分析报告
2. **portfolio_optimization_YYYYMMDD.txt** - 投资组合优化报告
3. **portfolio_composition_YYYYMMDD.png** - 投资组合构成图
4. **portfolio_weights_YYYYMMDD.png** - 投资组合权重图
5. **market_alerts_YYYYMMDD.txt** - 市场警报日志

## 故障排除

### API限制问题

如果出现 "Too Many Requests"，可能是因为yfinance API调用频率过高。解决方案：
1. 减少品种数量
2. 增加数据获取间隔
3. 使用付费API版本

### 数字货币数据问题

数字货币数据需要ccxt API密钥。如果没有密钥，可以：
1. 使用模拟数据（已内置）
2. 注册Binance等交易所API
3. 调整系统使用其他数据源

### 图表生成问题

如果图表生成失败，可能是因为matplotlib配置问题。解决方案：
1. 确保安装了matplotlib
2. 检查Python版本兼容性
3. 可能需要安装tkinter: `apt-get install python3-tk`

## 与现有系统的整合

你的现有AI Coin自动化脚本可以与这个系统整合：
1. **数据共享** - 使用相同的数据源
2. **技术指标一致** - 使用相同的RSI/MACD算法
3. **报告整合** - 可以将数字货币分析整合到综合报告中

## 下一步

1. **运行一次完整分析**，查看输出
2. **调整品种列表**，加入你关注的股票
3. **设置价格警报**，针对你的投资品种
4. **测试自动化监控**，每30分钟运行一次
5. **优化投资组合**，基于你的风险偏好

## 技术支持

如果遇到任何问题，可以查看：
- README.md - 详细文档
- market_data_collector.py - 数据获取源码
- portfolio_optimizer.py - 投资组合源码
- multi_market_analysis_system.py - 主系统源码

系统已经为你配置了默认参数，可以直接使用。如果需要调整，随时告诉我。