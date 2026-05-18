#!/usr/bin/env python3
"""
CSS优化脚本
压缩CSS文件，添加缓存头
"""

import os
import re
from datetime import datetime

def compress_css(css_content):
    """简单的CSS压缩"""
    # 移除注释
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # 移除空白字符
    css_content = re.sub(r'\s+', ' ', css_content)
    css_content = re.sub(r'\s*{\s*', '{', css_content)
    css_content = re.sub(r'\s*}\s*', '}', css_content)
    css_content = re.sub(r'\s*:\s*', ':', css_content)
    css_content = re.sub(r'\s*;\s*', ';', css_content)
    css_content = re.sub(r'\s*,\s*', ',', css_content)
    
    # 移除最后一个分号
    css_content = re.sub(r';}', '}', css_content)
    
    return css_content.strip()

def main():
    workspace = "/root/.openclaw/workspace"
    css_dir = os.path.join(workspace, "css")
    
    if not os.path.exists(css_dir):
        print("❌ CSS目录不存在")
        return
    
    # 查找所有CSS文件
    css_files = []
    for root, dirs, files in os.walk(css_dir):
        for file in files:
            if file.endswith('.css') and not file.endswith('.min.css'):
                css_files.append(os.path.join(root, file))
    
    if not css_files:
        print("✅ 没有需要优化的CSS文件")
        return
    
    print(f"🔧 开始优化CSS文件...")
    print(f"找到 {len(css_files)} 个CSS文件")
    
    optimized_count = 0
    for css_file in css_files:
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                original = f.read()
            
            original_size = len(original.encode('utf-8'))
            
            # 压缩CSS
            compressed = compress_css(original)
            compressed_size = len(compressed.encode('utf-8'))
            
            # 计算压缩率
            reduction = original_size - compressed_size
            reduction_percent = (reduction / original_size) * 100 if original_size > 0 else 0
            
            # 创建.min.css文件
            base_name = os.path.splitext(css_file)[0]
            min_file = f"{base_name}.min.css"
            
            with open(min_file, 'w', encoding='utf-8') as f:
                f.write(compressed)
            
            optimized_count += 1
            
            print(f"✅ {os.path.basename(css_file)}")
            print(f"   原始: {original_size:,} 字节")
            print(f"   压缩: {compressed_size:,} 字节")
            print(f"   节省: {reduction:,} 字节 ({reduction_percent:.1f}%)")
            
            # 创建缓存头文件 (对于静态服务器)
            cache_file = f"{css_file}.cache-header.txt"
            cache_content = f"""# 缓存头配置
# 文件: {os.path.basename(css_file)}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Nginx配置
location ~* \\.(css)$ {{
    expires 30d;
    add_header Cache-Control "public, immutable";
}}

# Apache配置
<FilesMatch "\\.(css)$">
    ExpiresActive On
    ExpiresDefault "access plus 30 days"
    Header set Cache-Control "public, immutable"
</FilesMatch>
"""
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(cache_content)
                
        except Exception as e:
            print(f"❌ 处理 {css_file} 时出错: {e}")
    
    print(f"\n🎉 优化完成:")
    print(f"   总共优化: {optimized_count}/{len(css_files)} 个文件")
    print(f"\n💡 建议:")
    print(f"   1. 在生产环境中使用 .min.css 文件")
    print(f"   2. 配置服务器缓存头 (参见 .cache-header.txt 文件)")
    print(f"   3. 考虑启用GZIP/Brotli压缩")

if __name__ == "__main__":
    main()