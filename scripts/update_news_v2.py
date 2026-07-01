#!/usr/bin/env python3
"""
AI News Daily Updater - Enhanced Version
- 抓取多个 RSS 源的最新 AI 新闻
- 使用现有 article-list 样式更新到"最新洞察"区域
- 自动生成分类标签和简洁摘要
"""

import feedparser
import os
import re
import html
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

RSS_FEEDS = [
    {
        "url": "https://www.jiqizhixin.com/rss",
        "category": "行业动态",
        "priority": 1
    },
    {
        "url": "https://www.qbitai.com/feed",
        "category": "技术前沿",
        "priority": 1
    },
    {
        "url": "https://36kr.com/feed",
        "category": "商业观察",
        "priority": 2
    },
    {
        "url": "https://www.zhidx.com/feed",
        "category": "政策趋势",
        "priority": 2
    },
    {
        "url": "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "category": "全球动态",
        "priority": 2
    },
    {
        "url": "https://venturebeat.com/category/ai/feed/",
        "category": "企业应用",
        "priority": 3
    },
]

CATEGORY_NAMES = {
    "行业动态": "行业动态",
    "技术前沿": "技术前沿",
    "商业观察": "商业观察",
    "政策趋势": "政策趋势",
    "全球动态": "全球动态",
    "企业应用": "企业应用",
    "模型发布": "模型发布",
    "开源动态": "开源动态",
    "工具发现": "工具发现",
}

def clean_html(raw_html):
    """移除 HTML 标签，提取纯文本"""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', raw_html)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_date(date_str):
    """解析日期字符串"""
    try:
        if date_str:
            # 尝试解析 RFC 2822 格式
            dt = parsedate_to_datetime(date_str)
            return dt
    except:
        pass
    return datetime.now()

def fetch_news(limit=8):
    """从多个 RSS 源抓取新闻"""
    news_list = []
    seen_titles = set()
    
    for feed_info in RSS_FEEDS:
        url = feed_info["url"]
        category = feed_info["category"]
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:4]:
                title = clean_html(entry.get("title", ""))
                title = title[:70] + ("..." if len(title) > 70 else "")
                
                if title.lower() in seen_titles or len(title) < 10:
                    continue
                seen_titles.add(title.lower())
                
                summary = clean_html(entry.get("summary", "") or entry.get("description", ""))
                summary = summary[:120] + ("..." if len(summary) > 120 else "")
                
                pub_date = parse_date(entry.get("published", ""))
                
                # 智能分类
                title_lower = title.lower()
                if any(k in title_lower for k in ["gpt", "claude", "gemini", "模型", "发布", "推出", "开源", "llama"]):
                    cat = "模型发布" if any(k in title_lower for k in ["发布", "推出", "gpt", "claude", "gemini", "llama"]) else "开源动态"
                elif any(k in title_lower for k in ["工具", "产品", "app", "插件"]):
                    cat = "工具发现"
                else:
                    cat = category
                
                news_list.append({
                    "title": title,
                    "link": entry.get("link", ""),
                    "date": pub_date,
                    "date_str": pub_date.strftime("%Y.%m.%d"),
                    "summary": summary,
                    "category": cat,
                    "priority": feed_info["priority"]
                })
        except Exception as e:
            print(f"抓取失败: {url} - {e}")
    
    # 按时间排序（最新优先），同优先级的在前
    news_list.sort(key=lambda x: (-x["date"].timestamp(), x["priority"]))
    
    # 去重并限制数量
    final_list = []
    seen = set()
    for item in news_list:
        key = item["title"][:20].lower()
        if key not in seen:
            seen.add(key)
            final_list.append(item)
            if len(final_list) >= limit:
                break
    
    return final_list

def update_articles_in_html(news_list):
    """更新 index.html 中的文章列表"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    today = datetime.now().strftime("%Y.%m.%d")
    
    articles_html = ""
    for i, item in enumerate(news_list):
        article = f'''                <div class="article-item">
                    <div class="article-content">
                        <div class="article-meta">{item["date_str"]} · {item["category"]}</div>
                        <div class="article-title">{item["title"]}</div>
                        <div class="article-summary">{item["summary"]}</div>
                    </div>
                </div>
'''
        articles_html += article
    
    # 替换 article-list 内容
    pattern = r'(<div class="article-list">)(.*?)(</div>\s*</div>\s*</div>\s*<footer)'
    replacement = r'\1\n' + articles_html + '                \3'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print("警告: 未找到匹配的 article-list，内容未更新")
        return False
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 成功更新 {len(news_list)} 条 AI 新闻，更新日期: {today}")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print(f"  AI 新闻更新脚本 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    print("正在抓取 RSS 新闻源...")
    news = fetch_news(limit=8)
    
    if news:
        print(f"\n获取到 {len(news)} 条新闻:")
        for i, item in enumerate(news, 1):
            print(f"  {i}. [{item['date_str']}] {item['title'][:50]}...")
        
        print(f"\n正在更新 index.html...")
        success = update_articles_in_html(news)
        
        if success:
            print("\n✅ 更新完成！")
        else:
            print("\n❌ 更新失败")
    else:
        print("\n❌ 未获取到任何新闻")
