#!/usr/bin/env python3
"""
AI News Daily Updater
- 抓取 RSS 新闻
- 更新 index.html 中的新闻列表
"""

import feedparser
import re
from datetime import datetime

# RSS Sources
RSS_FEEDS = [
    "https://deeplearning.ai/the-batch/rss/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
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
            for entry in feed.entries[:2]:
                news_list.append({
                    "title": entry.get("title", "")[:80],
                    "link": entry.get("link", ""),
                    "published": entry.get("published", "")[:16] if entry.get("published") else ""
                })
        except Exception as e:
            print(f"抓取失败: {url} - {e}")
    return news_list[:limit]

def update_html(news_list):
    """更新 index.html 中的新闻列表"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 生成新的新闻卡片 HTML
    cards_html = ""
    tags = ["tag-model", "tag-tech", "tag-open"]
    tag_names = ["模型发布", "技术突破", "开源动态"]

    for i, item in enumerate(news_list):
        tag_class = tags[i % 3]
        tag_name = tag_names[i % 3]
        date = item["published"] or datetime.now().strftime("%Y-%m-%d")

        card = f'''                <div class="news-card">
                    <div class="news-meta">
                        <span class="tag {tag_class}">{tag_name}</span>
                        <span class="news-date">{date}</span>
                    </div>
                    <h3>{item['title']}</h3>
                    <p>点击下方链接查看完整内容。</p>
                    <a href="{item['link']}" class="news-link" target="_blank">阅读全文 →</a>
                </div>
'''
        cards_html += card

    # 替换新闻网格内容
    pattern = r'(<div class="news-grid">)(.*?)(</div>\s*<div style="text-align: center; margin-top: 20px;">)'
    replacement = r'\1' + cards_html + r'\3'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[{datetime.now()}] 成功更新 {len(news_list)} 条新闻到 index.html")

if __name__ == "__main__":
    print("开始更新 AI 新闻...")
    news = fetch_news()
    update_html(news)
    print("更新完成。")