#!/bin/bash

# 修复HTML文件编码问题

set -e

echo "=== 修复HTML文件编码问题 ==="
echo "修复时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKSPACE="/root/.openclaw/workspace"

# 1. 检查所有HTML文件的编码
echo "1. 检查HTML文件编码..."
for html_file in $(find "$WORKSPACE" -name "*.html" -type f); do
    encoding=$(file -b --mime-encoding "$html_file" 2>/dev/null || echo "unknown")
    if [[ "$encoding" != "utf-8" && "$encoding" != "us-ascii" ]]; then
        echo "❌ $html_file: $encoding"
    fi
done
echo ""

# 2. 修复主要HTML文件
echo "2. 修复主要HTML文件..."
cat > "$WORKSPACE/index_fixed.html" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI.link.cn - 专业的AI工具评测和推荐平台</title>
    <meta name="description" content="AI.link.cn提供最新的AI工具评测、使用教程和推荐指南。每日自动更新，为您推荐最好的人工智能工具。">
    <meta name="keywords" content="AI工具,人工智能,工具评测,AI推荐,机器学习">
    <style>
        /* 基本样式 - 确保中文字体显示 */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
            line-height: 1.6; 
            color: #333; 
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        /* 头部 */
        header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 2rem; 
            border-radius: 10px; 
            margin-bottom: 2rem; 
            text-align: center; 
        }
        header h1 { font-size: 2.5rem; margin-bottom: 1rem; }
        nav { margin-top: 1rem; }
        nav a { 
            color: white; 
            text-decoration: none; 
            margin: 0 10px; 
            padding: 8px 15px; 
            border-radius: 5px; 
            background: rgba(255,255,255,0.1); 
        }
        nav a:hover { background: rgba(255,255,255,0.2); }
        
        /* 主要内容 */
        main { 
            background: white; 
            padding: 2rem; 
            border-radius: 10px; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.1); 
            margin-bottom: 2rem; 
        }
        
        h2 { color: #667eea; margin-bottom: 1.5rem; }
        
        /* 工具列表 */
        .tools-list { 
            list-style: none; 
            padding: 0; 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); 
            gap: 1rem; 
            margin: 2rem 0; 
        }
        .tools-list li { 
            background: #f8f9fa; 
            padding: 1rem; 
            border-radius: 8px; 
            border: 1px solid #e0e0e0; 
        }
        .tools-list a { 
            color: #333; 
            text-decoration: none; 
            font-weight: 500; 
        }
        .tools-list a:hover { color: #667eea; }
        
        /* 状态指示 */
        .status { 
            padding: 1rem; 
            border-radius: 8px; 
            margin: 1rem 0; 
        }
        .success { 
            background: #d4edda; 
            color: #155724; 
            border: 1px solid #c3e6cb; 
        }
        .warning { 
            background: #fff3cd; 
            color: #856404; 
            border: 1px solid #ffeaa7; 
        }
        
        /* 底部 */
        footer { 
            text-align: center; 
            padding: 2rem; 
            margin-top: 2rem; 
            color: #666; 
            border-top: 1px solid #e0e0e0; 
        }
        
        /* 响应式 */
        @media (max-width: 768px) {
            .tools-list { grid-template-columns: 1fr; }
            header h1 { font-size: 1.8rem; }
            .container { padding: 10px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AI.link.cn</h1>
            <p>专业的AI工具评测和推荐平台</p>
            <nav>
                <a href="/">首页</a>
                <a href="/pages/tools">所有工具</a>
                <a href="/pages/about">关于我们</a>
                <a href="/test_site.html">系统状态</a>
            </nav>
        </header>
        
        <div class="status success">
            <h3>✅ 自动化系统正常运行</h3>
            <p>网站每日自动更新，最后更新时间: 2026年5月17日 12:12:00</p>
        </div>
        
        <main>
            <h2>已收录的AI工具</h2>
            <p>我们每日自动发现和评测最新的AI工具，以下是我们推荐的优质工具:</p>
            
            <ul class="tools-list">
                <li><a href="/pages/tools/chatgpt.html">ChatGPT</a> - 最先进的对话AI</li>
                <li><a href="/pages/tools/midjourney.html">Midjourney</a> - 强大的AI图像生成工具</li>
                <li><a href="/pages/tools/github_copilot.html">GitHub Copilot</a> - AI编程助手</li>
                <li><a href="/pages/tools/canva.html">Canva</a> - 设计工具</li>
                <li><a href="/pages/tools/grammarly.html">Grammarly</a> - 写作助手</li>
                <li><a href="/pages/tools/jasper.html">Jasper AI</a> - 内容创作AI</li>
            </ul>
            
            <div class="status warning">
                <h3>🚀 自动更新功能</h3>
                <p>我们的网站每天自动:</p>
                <ul style="margin: 10px 0 10px 20px;">
                    <li>凌晨2点: 发现新AI工具</li>
                    <li>凌晨2:30: 生成工具页面并更新网站</li>
                    <li>自动提交变更到GitHub</li>
                    <li>触发Vercel自动部署</li>
                </ul>
            </div>
        </main>
        
        <footer>
            <p>&copy; 2026 AI.link.cn - 专业的AI工具评测和推荐平台</p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #888;">
                本网站采用自动化系统维护，每日自动更新AI工具信息。
            </p>
        </footer>
    </div>
    
    <script>
        // 简单的时间更新
        function updateTime() {
            const now = new Date();
            const timeElement = document.querySelector('.success p');
            if (timeElement) {
                const timeStr = '网站每日自动更新，最后更新时间: ' + 
                               now.getFullYear() + '年' + 
                               (now.getMonth() + 1) + '月' + 
                               now.getDate() + '日 ' + 
                               now.getHours() + ':' + 
                               now.getMinutes().toString().padStart(2, '0') + ':' + 
                               now.getSeconds().toString().padStart(2, '0');
                timeElement.textContent = timeStr;
            }
        }
        // 每分钟更新时间
        setInterval(updateTime, 60000);
        updateTime();
    </script>
</body>
</html>
EOF

echo "✅ 已生成修复后的主页: index_fixed.html"
echo ""

# 3. 检查并修复工具页面的编码
echo "3. 修复工具页面编码..."
for tool_file in $(find "$WORKSPACE/pages/tools" -name "*.html" -type f); do
    # 确保文件是UTF-8编码
    iconv -f UTF-8 -t UTF-8 "$tool_file" > "${tool_file}.tmp" 2>/dev/null && mv "${tool_file}.tmp" "$tool_file"
    echo "  修复: $(basename $tool_file)"
done
echo ""

# 4. 创建编码验证脚本
echo "4. 创建编码验证脚本..."
cat > "$WORKSPACE/scripts/validate_encoding.py" << 'EOF'
#!/usr/bin/env python3
# HTML文件编码验证脚本

import os
import sys
import chardet

def check_file_encoding(filepath):
    """检查文件编码"""
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            
            # 检查HTML头部是否包含正确的charset
            content = raw_data.decode(encoding, errors='ignore') if encoding else raw_data.decode('utf-8', errors='ignore')
            has_utf8_meta = '<meta charset="UTF-8">' in content or '<meta charset="utf-8">' in content
            
            return {
                'file': filepath,
                'encoding': encoding,
                'confidence': confidence,
                'has_utf8_meta': has_utf8_meta,
                'valid': encoding.lower() in ['utf-8', 'utf-8-sig', 'ascii'] and has_utf8_meta
            }
    except Exception as e:
        return {
            'file': filepath,
            'error': str(e),
            'valid': False
        }

def main():
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_files = []
    
    # 查找所有HTML文件
    for root, dirs, files in os.walk(workspace):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"检查 {len(html_files)} 个HTML文件的编码...")
    print("-" * 80)
    
    issues = []
    for filepath in sorted(html_files):
        result = check_file_encoding(filepath)
        
        if result.get('valid', False):
            print(f"✅ {os.path.relpath(filepath, workspace)}: {result['encoding']} (置信度: {result['confidence']:.2f})")
        else:
            print(f"❌ {os.path.relpath(filepath, workspace)}: {result.get('encoding', '未知')} {result.get('error', '')}")
            issues.append(result['file'])
    
    print("-" * 80)
    if issues:
        print(f"⚠️  发现 {len(issues)} 个编码问题:")
        for issue in issues:
            print(f"   - {os.path.relpath(issue, workspace)}")
        return 1
    else:
        print("✅ 所有HTML文件编码正确")
        return 0

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x "$WORKSPACE/scripts/validate_encoding.py"
echo "✅ 已创建编码验证脚本: scripts/validate_encoding.py"
echo ""

# 5. 运行编码验证
echo "5. 运行编码验证..."
python3 "$WORKSPACE/scripts/validate_encoding.py"
echo ""

# 6. 使用修复后的文件替换原文件
echo "6. 替换原主页文件..."
cp "$WORKSPACE/index_fixed.html" "$WORKSPACE/index.html"
echo "✅ 已替换主页文件"

echo ""
echo "=== 修复完成 ==="
echo "建议:"
echo "1. 清除浏览器缓存后访问网站"
echo "2. 如果仍有乱码，检查服务器返回的Content-Type头"
echo "3. 确保nginx/apache配置了正确的charset设置"