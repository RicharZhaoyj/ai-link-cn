#!/usr/bin/env python3
"""
验证GitHub仓库替换是否成功
"""

import os
import json
import subprocess
import sys

def print_header(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def check_file_exists(path, description):
    if os.path.exists(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: 文件不存在")
        return False

def read_json_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"  读取失败: {e}")
        return None

def main():
    print_header("GitHub仓库替换验证")
    
    # 1. 检查核心文件
    print("\n📁 1. 核心文件检查:")
    essential_files = [
        ("package.json", "Node.js项目配置"),
        ("README.md", "项目说明文档"),
        ("REPLACE_GUIDE.md", "替换指南"),
        ("PROJECT_SUMMARY.json", "项目总结"),
        ("vercel.json", "Vercel部署配置"),
        ("CNAME", "自定义域名配置"),
    ]
    
    all_essential = True
    for file_path, description in essential_files:
        if not check_file_exists(file_path, description):
            all_essential = False
    
    # 2. 检查目录结构
    print("\n📁 2. 目录结构检查:")
    essential_dirs = [
        ("config/", "配置文件目录"),
        ("src/", "源代码目录"),
        ("docs/", "文档目录"),
        ("scripts/", "脚本目录"),
    ]
    
    for dir_path, description in essential_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ {description}: {dir_path}")
            # 列出目录内容
            files = os.listdir(dir_path)
            for file in files[:3]:  # 显示前3个文件
                print(f"   - {file}")
            if len(files) > 3:
                print(f"   ... 共 {len(files)} 个文件")
        else:
            print(f"❌ {description}: 目录不存在")
            all_essential = False
    
    # 3. 检查配置文件
    print("\n⚙️ 3. 配置文件检查:")
    config_files = [
        ("config/affiliate_links.json", "Affiliate链接配置"),
        ("config/tools_list.json", "AI工具列表"),
        ("config/seo_keywords.json", "SEO关键词配置"),
    ]
    
    for file_path, description in config_files:
        if check_file_exists(file_path, description):
            data = read_json_file(file_path)
            if data:
                if "links" in data or "categories" in data:
                    print(f"   ✓ 配置有效，包含关键数据")
    
    # 4. 检查源代码
    print("\n💻 4. 源代码检查:")
    src_files = [
        ("src/ai_tools_scraper.js", "AI工具数据收集器"),
        ("src/affiliate_tracker.js", "Affiliate管理系统"),
        ("src/content_generator.js", "内容生成器"),
    ]
    
    for file_path, description in src_files:
        if check_file_exists(file_path, description):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    print(f"   ✓ {lines} 行代码")
            except:
                pass
    
    # 5. 检查脚本
    print("\n🛠️ 5. 脚本检查:")
    if check_file_exists("scripts/deploy.sh", "部署脚本"):
        try:
            with open("scripts/deploy.sh", 'r', encoding='utf-8') as f:
                content = f.read()
                if "#!/bin/bash" in content:
                    print("   ✓ 包含正确的shebang")
                if "deploy_vercel" in content:
                    print("   ✓ 包含Vercel部署功能")
                if "deploy_github" in content:
                    print("   ✓ 包含GitHub Pages部署功能")
        except:
            pass
    
    # 6. 检查Git状态
    print("\n🔧 6. Git状态检查:")
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-3"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            print("最近提交:")
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")
        else:
            print("  无法获取Git日志")
    except:
        print("  Git命令执行失败")
    
    # 7. 验证项目配置
    print("\n📊 7. 项目配置验证:")
    if os.path.exists("PROJECT_SUMMARY.json"):
        data = read_json_file("PROJECT_SUMMARY.json")
        if data:
            print(f"   项目名称: {data.get('project_name', '未知')}")
            print(f"   版本: {data.get('version', '未知')}")
            print(f"   描述: {data.get('description', '未知')[:80]}...")
            if "income_projection" in data:
                year1 = data["income_projection"].get("year_1", {})
                if year1:
                    print(f"   第1年收入预测: ${year1.get('annual_income', '未知')}")
    
    # 8. 总结
    print_header("替换验证总结")
    
    if all_essential:
        print("🎉 替换成功！所有核心文件都存在。")
        print("\n下一步操作:")
        print("1. 部署网站: chmod +x scripts/deploy.sh && ./scripts/deploy.sh --setup")
        print("2. 申请Affiliate: 阅读 docs/affiliate_guide.md")
        print("3. 生成内容: node src/content_generator.js review \"ChatGPT\"")
        print("4. 开始推广: 使用SEO关键词优化内容")
    else:
        print("⚠️ 替换可能不完整，某些文件缺失。")
        print("\n建议:")
        print("1. 检查备份目录: ls -la backup-old-project/")
        print("2. 重新执行替换步骤")
        print("3. 联系技术支持")
    
    # 9. 检查备份
    print("\n📦 8. 备份检查:")
    if os.path.exists("backup-old-project"):
        backup_files = len(os.listdir("backup-old-project"))
        print(f"✅ 旧项目备份存在，包含 {backup_files} 个文件/目录")
        print("   如果需要恢复旧文件，可以从 backup-old-project/ 复制")
    else:
        print("⚠️ 备份目录不存在")

if __name__ == "__main__":
    main()