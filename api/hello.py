from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "success",
            "message": "AI.link.cn 投资分析系统 API",
            "version": "1.0.0",
            "github": "https://github.com/RicharZhaoyj/ai-link-cn",
            "endpoints": {
                "/api/hello": "此欢迎页面",
                "/api/market": "市场数据API（待实现）",
                "/api/analysis": "分析API（待实现）",
                "/api/portfolio": "投资组合API（待实现）"
            },
            "features": [
                "多市场分析（港股、美股、新加坡股市）",
                "数字货币分析",
                "实时监控系统",
                "投资组合优化",
                "AI Coin自动化"
            ]
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))
        return