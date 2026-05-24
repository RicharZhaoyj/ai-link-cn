#!/usr/bin/env python3
"""
改进的AI工具发现系统
使用官方API和可靠的数据源，避免反爬虫限制
"""

import json
import requests
import os
import datetime
from pathlib import Path
import time

class AIDiscoveryImprovement:
    def __init__(self):
        self.workspace = Path("/root/.openclaw/workspace")
        self.discovered_dir = self.workspace / "discovered_tools"
        self.discovered_dir.mkdir(exist_ok=True)
        
        # 使用可靠的API和数据源
        self.sources = [
            {
                "name": "GitHub Trending AI",
                "type": "github_api",
                "url": "https://api.github.com/search/repositories?q=stars:>100+language:python+ai+machine+learning&sort=stars&order=desc",
                "description": "GitHub上最受欢迎的AI/ML项目"
            },
            {
                "name": "Hacker News AI Tools",
                "type": "hackernews_api",
                "url": "https://hn.algolia.com/api/v1/search?query=AI%20tool&tags=story&numericFilters=points>50",
                "description": "Hacker News上讨论的热门AI工具"
            },
            {
                "name": "Awesome AI List",
                "type": "github_raw",
                "url": "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md",
                "description": "Awesome AI开源列表"
            },
            {
                "name": "AI Tools Library",
                "type": "static_list",
                "url": "",
                "description": "预定义的AI工具库",
                "tools": [
                    "Claude (Anthropic)",
                    "DALL-E (OpenAI)",
                    "Stable Diffusion",
                    "Bard (Google)",
                    "Perplexity AI",
                    "ElevenLabs",
                    "Descript",
                    "RunwayML",
                    "Tome",
                    "Synthesia",
                    "Murf AI",
                    "Pictory",
                    "InVideo",
                    "Play.ht",
                    "Copy.ai",
                    "Anyword",
                    "Writesonic",
                    "Scale AI",
                    "Labelbox",
                    "SuperAnnotate"
                ]
            }
        ]
    
    def fetch_github_trending(self):
        """从GitHub API获取热门AI项目"""
        try:
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "AI-Discovery-Bot"
            }
            
            response = requests.get(
                self.sources[0]["url"],
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                tools = []
                
                for item in data.get("items", [])[:10]:  # 取前10个
                    tool_info = {
                        "name": item["name"],
                        "description": item.get("description", "No description"),
                        "url": item["html_url"],
                        "stars": item["stargazers_count"],
                        "language": item.get("language", "Unknown"),
                        "source": "GitHub"
                    }
                    tools.append(tool_info)
                
                return tools
            else:
                print(f"GitHub API错误: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"获取GitHub数据失败: {e}")
            return []
    
    def fetch_hackernews_ai(self):
        """从Hacker News API获取AI工具讨论"""
        try:
            response = requests.get(
                self.sources[1]["url"],
                headers={"User-Agent": "AI-Discovery-Bot"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                tools = []
                
                for hit in data.get("hits", [])[:10]:  # 取前10个
                    if "ai" in hit.get("title", "").lower() or "tool" in hit.get("title", "").lower():
                        tool_info = {
                            "name": hit["title"],
                            "description": f"HN讨论: {hit.get('points', 0)} points",
                            "url": hit.get("url", f"https://news.ycombinator.com/item?id={hit['objectID']}"),
                            "source": "Hacker News"
                        }
                        tools.append(tool_info)
                
                return tools
            else:
                print(f"Hacker News API错误: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"获取Hacker News数据失败: {e}")
            return []
    
    def get_static_ai_tools(self):
        """获取预定义的AI工具列表"""
        tools = []
        
        for tool_name in self.sources[3]["tools"]:
            # 为每个工具生成简单的URL和描述
            search_query = tool_name.replace(" ", "+")
            tool_info = {
                "name": tool_name,
                "description": f"知名的AI工具 - {tool_name}",
                "url": f"https://www.google.com/search?q={search_query}",
                "source": "AI Tools Library"
            }
            tools.append(tool_info)
        
        return tools
    
    def discover_new_tools(self):
        """发现新工具的主函数"""
        print("🚀 开始发现新AI工具...")
        
        all_tools = []
        
        # 1. 从GitHub获取
        print("📡 从GitHub获取热门AI项目...")
        github_tools = self.fetch_github_trending()
        all_tools.extend(github_tools)
        print(f"   找到 {len(github_tools)} 个GitHub项目")
        
        # 2. 从Hacker News获取
        print("📡 从Hacker News获取AI工具讨论...")
        hn_tools = self.fetch_hackernews_ai()
        all_tools.extend(hn_tools)
        print(f"   找到 {len(hn_tools)} 个HN讨论")
        
        # 3. 添加静态工具列表
        print("📡 添加预定义AI工具库...")
        static_tools = self.get_static_ai_tools()
        all_tools.extend(static_tools)
        print(f"   添加 {len(static_tools)} 个预定义工具")
        
        # 去重
        unique_tools = []
        seen_names = set()
        
        for tool in all_tools:
            if tool["name"] not in seen_names:
                seen_names.add(tool["name"])
                unique_tools.append(tool)
        
        print(f"📊 总计发现 {len(unique_tools)} 个唯一AI工具")
        
        # 保存发现结果
        self.save_discovery(unique_tools)
        
        return unique_tools
    
    def save_discovery(self, tools):
        """保存发现结果"""
        if not tools:
            print("⚠️ 没有发现新工具")
            return
        
        # 创建报告文件
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        report_file = self.discovered_dir / f"new_tools_{timestamp}.md"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"# AI工具发现报告 - {timestamp}\n\n")
            f.write(f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**总计发现**: {len(tools)} 个工具\n\n")
            
            # 按来源分组
            sources = {}
            for tool in tools:
                source = tool.get("source", "Unknown")
                if source not in sources:
                    sources[source] = []
                sources[source].append(tool)
            
            for source, source_tools in sources.items():
                f.write(f"## 来源: {source}\n\n")
                
                for i, tool in enumerate(source_tools, 1):
                    f.write(f"### {i}. {tool['name']}\n\n")
                    f.write(f"- **描述**: {tool['description']}\n")
                    f.write(f"- **URL**: {tool['url']}\n")
                    
                    # 额外信息
                    extra_info = []
                    if "stars" in tool:
                        extra_info.append(f"Stars: {tool['stars']}")
                    if "language" in tool:
                        extra_info.append(f"语言: {tool['language']}")
                    
                    if extra_info:
                        f.write(f"- **信息**: {', '.join(extra_info)}\n")
                    
                    f.write("\n")
        
        print(f"✅ 发现报告已保存: {report_file}")
        
        # 更新数据库
        self.update_database(tools)
    
    def update_database(self, new_tools):
        """更新AI工具数据库"""
        db_path = self.workspace / "ai_tools_database.json"
        
        try:
            # 读取现有数据库
            if db_path.exists():
                with open(db_path, "r", encoding="utf-8") as f:
                    db = json.load(f)
            else:
                db = {"tools": [], "lastUpdated": "", "stats": {}}
            
            existing_tools = {tool["name"] for tool in db.get("tools", [])}
            added_count = 0
            
            # 添加新工具到数据库
            for tool in new_tools:
                # 避免重复
                if tool["name"] in existing_tools:
                    continue
                
                # 创建数据库条目
                db_tool = {
                    "id": tool["name"].lower().replace(" ", "_").replace("(", "").replace(")", ""),
                    "name": tool["name"],
                    "category": self.categorize_tool(tool["name"]),
                    "description": tool["description"],
                    "url": tool["url"],
                    "pricing": "免费/付费",
                    "rating": 4.0,
                    "pros": ["功能强大", "易于使用"],
                    "cons": ["可能需要学习"],
                    "addedDate": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "lastUpdated": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "featured": False,
                    "reviewUrl": f"/pages/tools/{tool['name'].lower().replace(' ', '_')}.html"
                }
                
                db["tools"].append(db_tool)
                added_count += 1
            
            # 更新元数据
            db["lastUpdated"] = datetime.datetime.now().isoformat()
            db["stats"] = {
                "totalTools": len(db["tools"]),
                "newThisWeek": added_count,
                "categories": self.count_categories(db["tools"])
            }
            
            # 保存数据库
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 数据库已更新: 添加了 {added_count} 个新工具")
            print(f"   数据库总计: {len(db['tools'])} 个工具")
            
        except Exception as e:
            print(f"❌ 更新数据库失败: {e}")
    
    def categorize_tool(self, tool_name):
        """根据工具名称分类"""
        tool_name_lower = tool_name.lower()
        
        if any(keyword in tool_name_lower for keyword in ["chat", "gpt", "claude", "bard"]):
            return "对话AI"
        elif any(keyword in tool_name_lower for keyword in ["image", "art", "draw", "dall", "midjourney", "stable"]):
            return "图像生成"
        elif any(keyword in tool_name_lower for keyword in ["write", "grammar", "copy", "content"]):
            return "写作助手"
        elif any(keyword in tool_name_lower for keyword in ["code", "program", "copilot", "dev"]):
            return "编程助手"
        elif any(keyword in tool_name_lower for keyword in ["video", "audio", "edit"]):
            return "多媒体工具"
        else:
            return "AI工具"
    
    def count_categories(self, tools):
        """统计分类"""
        categories = {}
        for tool in tools:
            cat = tool.get("category", "AI工具")
            categories[cat] = categories.get(cat, 0) + 1
        return categories

def main():
    """主函数"""
    discovery = AIDiscoveryImprovement()
    
    print("=" * 60)
    print("🤖 AI工具发现系统 - 改进版")
    print("=" * 60)
    
    # 发现新工具
    new_tools = discovery.discover_new_tools()
    
    if new_tools:
        print("\n🎯 发现的新工具:")
        for i, tool in enumerate(new_tools[:5], 1):  # 显示前5个
            print(f"  {i}. {tool['name']} ({tool['source']})")
        
        if len(new_tools) > 5:
            print(f"  ... 还有 {len(new_tools) - 5} 个工具")
    else:
        print("\n⚠️ 没有发现新工具")
    
    print("\n✅ 发现流程完成")

if __name__ == "__main__":
    main()