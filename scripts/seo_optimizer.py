#!/usr/bin/env python3
"""
AI.link.cn SEO自动化优化脚本
功能：
1. 检查页面SEO状态
2. 自动添加缺失的SEO标签
3. 生成SEO报告
4. 更新sitemap和robots.txt
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

class SEOOptimizer:
    def __init__(self, workspace_path):
        self.workspace = Path(workspace_path)
        self.seo_config = self.load_seo_config()
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "pages_checked": 0,
            "issues_found": 0,
            "optimizations_applied": 0,
            "details": []
        }
    
    def load_seo_config(self):
        """加载SEO配置文件"""
        config_path = self.workspace / "config" / "seo_keywords.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "primary_keywords": ["AI工具", "人工智能", "工具评测", "AI推荐"],
            "secondary_keywords": ["教程", "使用指南", "2026", "免费", "替代"]
        }
    
    def check_page_seo(self, html_file):
        """检查单个页面的SEO状态"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # 检查基础SEO元素
        if not re.search(r'<title>', content):
            issues.append("缺少title标签")
        elif len(re.findall(r'<title>', content)) > 1:
            issues.append("多个title标签")
        
        if not re.search(r'<meta\s+name="description"', content):
            issues.append("缺少meta description")
        
        # 检查Open Graph标签
        og_tags = ['og:title', 'og:description', 'og:image', 'og:url']
        missing_og = []
        for tag in og_tags:
            if not re.search(f'property="{tag}"', content) and not re.search(f'property="{tag}"', content):
                missing_og.append(tag)
        if missing_og:
            issues.append(f"缺少Open Graph标签: {', '.join(missing_og)}")
        
        # 检查结构化数据
        if not re.search(r'schema\.org|ld\+json', content, re.IGNORECASE):
            issues.append("缺少结构化数据")
        
        # 检查H1标签
        h1_count = len(re.findall(r'<h1[^>]*>', content))
        if h1_count == 0:
            issues.append("缺少H1标签")
        elif h1_count > 1:
            issues.append(f"多个H1标签: {h1_count}个")
        
        # 检查图片alt文本
        img_tags = re.findall(r'<img[^>]*>', content)
        img_without_alt = [img for img in img_tags if 'alt=' not in img]
        if img_tags and img_without_alt:
            issues.append(f"{len(img_without_alt)}/{len(img_tags)}张图片缺少alt文本")
        
        # 检查关键词密度（简单检查）
        primary_kws = self.seo_config.get('primary_keywords', [])
        found_kws = []
        for kw in primary_kws[:5]:  # 只检查前5个主要关键词
            if kw.lower() in content.lower():
                found_kws.append(kw)
        
        if found_kws:
            kw_status = f"找到关键词: {', '.join(found_kws)}"
        else:
            kw_status = "未找到主要关键词"
            issues.append("关键词密度不足")
        
        return {
            "file": str(html_file.relative_to(self.workspace)),
            "issues": issues,
            "keywords": kw_status,
            "score": 100 - (len(issues) * 10)
        }
    
    def optimize_page(self, html_file, issues):
        """优化页面SEO"""
        if not issues:
            return False
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # 如果没有Open Graph标签，添加它们
        if any('Open Graph' in issue for issue in issues):
            head_end = content.find('</head>')
            if head_end != -1:
                og_tags = '''
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://project-f5cf8.vercel.app/">
    <meta property="og:title" content="AI.link.cn - 专业的AI工具评测和推荐平台">
    <meta property="og:description" content="每日更新的AI工具评测平台，为您推荐最好的人工智能工具。">
    <meta property="og:image" content="https://project-f5cf8.vercel.app/images/ai-tools-og.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="AI.link.cn - AI工具评测平台">
    <meta property="og:site_name" content="AI.link.cn">
    <meta property="og:locale" content="zh_CN">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://project-f5cf8.vercel.app/">
    <meta name="twitter:title" content="AI.link.cn - 专业的AI工具评测和推荐平台">
    <meta name="twitter:description" content="每日更新的AI工具评测平台，为您推荐最好的人工智能工具。">
    <meta name="twitter:image" content="https://project-f5cf8.vercel.app/images/ai-tools-twitter.png">
    <meta name="twitter:image:alt" content="AI.link.cn - AI工具评测平台">
                '''
                content = content[:head_end] + og_tags + content[head_end:]
                modified = True
        
        if modified:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return modified
    
    def update_sitemap(self):
        """更新网站地图"""
        today = datetime.now().strftime('%Y-%m-%d')
        sitemap_path = self.workspace / "sitemap.xml"
        
        if not sitemap_path.exists():
            print("sitemap.xml不存在，正在创建...")
            return
        
        # 简单的sitemap更新：更新最后修改时间
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新首页的最后修改时间
        updated_content = re.sub(
            r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>',
            f'<lastmod>{today}</lastmod>',
            content,
            count=1
        )
        
        if content != updated_content:
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✅ sitemap.xml已更新到 {today}")
    
    def generate_report(self):
        """生成SEO报告"""
        report_path = self.workspace / "logs" / f"seo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 SEO报告已生成: {report_path}")
    
    def run(self):
        """运行SEO检查和优化"""
        print("🔍 开始SEO检查和优化...")
        print("=" * 50)
        
        # 查找所有HTML文件
        html_files = list(self.workspace.rglob("*.html"))
        
        for html_file in html_files:
            # 跳过备份文件和node_modules等目录
            if any(skip in str(html_file) for skip in ['backup-old-project', 'node_modules', '.git']):
                continue
            
            self.report["pages_checked"] += 1
            result = self.check_page_seo(html_file)
            
            if result["issues"]:
                self.report["issues_found"] += len(result["issues"])
                print(f"❌ {result['file']}")
                print(f"   评分: {result['score']}/100")
                print(f"   问题: {', '.join(result['issues'])}")
                
                # 尝试优化
                optimized = self.optimize_page(html_file, result["issues"])
                if optimized:
                    self.report["optimizations_applied"] += 1
                    print(f"   ✅ 已自动优化")
            else:
                print(f"✅ {result['file']}")
                print(f"   评分: {result['score']}/100")
                print(f"   {result['keywords']}")
            
            self.report["details"].append(result)
        
        print("=" * 50)
        
        # 更新sitemap
        self.update_sitemap()
        
        # 生成报告
        self.generate_report()
        
        print(f"📊 检查完成:")
        print(f"   检查页面: {self.report['pages_checked']}个")
        print(f"   发现问题: {self.report['issues_found']}个")
        print(f"   应用优化: {self.report['optimizations_applied']}个")
        
        if self.report["issues_found"] == 0:
            print("🎉 所有页面SEO状态良好！")
        else:
            print("🔧 请查看上述问题并考虑进一步优化")

def main():
    workspace_path = "/root/.openclaw/workspace"
    optimizer = SEOOptimizer(workspace_path)
    optimizer.run()

if __name__ == "__main__":
    main()