#!/usr/bin/env python3
"""
AI News Daily Updater - No external dependencies version
Uses urllib + xml.etree.ElementTree instead of feedparser
"""

import os
import re
import html
import urllib.request
import ssl
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET

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

def clean_html(raw_html):
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', raw_html)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_date(date_str):
    try:
        if date_str:
            dt = parsedate_to_datetime(date_str)
            return dt
    except:
        pass
    return datetime.now()

def fetch_feed(url, timeout=15):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; AINewsBot/1.0)'
    })
    
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            data = resp.read()
            return data
    except Exception as e:
        print(f"  请求失败: {url} - {e}")
        return None

def parse_rss(data):
    root = ET.fromstring(data)
    
    # Handle different RSS formats
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'dc': 'http://purl.org/dc/elements/1.0/'
    }
    
    items = []
    
    # Standard RSS 2.0
    for item in root.iter('item'):
        title_el = item.find('title')
        link_el = item.find('link')
        pub_date_el = item.find('pubDate')
        desc_el = item.find('description')
        
        title = title_el.text if title_el is not None and title_el.text else ''
        link = link_el.text if link_el is not None and link_el.text else ''
        pub_date = pub_date_el.text if pub_date_el is not None and pub_date_el.text else ''
        description = desc_el.text if desc_el is not None and desc_el.text else ''
        
        if title:
            items.append({
                'title': clean_html(title),
                'link': link.strip() if link else '',
                'pub_date': pub_date,
                'description': clean_html(description)
            })
    
    # Atom format fallback
    if not items:
        for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):
            title_el = entry.find('{http://www.w3.org/2005/Atom}title')
            link_el = entry.find('{http://www.w3.org/2005/Atom}link')
            updated_el = entry.find('{http://www.w3.org/2005/Atom}updated')
            summary_el = entry.find('{http://www.w3.org/2005/Atom}summary')
            
            title = title_el.text if title_el is not None and title_el.text else ''
            link = link_el.get('href', '') if link_el is not None else ''
            updated = updated_el.text if updated_el is not None and updated_el.text else ''
            summary = summary_el.text if summary_el is not None and summary_el.text else ''
            
            if title:
                items.append({
                    'title': clean_html(title),
                    'link': link,
                    'pub_date': updated,
                    'description': clean_html(summary)
                })
    
    return items

def fetch_news(limit=8):
    news_list = []
    seen_titles = set()
    
    for feed_info in RSS_FEEDS:
        url = feed_info["url"]
        category = feed_info["category"]
        print(f"正在抓取: {url}")
        
        data = fetch_feed(url)
        if data is None:
            continue
        
        try:
            entries = parse_rss(data)
            for entry in entries[:4]:
                title = entry["title"][:70] + ("..." if len(entry["title"]) > 70 else "")
                
                if title.lower() in seen_titles or len(title) < 10:
                    continue
                seen_titles.add(title.lower())
                
                summary = entry["description"][:120] + ("..." if len(entry["description"]) > 120 else "")
                pub_date = parse_date(entry["pub_date"])
                
                title_lower = title.lower()
                if any(k in title_lower for k in ["gpt", "claude", "gemini", "模型", "发布", "推出", "开源", "llama"]):
                    cat = "模型发布" if any(k in title_lower for k in ["发布", "推出", "gpt", "claude", "gemini", "llama"]) else "开源动态"
                elif any(k in title_lower for k in ["工具", "产品", "app", "插件"]):
                    cat = "工具发现"
                else:
                    cat = category
                
                news_list.append({
                    "title": title,
                    "link": entry["link"],
                    "date": pub_date,
                    "date_str": pub_date.strftime("%Y.%m.%d"),
                    "summary": summary,
                    "category": cat,
                    "priority": feed_info["priority"]
                })
            print(f"  获取到 {len(entries)} 条")
        except Exception as e:
            print(f"  解析失败: {url} - {e}")
    
    news_list.sort(key=lambda x: (-x["date"].timestamp(), x["priority"]))
    
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
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    today = datetime.now().strftime("%Y.%m.%d")
    
    articles_html = ""
    for i, item in enumerate(news_list):
        article = f'''                <a href="{item["link"]}" class="article-item" target="_blank">
                    <div class="article-content">
                        <div class="article-meta">{item["date_str"]} · {item["category"]}</div>
                        <div class="article-title">{item["title"]}</div>
                        <div class="article-summary">{item["summary"]}</div>
                    </div>
                </a>
'''
        articles_html += article
    
    start_marker = '<!-- NEWS_PLACEHOLDER_START -->'
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print("警告: 未找到 NEWS_PLACEHOLDER_START 标记")
        return False
    
    end_marker = '            </div>\n        </div>\n    </div>\n\n            </div>'
    end_idx = content.find(end_marker, start_idx)
    
    if end_idx == -1:
        # Try alternative end marker
        end_marker_alt = '            </div>\n        </div>\n    </div>\n\n    <!-- Footer -->'
        end_idx = content.find(end_marker_alt, start_idx)
        if end_idx == -1:
            print("警告: 未找到结束标记")
            return False
        end_idx += len(end_marker_alt)
    else:
        end_idx += len(end_marker)
    
    new_content = (
        content[:start_idx + len(start_marker)]
        + "\n"
        + articles_html
        + content[end_idx:]
    )
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 成功更新 {len(news_list)} 条 AI 新闻，更新日期: {today}")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print(f"  AI 新闻更新脚本 V3 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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