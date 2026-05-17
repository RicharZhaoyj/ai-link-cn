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
