#!/usr/bin/env python3
"""
AI.link.cn 项目增长监控脚本
自动追踪GitHub stars、网站访问量、用户增长等指标
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path

class GrowthMonitor:
    """增长监控器"""
    
    def __init__(self, db_path="growth_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建增长数据表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS growth_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            source TEXT,
            notes TEXT
        )
        ''')
        
        # 创建每日汇总表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            date DATE PRIMARY KEY,
            github_stars INTEGER DEFAULT 0,
            github_forks INTEGER DEFAULT 0,
            website_visits INTEGER DEFAULT 0,
            api_calls INTEGER DEFAULT 0,
            new_users INTEGER DEFAULT 0,
            active_users INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_metric(self, name, value, source=None, notes=None):
        """追踪单个指标"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO growth_metrics (metric_name, metric_value, source, notes)
        VALUES (?, ?, ?, ?)
        ''', (name, value, source, notes))
        
        conn.commit()
        conn.close()
        
        print(f"[{datetime.now()}] 追踪指标: {name} = {value}")
        return True
    
    def get_github_stats(self):
        """获取GitHub统计数据"""
        try:
            # GitHub API请求
            headers = {
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # 如果有token可以提高速率限制
            github_token = os.getenv('GITHUB_TOKEN')
            if github_token:
                headers['Authorization'] = f'token {github_token}'
            
            repo_url = "https://api.github.com/repos/RicharZhaoyj/ai-link-cn"
            response = requests.get(repo_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # 记录各项指标
                metrics = {
                    'github_stars': data.get('stargazers_count', 0),
                    'github_forks': data.get('forks_count', 0),
                    'github_watchers': data.get('watchers_count', 0),
                    'github_open_issues': data.get('open_issues_count', 0),
                    'github_size_kb': data.get('size', 0),
                    'github_last_push': data.get('pushed_at', '')
                }
                
                for name, value in metrics.items():
                    self.track_metric(name, value, source='github')
                
                return metrics
            else:
                print(f"GitHub API错误: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取GitHub数据失败: {e}")
            return None
    
    def get_website_analytics(self):
        """获取网站分析数据（模拟）"""
        # 实际应用中这里应该接入Google Analytics或Vercel Analytics
        # 这里使用模拟数据
        
        try:
            # 模拟数据 - 实际应该从Vercel API获取
            metrics = {
                'website_visits_today': 150,  # 模拟
                'website_pageviews_today': 450,  # 模拟
                'website_bounce_rate': 0.35,  # 模拟
                'website_avg_session_duration': 180,  # 模拟秒数
            }
            
            for name, value in metrics.items():
                self.track_metric(name, value, source='website')
            
            return metrics
            
        except Exception as e:
            print(f"获取网站数据失败: {e}")
            return None
    
    def get_api_usage(self):
        """获取API使用数据"""
        try:
            # 这里可以从应用日志或数据库中获取实际数据
            # 使用模拟数据
            
            metrics = {
                'api_calls_today': 1200,
                'api_calls_success_rate': 0.98,
                'api_response_time_avg': 150,  # 毫秒
                'api_error_count': 24,
                'api_unique_users': 85,
            }
            
            for name, value in metrics.items():
                self.track_metric(name, value, source='api')
            
            return metrics
            
        except Exception as e:
            print(f"获取API数据失败: {e}")
            return None
    
    def update_daily_summary(self):
        """更新每日汇总数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date().isoformat()
        
        # 获取今日各项指标
        cursor.execute('''
        SELECT 
            SUM(CASE WHEN metric_name = 'github_stars' THEN metric_value ELSE 0 END) as stars,
            SUM(CASE WHEN metric_name = 'github_forks' THEN metric_value ELSE 0 END) as forks,
            SUM(CASE WHEN metric_name = 'website_visits_today' THEN metric_value ELSE 0 END) as visits,
            SUM(CASE WHEN metric_name = 'api_calls_today' THEN metric_value ELSE 0 END) as api_calls,
            SUM(CASE WHEN metric_name = 'api_unique_users' THEN metric_value ELSE 0 END) as active_users
        FROM growth_metrics
        WHERE date(timestamp) = date('now')
        ''')
        
        result = cursor.fetchone()
        
        if result:
            stars, forks, visits, api_calls, active_users = result
            
            # 插入或更新每日汇总
            cursor.execute('''
            INSERT OR REPLACE INTO daily_summary 
            (date, github_stars, github_forks, website_visits, api_calls, active_users)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (today, stars or 0, forks or 0, visits or 0, api_calls or 0, active_users or 0))
        
        conn.commit()
        conn.close()
    
    def generate_daily_report(self):
        """生成每日报告"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取今日数据
        today = datetime.now().date().isoformat()
        cursor.execute('''
        SELECT * FROM daily_summary WHERE date = ?
        ''', (today,))
        
        daily_data = cursor.fetchone()
        
        # 获取历史趋势
        cursor.execute('''
        SELECT date, github_stars, website_visits, api_calls, active_users
        FROM daily_summary 
        ORDER BY date DESC 
        LIMIT 7
        ''')
        
        weekly_data = cursor.fetchall()
        
        conn.close()
        
        # 生成报告
        report = {
            'date': today,
            'timestamp': datetime.now().isoformat(),
            'daily_summary': daily_data,
            'weekly_trend': weekly_data,
            'growth_insights': self._analyze_growth(weekly_data)
        }
        
        # 保存报告到文件
        report_file = f"reports/daily_report_{today}.json"
        os.makedirs("reports", exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 生成文本报告
        text_report = self._format_text_report(report)
        text_report_file = f"reports/daily_report_{today}.txt"
        
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(text_report)
        
        print(f"生成报告: {report_file}")
        print(text_report)
        
        return report
    
    def _analyze_growth(self, weekly_data):
        """分析增长趋势"""
        if len(weekly_data) < 2:
            return {"status": "数据不足", "message": "需要更多数据进行分析"}
        
        # 计算增长率
        insights = {
            "github_stars_growth": 0,
            "website_visits_growth": 0,
            "api_calls_growth": 0,
            "active_users_growth": 0,
            "trend": "stable",
            "recommendations": []
        }
        
        try:
            # 获取第一天和最后一天的数据
            first_day = weekly_data[-1]
            last_day = weekly_data[0]
            
            # 计算各项增长率
            for i, metric in enumerate(['github_stars', 'website_visits', 'api_calls', 'active_users']):
                first_value = first_day[i+1] or 1  # i+1跳过date字段
                last_value = last_day[i+1] or 1
                
                if first_value > 0:
                    growth_rate = ((last_value - first_value) / first_value) * 100
                    insights[f"{metric}_growth"] = round(growth_rate, 2)
            
            # 判断整体趋势
            positive_growths = sum(1 for key in insights if key.endswith('_growth') and insights[key] > 0)
            total_metrics = sum(1 for key in insights if key.endswith('_growth'))
            
            if positive_growths == total_metrics:
                insights["trend"] = "strong_growth"
                insights["recommendations"].append("所有指标都在增长，继续保持当前策略")
            elif positive_growths >= total_metrics / 2:
                insights["trend"] = "moderate_growth"
                insights["recommendations"].append("多数指标在增长，优化表现不佳的方面")
            else:
                insights["trend"] = "needs_attention"
                insights["recommendations"].append("增长放缓，需要重新评估推广策略")
            
            # 根据具体指标给出建议
            if insights.get('website_visits_growth', 0) < 10:
                insights["recommendations"].append("网站访问增长缓慢，考虑增加内容营销")
            
            if insights.get('api_calls_growth', 0) < 5:
                insights["recommendations"].append("API使用增长有限，优化开发者体验")
            
            if insights.get('active_users_growth', 0) < 0:
                insights["recommendations"].append("活跃用户下降，检查用户留存问题")
        
        except Exception as e:
            insights["error"] = str(e)
        
        return insights
    
    def _format_text_report(self, report):
        """格式化文本报告"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"AI.link.cn 每日增长报告 - {report['date']}")
        lines.append("=" * 60)
        lines.append("")
        
        if report['daily_summary']:
            date, stars, forks, visits, api_calls, active_users, created_at = report['daily_summary']
            lines.append("📊 今日关键指标:")
            lines.append(f"  ⭐ GitHub Stars: {stars}")
            lines.append(f"  🍴 GitHub Forks: {forks}")
            lines.append(f"  👁️  网站访问量: {visits}")
            lines.append(f"  🔧 API调用次数: {api_calls}")
            lines.append(f"  👥 活跃用户数: {active_users}")
            lines.append("")
        
        if report['weekly_trend']:
            lines.append("📈 周趋势分析:")
            for row in report['weekly_trend']:
                date_str, stars, visits, api_calls, active_users = row
                lines.append(f"  {date_str}: ⭐{stars} 👁️{visits} 🔧{api_calls} 👥{active_users}")
            lines.append("")
        
        if report['growth_insights']:
            insights = report['growth_insights']
            lines.append("💡 增长洞察:")
            
            for key in ['github_stars_growth', 'website_visits_growth', 
                       'api_calls_growth', 'active_users_growth']:
                if key in insights and isinstance(insights[key], (int, float)):
                    lines.append(f"  {key.replace('_', ' ').title()}: {insights[key]:+.2f}%")
            
            lines.append(f"  整体趋势: {insights.get('trend', 'N/A').replace('_', ' ').title()}")
            lines.append("")
            
            if insights.get('recommendations'):
                lines.append("🎯 建议行动:")
                for rec in insights['recommendations']:
                    lines.append(f"  • {rec}")
        
        lines.append("")
        lines.append("=" * 60)
        lines.append("报告生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def export_to_json(self, output_file="growth_data_export.json"):
        """导出所有数据到JSON"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取所有数据
        cursor.execute('SELECT * FROM growth_metrics ORDER BY timestamp DESC')
        growth_data = cursor.fetchall()
        
        cursor.execute('SELECT * FROM daily_summary ORDER BY date DESC')
        daily_data = cursor.fetchall()
        
        conn.close()
        
        # 构建导出结构
        export_data = {
            'export_time': datetime.now().isoformat(),
            'growth_metrics': [
                {
                    'id': row[0],
                    'timestamp': row[1],
                    'metric_name': row[2],
                    'metric_value': row[3],
                    'source': row[4],
                    'notes': row[5]
                }
                for row in growth_data
            ],
            'daily_summary': [
                {
                    'date': row[0],
                    'github_stars': row[1],
                    'github_forks': row[2],
                    'website_visits': row[3],
                    'api_calls': row[4],
                    'active_users': row[5],
                    'created_at': row[6]
                }
                for row in daily_data
            ]
        }
        
        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已导出到: {output_file}")
        return export_data
    
    def run_full_monitoring(self):
        """运行完整监控流程"""
        print(f"[{datetime.now()}] 开始运行增长监控...")
        
        # 收集各项数据
        github_stats = self.get_github_stats()
        website_stats = self.get_website_analytics()
        api_stats = self.get_api_usage()
        
        # 更新每日汇总
        self.update_daily_summary()
        
        # 生成报告
        report = self.generate_daily_report()
        
        print(f"[{datetime.now()}] 增长监控完成")
        return report

def main():
    """主函数"""
    monitor = GrowthMonitor()
    
    # 运行完整监控
    report = monitor.run_full_monitoring()
    
    # 可选：导出数据
    # monitor.export_to_json()
    
    # 可选：发送报告到邮件或Slack（需要配置）
    # send_report_via_email(report)
    # send_report_via_slack(report)
    
    return report

if __name__ == "__main__":
    main()