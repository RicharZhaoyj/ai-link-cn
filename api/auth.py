import json
import time
import hashlib
import secrets
from http.server import BaseHTTPRequestHandler

# 简单的内存数据库（实际应用中应该用Redis或数据库）
users_db = {
    "demo@example.com": {
        "password_hash": hashlib.sha256("demo123".encode()).hexdigest(),
        "subscription": "free",
        "created_at": time.time(),
        "api_calls_today": 0,
        "max_daily_calls": 10
    }
}

sessions = {}

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "无效的JSON数据"}).encode())
            return
        
        if self.path == '/api/auth/register':
            self.register(data)
        elif self.path == '/api/auth/login':
            self.login(data)
        elif self.path == '/api/auth/logout':
            self.logout(data)
        elif self.path == '/api/auth/status':
            self.auth_status(data)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "API路径不存在"}).encode())
    
    def do_GET(self):
        if self.path == '/api/auth/plans':
            self.get_subscription_plans()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "API路径不存在"}).encode())
    
    def register(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "邮箱和密码不能为空"}).encode())
            return
        
        if email in users_db:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "邮箱已注册"}).encode())
            return
        
        # 创建用户
        users_db[email] = {
            "password_hash": hashlib.sha256(password.encode()).hexdigest(),
            "subscription": "free",
            "created_at": time.time(),
            "api_calls_today": 0,
            "max_daily_calls": 10,
            "email": email
        }
        
        self._set_headers(201)
        response = {
            "success": True,
            "message": "注册成功",
            "user": {
                "email": email,
                "subscription": "free",
                "created_at": users_db[email]["created_at"]
            }
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
    
    def login(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "邮箱和密码不能为空"}).encode())
            return
        
        user = users_db.get(email)
        if not user:
            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "用户不存在"}).encode())
            return
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user["password_hash"] != password_hash:
            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "密码错误"}).encode())
            return
        
        # 创建会话
        session_token = secrets.token_hex(32)
        sessions[session_token] = {
            "email": email,
            "created_at": time.time(),
            "expires_at": time.time() + 86400  # 24小时
        }
        
        self._set_headers(200)
        response = {
            "success": True,
            "message": "登录成功",
            "session_token": session_token,
            "user": {
                "email": email,
                "subscription": user["subscription"],
                "api_calls_remaining": user["max_daily_calls"] - user["api_calls_today"]
            }
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
    
    def logout(self, data):
        session_token = data.get('session_token')
        
        if session_token in sessions:
            del sessions[session_token]
        
        self._set_headers(200)
        self.wfile.write(json.dumps({"success": True, "message": "登出成功"}).encode())
    
    def auth_status(self, data):
        session_token = data.get('session_token')
        
        if not session_token or session_token not in sessions:
            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "未认证"}).encode())
            return
        
        session = sessions[session_token]
        if time.time() > session["expires_at"]:
            del sessions[session_token]
            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "会话已过期"}).encode())
            return
        
        email = session["email"]
        user = users_db.get(email, {})
        
        self._set_headers(200)
        response = {
            "authenticated": True,
            "user": {
                "email": email,
                "subscription": user.get("subscription", "free"),
                "api_calls_today": user.get("api_calls_today", 0),
                "max_daily_calls": user.get("max_daily_calls", 10),
                "api_calls_remaining": user.get("max_daily_calls", 10) - user.get("api_calls_today", 0)
            }
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
    
    def get_subscription_plans(self):
        plans = {
            "free": {
                "name": "免费版",
                "price": 0,
                "currency": "CNY",
                "features": [
                    "每日10次API调用",
                    "基础市场数据",
                    "延迟15分钟",
                    "基础技术指标"
                ],
                "limits": {
                    "daily_api_calls": 10,
                    "data_delay": 15,  # 分钟
                    "historical_data_days": 30
                }
            },
            "pro": {
                "name": "专业版",
                "price": 99,
                "currency": "CNY",
                "features": [
                    "每日1000次API调用",
                    "实时数据（<1分钟延迟）",
                    "高级技术指标",
                    "投资组合优化",
                    "邮件警报",
                    "API访问"
                ],
                "limits": {
                    "daily_api_calls": 1000,
                    "data_delay": 1,  # 分钟
                    "historical_data_days": 365
                }
            },
            "business": {
                "name": "商业版",
                "price": 999,
                "currency": "CNY",
                "features": [
                    "无限API调用",
                    "毫秒级实时数据",
                    "自定义算法策略",
                    "白标解决方案",
                    "优先技术支持",
                    "私有部署选项"
                ],
                "limits": {
                    "daily_api_calls": 1000000,
                    "data_delay": 0.1,  # 秒
                    "historical_data_days": 9999
                }
            }
        }
        
        self._set_headers(200)
        self.wfile.write(json.dumps({"plans": plans}, ensure_ascii=False).encode())