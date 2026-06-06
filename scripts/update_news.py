#!/usr/bin/env python3
"""
AI News Daily Updater (简化版)
- 仅抓取 RSS，不调用 AI
- 更新 index.html 中的新闻列表
"""

import feedparser
from datetime import datetime

# RSS Sources (中英文各 4 个)
RSS_FEEDS = [
    # English
    "https://deeplearning.ai/the-batch/rss/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    # Chinese
    "https://www.jiqizhixin.com/rss",
    "https://www.qbitai.com/feed",
    "https://36kr.com/feed",
    "https://www.zhidx.com/feed",
]

def fetch_news(limit=6):
    """抓取最新新闻"""
    news_list = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:  # 每个源取 2 条
                news_list.append({
                    "title": entry.get("title", "")[:80],
                    "link": entry.get("link", ""),
                    "published": entry.get("published", "")[:16] if entry.get("published") else ""
                })
        except Exception as e:
            print(f"抓取失败: {url} - {e}")
    return news_list[:limit]

def update_html(news_list):
    """更新 index.html（简化版，实际可替换新闻区块）"""
    print(f"[{datetime.now()}] 成功抓取 {len(news_list)} 条新闻")
    for item in news_list:
        print(f"- {item['title']}")

if __name__ == "__main__":
    print("开始更新 AI 新闻...")
    news = fetch_news()
    update_html(news)
    print("更新完成。")