#!/usr/bin/env python3
# 重新生成所有页面，确保UTF-8编码

import os
import sys

def ensure_utf8(filepath):
    """确保文件是UTF-8编码"""
    try:
        # 读取文件内容
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # 尝试解码为UTF-8
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            # 如果不是UTF-8，尝试其他编码
            import chardet
            result = chardet.detect(content)
            encoding = result['encoding']
            if encoding:
                text = content.decode(encoding, errors='ignore')
            else:
                text = content.decode('utf-8', errors='ignore')
        
        # 确保HTML头部有正确的charset
        if '<!DOCTYPE html>' in text:
            if '<meta charset="UTF-8">' not in text and '<meta charset="utf-8">' not in text:
                # 插入charset meta
                text = text.replace('<head>', '<head>\n    <meta charset="UTF-8">')
                text = text.replace('<head>\n    <meta charset="UTF-8">\n    <meta charset="UTF-8">', '<head>\n    <meta charset="UTF-8">')
        
        # 写入UTF-8文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✅ 修复: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ 修复失败 {filepath}: {e}")
        return False

def create_simple_index():
    """创建简单的主页"""
    content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI.link.cn - 专业的AI工具评测和推荐平台</title>
    <meta name="description" content="AI.link.cn提供最新的AI工具评测、使用教程和推荐指南。每日自动更新，为您推荐最好的人工智能工具。">
    <meta name="keywords" content="AI工具,人工智能,工具评测,AI推荐,机器学习">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        header { background: #667eea; color: white; padding: 2rem; border-radius: 10px; text-align: center; }
        nav a { color: white; margin: 0 10px; }
        .tools { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }
        .tool { background: #f8f9fa; padding: 1rem; border-radius: 8px; }
        footer { text-align: center; padding: 2rem; color: #666; }
    </style>
</head>
<body>
    <header>
        <h1>AI.link.cn</h1>
        <p>专业的AI工具评测和推荐平台</p>
        <nav>
            <a href="/">首页</a>
            <a href="/pages/tools/index.html">所有工具</a>
            <a href="/pages/about.html">关于我们</a>
        </nav>
    </header>
    
    <main>
        <h2>已收录的AI工具</h2>
        <div class="tools">
            <div class="tool">
                <h3>ChatGPT</h3>
                <p>最先进的对话AI</p>
                <a href="/pages/tools/chatgpt.html">查看详情</a>
            </div>
            <div class="tool">
                <h3>Midjourney</h3>
                <p>强大的AI图像生成工具</p>
                <a href="/pages/tools/midjourney.html">查看详情</a>
            </div>
            <div class="tool">
                <h3>GitHub Copilot</h3>
                <p>AI编程助手</p>
                <a href="/pages/tools/github_copilot.html">查看详情</a>
            </div>
            <div class="tool">
                <h3>Canva</h3>
                <p>设计工具</p>
                <a href="/pages/tools/canva.html">查看详情</a>
            </div>
        </div>
        
        <div style="background: #e8f4fd; padding: 1rem; border-radius: 8px; margin: 2rem 0;">
            <h3>🚀 自动更新系统</h3>
            <p>网站每天自动更新：</p>
            <ul>
                <li>凌晨2点：发现新AI工具</li>
                <li>凌晨2:30：生成工具页面</li>
                <li>自动提交到GitHub</li>
                <li>触发Vercel部署</li>
            </ul>
        </div>
    </main>
    
    <footer>
        <p>&copy; 2026 AI.link.cn - 专业的AI工具评测和推荐平台</p>
        <p>最后更新: 2026年5月17日</p>
    </footer>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 已生成UTF-8编码的主页")

def main():
    workspace = os.getcwd()
    
    print("=== 重新生成页面确保UTF-8编码 ===")
    
    # 1. 创建简单的主页
    create_simple_index()
    
    # 2. 修复关键HTML文件
    key_files = [
        'pages/tools/index.html',
        'pages/tools/chatgpt.html',
        'pages/tools/midjourney.html',
        'pages/tools/github_copilot.html',
        'pages/about.html',
        'test_site.html'
    ]
    
    print("\n2. 修复关键HTML文件:")
    for filepath in key_files:
        if os.path.exists(filepath):
            ensure_utf8(filepath)
        else:
            print(f"⚠️  文件不存在: {filepath}")
    
    # 3. 检查并修复所有工具页面
    print("\n3. 修复所有工具页面:")
    tools_dir = 'pages/tools'
    if os.path.exists(tools_dir):
        for filename in os.listdir(tools_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(tools_dir, filename)
                ensure_utf8(filepath)
    
    print("\n✅ 修复完成")
    print("\n建议:")
    print("1. 清除浏览器缓存后访问网站")
    print("2. 检查服务器是否正确设置了Content-Type: text/html; charset=utf-8")
    print("3. 确保所有HTML文件都以UTF-8编码保存")

if __name__ == "__main__":
    main()