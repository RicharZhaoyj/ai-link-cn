# 全方位投资分析系统

🌐 **在线演示**: [ai.link.cn](https://ai.link.cn) | 📁 **GitHub**: [RicharZhaoyj/ai-link-cn](https://github.com/RicharZhaoyj/ai-link-cn)

🚀 **Vercel 自动部署**: 每次推送到 `main` 分支会自动部署到 [ai.link.cn](https://ai.link.cn)

这是一个完整的投资分析系统，支持港股、美股、新加坡股市、基金、ETF、期货和数字货币的分析和监控。

## 系统架构

```
系统包含三个主要模块：

1. **MarketDataCollector** - 市场数据收集器
   - 从yfinance获取股票、ETF、期货、基金数据
   - 从ccxt获取数字货币数据
   - 支持港股、美股、新加坡股市
   - 实时价格、成交量、技术指标计算

2. **MarketMonitor** - 实时监控系统
   - 价格警报：突破买入/卖出价位时报警
   - 技术指标警报：RSI超买/超卖、MACD信号
   - 成交量警报：成交量放大超过50%
   - 市场健康度评分
   - 定时监控（可选每30分钟）

3. **PortfolioOptimizer** - 投资组合优化器
   - 投资组合配置（总投资额、风险级别、市场权重）
   - 相关性分析
   - 回报率计算
   - 风险指标评估
   - 自动优化投资组合权重
   - 图表展示投资组合构成
```

## 安装依赖

```bash
pip install pandas numpy matplotlib yfinance ccxt schedule
```

## 使用方法

### 1. 运行完整分析

```bash
python multi_market_analysis_system.py run
```

这会执行：
- 获取所有市场数据
- 监控市场状态
- 优化投资组合
- 生成综合报告

### 2. 启动实时监控

```bash
python multi_market_analysis_system.py monitor [interval]
```

示例：
```bash
python multi_market_analysis_system.py monitor 30  # 每30分钟监控一次
python multi_market_analysis_system.py monitor 60  # 每60分钟监控一次
```

### 3. 仅运行投资组合优化

```bash
python multi_market_analysis_system.py optimize
```

### 4. 生成每日报告

```bash
python multi_market_analysis_system.py daily
```

### 5. 更新系统配置

```bash
python multi_market_analysis_system.py config total_investment risk_level
```

示例：
```bash
python multi_market_analysis_system.py config 1000000 moderate
python multi_market_analysis_system.py config 500000 conservative
```

## 配置参数

### 总投资额
默认：`$1,000,000`

修改总投资额会影响：
- 每个品种的投资金额
- 价格警报阈值
- 投资组合权重

### 风险级别
- `conservative`（保守型）
  - 单个品种最大权重：10%
  - 最大亏损容忍度：5%
  - 最小相关系数：0.3
  - 再平衡频率：每月

- `moderate`（平衡型）
  - 单个品种最大权重：15%
  - 最大亏损容忍度：10%
  - 最小相关系数：0.2
  - 再平衡频率：每周

- `aggressive`（激进型）
  - 单个品种最大权重：25%
  - 最大亏损容忍度：20%
  - 最小相关系数：0.1
  - 再平衡频率：每天

### 各市场最大权重
默认配置：
- 港股：30%
- 美股：35%
- 新加坡股市：10%
- ETF：15%
- 期货：5%
- 基金：10%
- 数字货币：20%

## 主要功能

### 市场数据收集
支持的市场：
1. **港股** - 主要港股（腾讯、建设银行、汇丰控股等）
2. **美股** - 美股大盘股（苹果、微软、谷歌等）
3. **新加坡股市** - SGX主要股票（DBS、UOB、Singtel等）
4. **ETF** - 主要ETF（SPY、QQQ、VTI等）
5. **期货** - 大宗商品期货（黄金、原油、大豆等）
6. **基金** - Vanguard系列基金（VOO、VGK、VPL等）
7. **数字货币** - 主要加密货币（BTC、ETH、SOL等）

### 技术分析指标
1. **RSI**（相对强度指数）
   - 14天周期
   - RSI < 30：超卖，买入信号
   - RSI > 70：超买，卖出信号

2. **MACD**（移动平均收敛发散）
   - EMA12和EMA26
   - MACD柱状图 > 0：买入信号
   - MACD柱状图 < 0：卖出信号

3. **移动平均线**
   - MA7（7日平均）
   - MA30（30日平均）
   - MA7 > MA30：上涨趋势

4. **布林带**
   - 20日标准差
   - 价格突破上轨：上涨信号
   - 价格跌破下轨：下跌信号

### 监控警报系统

1. **价格警报**
   - 当价格突破预设的买入/卖出价位时报警
   - 示例：
     ```
     BTC/USDT > 75000 → 卖出警报
     BTC/USDT < 65000 → 买入警报
     ```

2. **技术指标警报**
   - RSI低于30（超卖买入）
   - RSI高于70（超买卖出）
   - MACD柱状图转正（买入信号）

3. **成交量警报**
   - 成交量放大超过50%（可能有突破）

### 投资组合优化

1. **评分系统**
   - 回报率评分
   - 技术指标评分
   - 风险调整评分
   - 相关性调整评分

2. **自动优化**
   - 基于评分分配权重
   - 确保不超过市场权重上限
   - 确保不超过单个品种权重上限

3. **风险管理**
   - 止损位设置
   - 仓位管理
   - 分批建仓建议
   - 定期再平衡

## 输出文件

### 市场数据
- `market_data_YYYYMMDD_HHMMSS.json` - 原始市场数据
- `market_report_YYYYMMDD_HHMMSS.txt` - 市场报告

### 监控结果
- `market_alerts_YYYYMMDD.txt` - 警报日志
- `monitor_results_YYYYMMDD_HHMMSS.json` - 监控结果

### 投资组合
- `portfolio_optimization_YYYYMMDD.txt` - 投资组合优化报告
- `portfolio_composition_YYYYMMDD.png` - 投资组合构成图
- `portfolio_weights_YYYYMMDD.png` - 投资组合权重图

### 综合报告
- `comprehensive_report_YYYYMMDD_HHMMSS.txt` - 综合分析报告

## 自定义配置

### 修改市场品种列表
在 `market_data_collector.py` 中修改：
- `self.stock_markets`：股票市场配置
- `self.etf_symbols`：ETF列表
- `self.futures_symbols`：期货列表
- `self.fund_symbols`：基金列表
- `self.crypto_symbols`：数字货币列表

### 修改价格警报阈值
在 `market_monitor.py` 中修改：
- `self.price_alerts_config`：价格警报配置
- `self.alert_thresholds`：技术指标阈值

### 修改投资组合配置
在 `portfolio_optimizer.py` 中修改：
- `self.portfolio_config`：投资组合配置
- `self.risk_params`：风险参数

## 示例运行

```python
# 导入模块
from market_data_collector import MarketDataCollector
from market_monitor import MarketMonitor
from portfolio_optimizer import PortfolioOptimizer

# 数据收集
collector = MarketDataCollector()
all_data = collector.get_all_market_data()

# 实时监控
monitor = MarketMonitor()
monitor.monitor_once()  # 运行一次监控
monitor.start_monitoring(30)  # 每30分钟监控一次

# 投资组合优化
optimizer = PortfolioOptimizer()
portfolio = optimizer.run_optimization()
```

## 注意事项

1. **数据准确性**
   - yfinance API可能延迟或中断
   - ccxt需要API密钥（如果需要交易）
   - 建议使用自己的API密钥提高数据准确性

2. **风险评估**
   - 系统仅提供分析建议，不构成投资建议
   - 实际投资需要综合判断
   - 高风险品种（期货、数字货币）需要谨慎

3. **实时监控**
   - 定时监控会消耗网络资源
   - 建议工作时间使用，避免夜间频繁监控
   - 可以调整监控频率

4. **投资组合调整**
   - 建议定期（每周）重新优化投资组合
   - 根据市场变化调整风险级别
   - 分批建仓降低风险

## 未来扩展

1. **API扩展**
   - 添加更多数据源（东方财富、新浪财经等）
   - 添加实时交易接口
   - 添加更多国际市场（日本、欧洲等）

2. **策略扩展**
   - 添加机器学习预测
   - 添加更多技术指标
   - 添加基本面分析

3. **自动化交易**
   - 连接交易所API
   - 自动化订单执行
   - 风险管理自动化

## Vercel 部署

本项目已配置 Vercel 自动部署，支持以下功能：

### API 接口
- `GET /api/hello` - 欢迎页面和系统信息
- 更多 API 接口正在开发中...

### 静态页面
- `GET /` - 项目首页
- `GET /index.html` - 项目详细介绍页面

### 自动部署
每次推送到 `main` 分支会自动触发 Vercel 部署，更新 [ai.link.cn](https://ai.link.cn)

### 环境变量
在 Vercel 项目中可配置以下环境变量：
- `PYTHON_VERSION`: Python 版本（默认 3.9）
- `MARKET_API_KEY`: 市场数据 API 密钥（可选）
- `CRYPTO_API_KEY`: 数字货币 API 密钥（可选）

## 联系作者

如果有问题或建议，请联系Richard Zhao。

## 在线资源
- 🌐 **网站**: [ai.link.cn](https://ai.link.cn)
- 📁 **源码**: [github.com/RicharZhaoyj/ai-link-cn](https://github.com/RicharZhaoyj/ai-link-cn)
- 🔗 **API**: [ai.link.cn/api/hello](https://ai.link.cn/api/hello)