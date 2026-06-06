#!/usr/bin/env python3
"""
AI News Daily Updater
- 抓取 RSS 新闻
- 使用 DeepSeek 进行 AI 总结
- 更新 index.html
"""

import feedparser
import requests
import os
import re
from datetime import datetime

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

DEEPSEEK_API_KEY = os.environ.get("AI_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def fetch_news(limit=6):
    news_list = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:
                news_list.append({
                    "title": entry.get("title", "")[:80],
                    "link": entry.get("link", ""),
                    "published": entry.get("published", "")[:16] if entry.get("published") else "",
                    "summary": entry.get("summary", "")[:400]
                })
        except Exception as e:
            print(f"抓取失败: {url} - {e}")
    return news_list[:limit]

def summarize_with_deepseek(text):
    """使用 DeepSeek 生成简洁总结"""
    if not DEEPSEEK_API_KEY:
        return text[:120] + "..."

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的AI新闻编辑，请用简洁的中文总结以下新闻，控制在80字以内，突出核心信息。"},
            {"role": "user", "content": text}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"DeepSeek API 错误: {e}")
        return text[:120] + "..."

def update_html(news_list):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    cards_html = ""
    tags = ["tag-model", "tag-tech", "tag-open"]
    tag_names = ["模型发布", "技术突破", "开源动态"]

    for i, item in enumerate(news_list):
        tag_class = tags[i % 3]
        tag_name = tag_names[i % 3]
        date = item["published"] or datetime.now().strftime("%Y-%m-%d")
        summary = summarize_with_deepseek(item["summary"])

        card = f'''                <div class="news-card">
                    <div class="news-meta">
                        <span class="tag {tag_class}">{tag_name}</span>
                        <span class="news-date">{date}</span>
                    </div>
                    <h3>{item['title']}</h3>
                    <p>{summary}</p>
                    <a href="{item['link']}" class="news-link" target="_blank">阅读全文 →</a>
                </div>
'''
        cards_html += card

    pattern = r'(<div class="news-grid">)(.*?)(</div>\s*<div style="text-align: center; margin-top: 20px;">)'
    replacement = r'\1' + cards_html + r'\3'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[{datetime.now()}] 成功更新 {len(news_list)} 条新闻（含 AI 总结）")

if __name__ == "__main__":
    print("开始更新 AI 新闻...")
    news = fetch_news()
    update_html(news)
    print("更新完成。")