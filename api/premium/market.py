import json
import time
from http.server import BaseHTTPRequestHandler
import yfinance as yf
import pandas as pd

# 导入认证模块的功能
try:
    from ..auth import sessions, users_db
except ImportError:
    # 简化版本，实际应用中应该正确导入
    sessions = {}
    users_db = {}

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def _check_auth(self):
        """检查用户认证和订阅状态"""
        auth_header = self.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None, {"error": "需要认证令牌"}
        
        session_token = auth_header.split(' ')[1]
        
        # 检查会话
        if session_token not in sessions:
            return None, {"error": "会话无效或已过期"}
        
        session = sessions[session_token]
        if time.time() > session.get('expires_at', 0):
            return None, {"error": "会话已过期"}
        
        email = session['email']
        user = users_db.get(email)
        
        if not user:
            return None, {"error": "用户不存在"}
        
        # 检查API调用限制
        if user.get('api_calls_today', 0) >= user.get('max_daily_calls', 10):
            return None, {"error": "今日API调用次数已用完"}
        
        # 更新API调用计数
        user['api_calls_today'] = user.get('api_calls_today', 0) + 1
        
        return user, None
    
    def _check_subscription(self, user, required_plan='free'):
        """检查用户订阅等级"""
        plan_levels = {'free': 0, 'pro': 1, 'business': 2}
        
        user_plan = user.get('subscription', 'free')
        user_level = plan_levels.get(user_plan, 0)
        required_level = plan_levels.get(required_plan, 0)
        
        if user_level < required_level:
            return False, f"需要{required_plan}订阅，当前为{user_plan}"
        
        return True, None
    
    def do_GET(self):
        # 认证检查
        user, auth_error = self._check_auth()
        if auth_error:
            self._set_headers(401)
            self.wfile.write(json.dumps(auth_error).encode())
            return
        
        if self.path == '/api/premium/market/real-time':
            self.get_real_time_data(user)
        elif self.path == '/api/premium/market/historical':
            self.get_historical_data(user)
        elif self.path == '/api/premium/market/analysis':
            self.get_market_analysis(user)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "API路径不存在"}).encode())
    
    def get_real_time_data(self, user):
        """获取实时市场数据（需要pro订阅）"""
        # 检查订阅等级
        allowed, error_msg = self._check_subscription(user, 'pro')
        if not allowed:
            self._set_headers(402)
            self.wfile.write(json.dumps({
                "error": "订阅等级不足",
                "message": error_msg,
                "upgrade_url": "/pricing"
            }).encode())
            return
        
        # 获取查询参数
        import urllib.parse
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        symbol = params.get('symbol', ['BTC-USD'])[0]
        
        try:
            # 使用yfinance获取数据
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 获取最新价格
            hist = ticker.history(period='1d')
            
            if hist.empty:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "未找到该交易对数据"}).encode())
                return
            
            latest = hist.iloc[-1]
            
            response = {
                "symbol": symbol,
                "timestamp": time.time(),
                "data": {
                    "price": float(latest['Close']),
                    "open": float(latest['Open']),
                    "high": float(latest['High']),
                    "low": float(latest['Low']),
                    "volume": int(latest['Volume']),
                    "change": float(latest['Close'] - latest['Open']),
                    "change_percent": float((latest['Close'] - latest['Open']) / latest['Open'] * 100)
                },
                "info": {
                    "name": info.get('longName', symbol),
                    "currency": info.get('currency', 'USD'),
                    "market": info.get('market', 'Unknown'),
                    "timezone": info.get('exchangeTimezoneName', 'UTC')
                },
                "user_limits": {
                    "api_calls_today": user.get('api_calls_today', 0),
                    "max_daily_calls": user.get('max_daily_calls', 10),
                    "remaining_calls": user.get('max_daily_calls', 10) - user.get('api_calls_today', 0)
                }
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({
                "error": "获取数据失败",
                "message": str(e)
            }).encode())
    
    def get_historical_data(self, user):
        """获取历史数据（需要pro订阅）"""
        allowed, error_msg = self._check_subscription(user, 'pro')
        if not allowed:
            self._set_headers(402)
            self.wfile.write(json.dumps({
                "error": "订阅等级不足",
                "message": error_msg,
                "upgrade_url": "/pricing"
            }).encode())
            return
        
        import urllib.parse
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        symbol = params.get('symbol', ['BTC-USD'])[0]
        period = params.get('period', ['1mo'])[0]  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval = params.get('interval', ['1d'])[0]  # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "未找到历史数据"}).encode())
                return
            
            # 转换数据为JSON格式
            data = []
            for idx, row in hist.iterrows():
                data.append({
                    "timestamp": idx.timestamp(),
                    "date": idx.strftime('%Y-%m-%d %H:%M:%S'),
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": int(row['Volume'])
                })
            
            response = {
                "symbol": symbol,
                "period": period,
                "interval": interval,
                "count": len(data),
                "data": data,
                "summary": {
                    "start_date": hist.index[0].strftime('%Y-%m-%d'),
                    "end_date": hist.index[-1].strftime('%Y-%m-%d'),
                    "price_change": float(hist['Close'].iloc[-1] - hist['Close'].iloc[0]),
                    "price_change_percent": float((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100),
                    "average_volume": int(hist['Volume'].mean())
                }
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({
                "error": "获取历史数据失败",
                "message": str(e)
            }).encode())
    
    def get_market_analysis(self, user):
        """获取市场分析（需要business订阅）"""
        allowed, error_msg = self._check_subscription(user, 'business')
        if not allowed:
            self._set_headers(402)
            self.wfile.write(json.dumps({
                "error": "订阅等级不足",
                "message": error_msg,
                "upgrade_url": "/pricing"
            }).encode())
            return
        
        import urllib.parse
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        symbol = params.get('symbol', ['BTC-USD'])[0]
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='6mo')
            
            if hist.empty:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "未找到足够的历史数据进行分析"}).encode())
                return
            
            # 计算技术指标
            closes = hist['Close']
            
            # RSI计算
            delta = closes.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # 移动平均线
            ma_7 = closes.rolling(window=7).mean()
            ma_30 = closes.rolling(window=30).mean()
            
            # 价格动量
            momentum = (closes.iloc[-1] / closes.iloc[-20] - 1) * 100
            
            # 波动率
            volatility = closes.pct_change().std() * (252 ** 0.5) * 100  # 年化波动率
            
            response = {
                "symbol": symbol,
                "analysis_date": time.strftime('%Y-%m-%d %H:%M:%S'),
                "technical_indicators": {
                    "current_price": float(closes.iloc[-1]),
                    "rsi_14": float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None,
                    "rsi_signal": "超卖" if rsi.iloc[-1] < 30 else "超买" if rsi.iloc[-1] > 70 else "中性",
                    "ma_7": float(ma_7.iloc[-1]) if not pd.isna(ma_7.iloc[-1]) else None,
                    "ma_30": float(ma_30.iloc[-1]) if not pd.isna(ma_30.iloc[-1]) else None,
                    "ma_trend": "上涨" if ma_7.iloc[-1] > ma_30.iloc[-1] else "下跌",
                    "momentum_20d": float(momentum),
                    "volatility_annual": float(volatility)
                },
                "recommendation": {
                    "action": self._generate_recommendation(rsi.iloc[-1], ma_7.iloc[-1], ma_30.iloc[-1]),
                    "confidence": 0.85,
                    "timeframe": "短期(1-4周)",
                    "target_price": float(closes.iloc[-1] * 1.05),  # 示例目标价
                    "stop_loss": float(closes.iloc[-1] * 0.95)     # 示例止损价
                },
                "risk_assessment": {
                    "level": "中等" if volatility < 50 else "高",
                    "score": 65,
                    "factors": ["市场波动性", "流动性风险", "宏观环境"]
                }
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({
                "error": "分析失败",
                "message": str(e)
            }).encode())
    
    def _generate_recommendation(self, rsi, ma_7, ma_30):
        """生成交易建议（简化版本）"""
        if pd.isna(rsi) or pd.isna(ma_7) or pd.isna(ma_30):
            return "观望"
        
        if rsi < 30 and ma_7 > ma_30:
            return "强烈买入"
        elif rsi < 35:
            return "买入"
        elif rsi > 70 and ma_7 < ma_30:
            return "强烈卖出"
        elif rsi > 65:
            return "卖出"
        else:
            return "持有"