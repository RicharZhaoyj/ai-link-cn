#!/usr/bin/env python3
"""
批量移除AI工具评测页面中的佣金内容
将所有页面调整为专注于工具价值的内容导向策略
"""

import os
import re
from pathlib import Path

# 要修改的文件列表
TOOL_PAGES = [
    "pages/tools/chatgpt.html",
    "pages/tools/grammarly.html",
    "pages/tools/notion_ai.html",
    "pages/tools/midjourney.html",
    "pages/tools/canva.html",
    "pages/tools/hostinger.html",
    "pages/tools/convertkit.html",
    # jasper.html 和 prowritingaid.html 已经修改过了
]

def remove_affiliate_content(content):
    """
    从HTML内容中移除佣金相关内容
    """
    # 1. 修改CSS类名
    content = content.replace('.affiliate-box {', '.value-box {')
    content = content.replace('class="affiliate-box"', 'class="value-box"')
    
    # 2. 移除标准的佣金说明文本
    affiliate_texts = [
        # 常见的佣金说明
        r'通过我们的Affiliate链接注册，你可能会获得专属优惠。',
        r'通过此链接购买，我们可能获得佣金，不影响您的价格。',
        r'免责声明：通过此链接购买，我们可能获得佣金',
        r'这是一个真实的Affiliate项目',
        r'我正在申请中，获批后会更新购买链接',
        r'💡 提示：这是一个真实的Affiliate项目',
        r'💡 提示：我正在申请中，获批后会更新购买链接',
        r'💡 提示：通过此链接购买，我们可能获得佣金',
        
        # 其他可能的佣金提及
        r'佣金比例[:\s]*\d+%',
        r'佣金.*\d+%',
        r'Affiliate.*佣金',
        r'affiliate.*佣金',
    ]
    
    for pattern in affiliate_texts:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # 3. 替换导航链接中的"赚钱指南"为"价值指南"
    content = content.replace('/pages/affiliate-guide.html">赚钱指南', '/pages/value-guide.html">价值指南')
    content = content.replace('affiliate-guide.html', 'value-guide.html')
    
    # 4. 替换affiliate-box的内容为价值导向内容
    affiliate_box_pattern = r'<div class="value-box"[^>]*>.*?<p>[^<]*?</p>'
    
    # 用更好的内容替换
    new_value_box_content = '''
        <div class="value-box">
            <h3>🎯 为什么选择这个工具？</h3>
            <p>我们专注于提供客观、深入的评测，帮助你了解工具的真正价值，而不是仅仅推荐产品。</p>
        </div>
    '''
    
    content = re.sub(affiliate_box_pattern, new_value_box_content, content, flags=re.DOTALL)
    
    # 5. 添加新的value-box样式
    if '.value-box {' not in content:
        # 在<style>标签中添加value-box样式
        value_box_css = '''
        .value-box { 
            background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
            border-left: 4px solid #3b82f6;
            padding: 1.5rem;
            margin: 2rem 0;
            border-radius: 0 8px 8px 0;
        }
        '''
        content = content.replace('.affiliate-box {', value_box_css + '\n        .affiliate-box {')
    
    return content

def update_navigation_links(content, tool_name):
    """
    更新页面底部的相关工具链接
    """
    # 移除affiliate指南链接
    content = content.replace('affiliate-guide.html">如何通过AI工具赚钱', 'value-guide.html">如何选择AI工具')
    
    # 根据工具类型添加相关工具推荐
    if 'ChatGPT' in tool_name:
        # ChatGPT相关工具
        footer_links = '''
            <p><strong>🔍 更多AI写作工具：</strong></p>
            <p>
                <a href="notion_ai.html">Notion AI评测</a> | 
                <a href="prowritingaid.html">ProWritingAid评测</a> | 
                <a href="jasper.html">Jasper AI评测</a> |
                <a href="../">查看所有工具</a>
            </p>
        '''
    elif 'Grammarly' in tool_name or 'ProWritingAid' in tool_name:
        # 语法检查工具
        footer_links = '''
            <p><strong>🔍 更多英语写作工具：</strong></p>
            <p>
                <a href="grammarly.html">Grammarly评测</a> | 
                <a href="prowritingaid.html">ProWritingAid评测</a> | 
                <a href="chatgpt.html">ChatGPT评测</a> |
                <a href="../">查看所有工具</a>
            </p>
        '''
    elif 'Midjourney' in tool_name:
        # AI图像工具
        footer_links = '''
            <p><strong>🔍 更多AI图像工具：</strong></p>
            <p>
                <a href="canva.html">Canva AI评测</a> | 
                <a href="../">查看所有工具</a>
            </p>
        '''
    else:
        # 默认
        footer_links = '''
            <p><strong>🔍 更多AI工具评测：</strong></p>
            <p>
                <a href="../">查看所有工具</a>
            </p>
        '''
    
    # 找到footer区域并更新
    footer_pattern = r'<footer[^>]*>.*?</footer>'
    new_footer = f'''
        <footer style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e5e7eb;">
            {footer_links}
            <p>本文最后更新: 2026年5月 | 作者: AI.link.cn工具评测团队</p>
            <p><a href="/">返回首页</a> | <a href="../">所有工具评测</a></p>
        </footer>
    '''
    
    content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL)
    
    return content

def main():
    base_dir = Path("/root/.openclaw/workspace")
    
    print("🚀 开始批量移除佣金内容...")
    print("=" * 60)
    
    modified_files = []
    
    for page_path in TOOL_PAGES:
        file_path = base_dir / page_path
        if not file_path.exists():
            print(f"❌ 文件不存在: {page_path}")
            continue
        
        print(f"📄 正在处理: {page_path}")
        
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份原始内容
        original_content = content[:]
        
        # 移除佣金内容
        content = remove_affiliate_content(content)
        
        # 更新导航链接
        tool_name = page_path.split('/')[-1].replace('.html', '').upper()
        content = update_navigation_links(content, tool_name)
        
        # 检查是否有实际修改
        if content != original_content:
            # 写入修改后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            modified_files.append(page_path)
            print(f"  ✅ 已更新: {page_path}")
            
            # 验证佣金内容已移除
            with open(file_path, 'r', encoding='utf-8') as f:
                new_content = f.read()
                if '佣金' in new_content or 'affiliate' in new_content.lower():
                    print(f"  ⚠️  警告: 可能还有佣金内容残留")
        else:
            print(f"  ⏭️  无需修改: {page_path}")
    
    print("=" * 60)
    print(f"📊 批量处理完成:")
    print(f"   总文件数: {len(TOOL_PAGES)}")
    print(f"   已修改文件: {len(modified_files)}")
    
    if modified_files:
        print("\n📋 修改的文件列表:")
        for file in modified_files:
            print(f"   • {file}")
        
        print("\n🎯 下一步操作:")
        print("   1. 提交修改到Git: git add pages/tools/*.html")
        print("   2. 提交: git commit -m '移除所有工具页面的佣金内容'")
        print("   3. 推送到Vercel: git push origin main")
        print("   4. 等待Vercel自动部署")
    else:
        print("\n⚠️  没有文件需要修改。")

if __name__ == "__main__":
    main()