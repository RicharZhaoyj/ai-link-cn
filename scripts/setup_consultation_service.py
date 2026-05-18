#!/usr/bin/env python3
"""
AI.link.cn 咨询服务设置脚本
建立专业的AI工具咨询服务框架
"""

import os
import json
from datetime import datetime

class ConsultationService:
    def __init__(self, workspace_path):
        self.workspace = workspace_path
        self.services_config = {
            "version": "1.0.0",
            "services": [],
            "pricing": {},
            "availability": {},
            "booking_rules": {}
        }
    
    def setup_basic_services(self):
        """设置基础咨询服务"""
        services = [
            {
                "id": "consultation_basic",
                "name": "AI工具选型咨询",
                "description": "60分钟一对一咨询，帮助您选择最适合的AI工具",
                "duration": 60,  # 分钟
                "price": 99.00,
                "currency": "USD",
                "delivery_method": ["video_call", "audio_call"],
                "whats_included": [
                    "需求分析和目标设定",
                    "工具推荐和对比分析", 
                    "成本效益分析",
                    "实施建议和后续步骤",
                    "咨询报告和推荐列表"
                ],
                "target_audience": ["个人用户", "小团队", "创业者"],
                "prerequisites": ["准备好工具使用需求描述"],
                "status": "active",
                "created": datetime.now().isoformat()
            },
            {
                "id": "consultation_team",
                "name": "团队AI工具部署咨询",
                "description": "90分钟团队咨询，制定团队AI工具部署方案",
                "duration": 90,
                "price": 199.00,
                "currency": "USD",
                "delivery_method": ["video_call", "onsite_workshop"],
                "whats_included": [
                    "团队需求分析和工作流评估",
                    "团队协作工具推荐",
                    "部署路线图制定",
                    "培训计划设计",
                    "ROI分析和预算规划",
                    "实施支持计划"
                ],
                "target_audience": ["中小企业", "创业团队", "部门管理者"],
                "prerequisites": ["团队成员名单", "现有工作流描述", "预算范围"],
                "status": "active",
                "created": datetime.now().isoformat()
            },
            {
                "id": "consultation_enterprise",
                "name": "企业AI战略咨询",
                "description": "深度企业咨询，制定全面的AI工具战略",
                "duration": 120,
                "price": 499.00,
                "currency": "USD",
                "delivery_method": ["video_call", "onsite_consultation"],
                "whats_included": [
                    "企业AI成熟度评估",
                    "战略规划和目标设定",
                    "工具选型和供应商评估",
                    "实施路线图和风险管理",
                    "ROI模型和投资回报分析",
                    "团队培训和发展计划",
                    "后续跟进和支持"
                ],
                "target_audience": ["企业决策者", "技术总监", "创新部门"],
                "prerequisites": ["企业概况", "战略目标", "现有技术栈"],
                "status": "active",
                "created": datetime.now().isoformat()
            },
            {
                "id": "audit_comprehensive",
                "name": "AI工具使用全面审计",
                "description": "对现有AI工具使用情况进行全面审计和优化建议",
                "duration": 0,  # 按项目定价
                "price": 799.00,
                "currency": "USD",
                "delivery_method": ["remote_audit", "report_delivery"],
                "whats_included": [
                    "现有工具使用情况评估",
                    "效率和成本分析",
                    "工具整合和优化建议",
                    "替代方案分析",
                    "详细审计报告",
                    "实施建议和预算规划"
                ],
                "target_audience": ["已使用AI工具的企业", "希望优化的团队"],
                "prerequisites": ["现有工具列表", "使用数据", "团队反馈"],
                "status": "active",
                "created": datetime.now().isoformat()
            }
        ]
        
        self.services_config["services"] = services
        return services
    
    def setup_pricing_packages(self):
        """设置定价套餐"""
        packages = {
            "individual": {
                "name": "个人咨询套餐",
                "price": 249.00,
                "currency": "USD",
                "includes": [
                    "2次基础咨询",
                    "1次工具审计",
                    "邮件支持30天",
                    "工具推荐库访问"
                ],
                "savings": "节省$48 (16%)",
                "popular": True
            },
            "team": {
                "name": "团队咨询套餐",
                "price": 699.00,
                "currency": "USD",
                "includes": [
                    "1次团队咨询",
                    "2次基础咨询",
                    "团队工作流分析",
                    "实施支持60天"
                ],
                "savings": "节省$98 (12%)",
                "popular": False
            },
            "enterprise": {
                "name": "企业年度咨询",
                "price": 2999.00,
                "currency": "USD",
                "includes": [
                    "4次企业咨询",
                    "全面工具审计",
                    "季度战略回顾",
                    "优先技术支持",
                    "团队培训工作坊"
                ],
                "savings": "节省$996 (25%)",
                "popular": False
            }
        }
        
        self.services_config["pricing"] = packages
        return packages
    
    def create_booking_system(self):
        """创建预约系统页面"""
        booking_page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI工具咨询服务预约 - AI.link.cn</title>
    <meta name="description" content="专业AI工具咨询服务，帮助您选择、部署和优化AI工具。一对一咨询，定制化解决方案。">
    
    <!-- Open Graph -->
    <meta property="og:title" content="AI工具咨询服务 - AI.link.cn">
    <meta property="og:description" content="专业的AI工具咨询，帮助您最大化AI投资回报。">
    
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        .header {{
            text-align: center;
            margin-bottom: 4rem;
        }}
        .main-title {{
            font-size: 3rem;
            color: #2563eb;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{
            font-size: 1.2rem;
            color: #6b7280;
            max-width: 800px;
            margin: 0 auto;
        }}
        .services-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 4rem;
        }}
        .service-card {{
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            position: relative;
            border: 2px solid transparent;
        }}
        .service-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.1);
            border-color: #3b82f6;
        }}
        .service-card.popular {{
            border-color: #10b981;
        }}
        .popular-badge {{
            position: absolute;
            top: -10px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 0.25rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: bold;
        }}
        .service-title {{
            font-size: 1.5rem;
            color: #1e293b;
            margin-bottom: 1rem;
        }}
        .service-price {{
            font-size: 2rem;
            font-weight: bold;
            color: #3b82f6;
            margin: 1rem 0;
        }}
        .service-duration {{
            color: #6b7280;
            margin-bottom: 1.5rem;
        }}
        .feature-list {{
            list-style: none;
            padding: 0;
            margin: 1.5rem 0;
        }}
        .feature-list li {{
            margin: 0.75rem 0;
            padding-left: 1.5rem;
            position: relative;
        }}
        .feature-list li:before {{
            content: '✓';
            color: #10b981;
            font-weight: bold;
            position: absolute;
            left: 0;
        }}
        .cta-button {{
            display: block;
            text-align: center;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            margin-top: 1.5rem;
            transition: all 0.3s;
        }}
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(59, 130, 246, 0.3);
        }}
        .packages-section {{
            margin: 4rem 0;
            background: white;
            border-radius: 15px;
            padding: 3rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }}
        .section-title {{
            text-align: center;
            font-size: 2rem;
            color: #1e293b;
            margin-bottom: 3rem;
        }}
        .packages-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }}
        .package-card {{
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
        }}
        .package-card.popular {{
            border-color: #3b82f6;
            background: linear-gradient(135deg, #f8fafc, #e0f2fe);
        }}
        .process-section {{
            margin: 4rem 0;
        }}
        .process-steps {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }}
        .process-step {{
            text-align: center;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .step-number {{
            display: inline-block;
            width: 40px;
            height: 40px;
            background: #3b82f6;
            color: white;
            border-radius: 50%;
            line-height: 40px;
            font-weight: bold;
            margin-bottom: 1rem;
        }}
        .faq-section {{
            margin: 4rem 0;
        }}
        .faq-item {{
            margin: 1.5rem 0;
            padding: 1.5rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .faq-question {{
            font-weight: bold;
            color: #1e293b;
            margin-bottom: 0.5rem;
        }}
        .footer {{
            text-align: center;
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #e5e7eb;
            color: #6b7280;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="main-title">AI工具专业咨询服务</h1>
            <p class="subtitle">帮助个人、团队和企业选择、部署和优化AI工具，最大化您的AI投资回报。</p>
        </div>
        
        <div class="services-grid">
            <!-- 基础咨询 -->
            <div class="service-card">
                <h2 class="service-title">AI工具选型咨询</h2>
                <div class="service-price">$99</div>
                <div class="service-duration">60分钟 · 一对一咨询</div>
                <ul class="feature-list">
                    <li>需求分析和目标设定</li>
                    <li>工具推荐和对比分析</li>
                    <li>成本效益分析</li>
                    <li>实施建议和后续步骤</li>
                    <li>咨询报告和推荐列表</li>
                </ul>
                <a href="#booking" class="cta-button">立即预约</a>
            </div>
            
            <!-- 团队咨询 -->
            <div class="service-card">
                <h2 class="service-title">团队部署咨询</h2>
                <div class="service-price">$199</div>
                <div class="service-duration">90分钟 · 团队咨询</div>
                <ul class="feature-list">
                    <li>团队需求和工作流评估</li>
                    <li>团队协作工具推荐</li>
                    <li>部署路线图制定</li>
                    <li>培训计划设计</li>
                    <li>ROI分析和预算规划</li>
                    <li>实施支持计划</li>
                </ul>
                <a href="#booking" class="cta-button">立即预约</a>
            </div>
            
            <!-- 企业咨询 -->
            <div class="service-card popular">
                <div class="popular-badge">最受欢迎</div>
                <h2 class="service-title">企业战略咨询</h2>
                <div class="service-price">$499</div>
                <div class="service-duration">120分钟 · 深度咨询</div>
                <ul class="feature-list">
                    <li>企业AI成熟度评估</li>
                    <li>战略规划和目标设定</li>
                    <li>工具选型和供应商评估</li>
                    <li>实施路线图和风险管理</li>
                    <li>ROI模型和投资回报分析</li>
                    <li>团队培训和发展计划</li>
                    <li>后续跟进和支持</li>
                </ul>
                <a href="#booking" class="cta-button">立即预约</a>
            </div>
        </div>
        
        <div class="packages-section">
            <h2 class="section-title">咨询套餐计划</h2>
            <div class="packages-grid">
                <div class="package-card">
                    <h3>个人咨询套餐</h3>
                    <div class="service-price">$249</div>
                    <p>节省 $48 (16%)</p>
                    <ul class="feature-list">
                        <li>2次基础咨询</li>
                        <li>1次工具审计</li>
                        <li>邮件支持30天</li>
                        <li>工具推荐库访问</li>
                    </ul>
                </div>
                
                <div class="package-card popular">
                    <h3>团队咨询套餐</h3>
                    <div class="service-price">$699</div>
                    <p>节省 $98 (12%)</p>
                    <ul class="feature-list">
                        <li>1次团队咨询</li>
                        <li>2次基础咨询</li>
                        <li>团队工作流分析</li>
                        <li>实施支持60天</li>
                    </ul>
                </div>
                
                <div class="package-card">
                    <h3>企业年度咨询</h3>
                    <div class="service-price">$2,999</div>
                    <p>节省 $996 (25%)</p>
                    <ul class="feature-list">
                        <li>4次企业咨询</li>
                        <li>全面工具审计</li>
                        <li>季度战略回顾</li>
                        <li>优先技术支持</li>
                        <li>团队培训工作坊</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="process-section">
            <h2 class="section-title">咨询流程</h2>
            <div class="process-steps">
                <div class="process-step">
                    <div class="step-number">1</div>
                    <h3>需求评估</h3>
                    <p>填写需求问卷，了解您的具体需求和目标</p>
                </div>
                <div class="process-step">
                    <div class="step-number">2</div>
                    <h3>预约咨询</h3>
                    <p>选择适合的咨询服务和时间，完成预约支付</p>
                </div>
                <div class="process-step">
                    <div class="step-number">3</div>
                    <h3>咨询会议</h3>
                    <p>进行一对一咨询，深入分析您的情况</p>
                </div>
                <div class="process-step">
                    <div class="step-number">4</div>
                    <h3>交付报告</h3>
                    <p>收到详细的咨询报告和建议方案</p>
                </div>
                <div class="process-step">
                    <div class="step-number">5</div>
                    <h3>后续支持</h3>
                    <p>获得实施支持和问题解答</p>
                </div>
            </div>
        </div>
        
        <div class="faq-section">
            <h2 class="section-title">常见问题</h2>
            
            <div class="faq-item">
                <div class="faq-question">咨询需要准备什么？</div>
                <p>建议准备好您的具体需求描述、预算范围、团队情况（如果是团队咨询）、现有工具使用情况等。我们会提供详细的需求问卷。</p>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">咨询如何进行？</div>
                <p>主要通过视频会议（Zoom/Google Meet）进行，也可以提供现场咨询（额外费用）。咨询前会发送会议链接和准备材料。</p>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">咨询后有后续支持吗？</div>
                <p>是的，所有咨询都包含7天的邮件支持。团队和企业咨询包含更长的支持期。也可以购买额外的支持服务。</p>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">如何保证咨询质量？</div>
                <p>我们提供100%满意度保证。如果对咨询不满意，可以在7天内申请全额退款。我们拥有丰富的AI工具经验和成功案例。</p>
            </div>
            
            <div class="faq-item">
                <div class="faq-question">可以定制咨询内容吗？</div>
                <p>是的，我们提供完全定制化的咨询服务。请通过邮件或预约系统与我们联系，讨论您的具体需求。</p>
            </div>
        </div>
        
        <div id="booking" style="text-align: center; margin: 4rem 0;">
            <h2 class="section-title">立即预约咨询</h2>
            <p style="margin-bottom: 2rem;">选择适合您的咨询服务，开始AI工具优化之旅</p>
            
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 3rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
                <h3>预约系统即将上线</h3>
                <p>我们正在集成专业的预约系统，很快将开放预约功能。</p>
                <p>在此期间，请通过以下方式联系我们：</p>
                
                <div style="margin-top: 2rem;">
                    <p><strong>📧 邮箱:</strong> contact@ai-link.cn</p>
                    <p><strong>📱 电话:</strong> +86 138 0013 8000</p>
                    <p><strong>💬 微信:</strong> AI_link_cn</p>
                </div>
                
                <div style="margin-top: 2rem; padding: 1.5rem; background: #f0f9ff; border-radius: 8px;">
                    <p><strong>💡 预约提醒:</strong> 发送邮件时请注明：</p>
                    <ul style="text-align: left; padding-left: 1.5rem;">
                        <li>您的具体需求</li>
                        <li>希望咨询的服务类型</li>
                        <li>可预约的时间段</li>
                        <li>团队规模（如果是团队咨询）</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2026 AI.link.cn - 专业的AI工具评测和咨询平台</p>
            <p>所有咨询服务均由经验丰富的AI专家提供，基于真实案例和最佳实践</p>
        </div>
    </div>
</body>
</html>"""
        
        # 保存预约页面
        booking_page_path = os.path.join(self.workspace, "pages", "consultation", "index.html")
        os.makedirs(os.path.dirname(booking_page_path), exist_ok=True)
        
        with open(booking_page_path, 'w', encoding='utf-8') as f:
            f.write(booking_page)
        
        return booking_page_path
    
    def save_configuration(self):
        """保存服务配置"""
        # 更新配置时间
        self.services_config["updated_at"] = datetime.now().isoformat()
        
        # 保存到文件
        config_dir = os.path.join(self.workspace, "config", "services")
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, "consultation_services.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.services_config, f, ensure_ascii=False, indent=2)
        
        return config_file
    
    def run(self):
        """运行设置流程"""
        print("🎯 设置AI.link.cn咨询服务系统")
        print("=" * 50)
        
        # 1. 设置基础服务
        print("1. 设置基础咨询服务...")
        services = self.setup_basic_services()
        print(f"   ✅ 创建 {len(services)} 个服务项目")
        
        # 2. 设置定价套餐
        print("2. 设置定价套餐...")
        packages = self.setup_pricing_packages()
        print(f"   ✅ 创建 {len(packages)} 个套餐计划")
        
        # 3. 创建预约系统
        print("3. 创建预约系统页面...")
        booking_page = self.create_booking_system()
        print(f"   ✅ 预约页面: {booking_page}")
        
        # 4. 保存配置
        print("4. 保存服务配置...")
        config_file = self.save_configuration()
        print(f"   ✅ 配置文件: {config_file}")
        
        # 5. 创建文档
        print("5. 创建咨询流程文档...")
        docs_file = self.create_documentation()
        print(f"   ✅ 文档文件: {docs_file}")
        
        print("=" * 50)
        print("🎉 咨询服务系统设置完成!")
        print("")
        print("🚀 下一步操作:")
        print("   1. 完善咨询页面内容")
        print("   2. 设置支付系统 (Stripe/PayPal)")
        print("   3. 集成预约系统 (Calendly/Acuity)")
        print("   4. 创建咨询材料模板")
        print("   5. 开始市场推广")
        
        return {
            "services": services,
            "packages": packages,
            "booking_page": booking_page,
            "config_file": config_file
        }
    
    def create_documentation(self):
        """创建咨询流程文档"""
        docs_content = """# AI.link.cn 咨询服务操作手册

## 📋 服务概览

### 提供的服务类型
1. **基础咨询** ($99) - 60分钟一对一咨询
2. **团队咨询** ($199) - 90分钟团队咨询  
3. **企业咨询** ($499) - 120分钟深度咨询
4. **全面审计** ($799) - 工具使用情况审计

### 目标客户
- **个人用户**: 自由职业者、内容创作者、个人开发者
- **小团队**: 创业团队、中小型企业部门
- **企业客户**: 技术决策者、创新部门负责人

## 📅 咨询流程

### 阶段1: 预约前准备
1. **客户填写需求问卷**
   - 基本信息收集
   - 具体需求描述
   - 预算和期望目标

2. **初步评估**
   - 评估咨询可行性
   - 推荐适合的服务类型
   - 提供初步建议

### 阶段2: 咨询预约
1. **选择服务类型和时间**
2. **完成支付确认**
3. **发送预约确认邮件**
   - 会议链接和时间
   - 准备材料清单
   - 咨询前阅读材料

### 阶段3: 咨询执行
1. **会前准备** (15分钟)
   - 查看客户问卷
   - 准备初步分析
   - 准备推荐列表

2. **咨询会议** (60-120分钟)
   - 需求深入讨论
   - 工具推荐和对比
   - 方案制定
   - 问答环节

3. **会后跟进** (30分钟)
   - 整理会议记录
   - 准备咨询报告
   - 发送给客户

### 阶段4: 报告交付
1. **咨询报告包含**:
   - 需求分析总结
   - 推荐工具列表（含优缺点）
   - 实施路线图
   - 成本效益分析
   - 后续步骤建议

2. **报告交付时间**: 咨询后24小时内

### 阶段5: 后续支持
1. **7天邮件支持**: 回答实施问题
2. **可选延长支持**: 30天/60天支持计划
3. **定期跟进**: 重要客户月度跟进

## 💼 咨询材料模板

### 需求问卷模板
```markdown
# AI工具咨询需求问卷

## 基本信息
- 姓名/公司: _______
- 邮箱: _______
- 电话: _______

## 当前情况
1. 目前使用哪些AI工具?
2. 主要使用场景是什么?
3. 遇到的主要问题或挑战?

## 目标需求
1. 希望通过咨询解决什么问题?
2. 预算范围是多少?
3. 期望的时间框架?

## 团队情况（如适用）
1. 团队规模: _______
2. 技术背景: _______
3. 协作需求: _______
```

### 咨询报告模板
```markdown
# AI工具咨询报告

## 客户信息
- 客户: _______
- 咨询日期: _______
- 咨询类型: _______

## 需求分析总结
[客户需求总结]

## 推荐方案
### 1. 核心推荐工具
[工具1]: 优缺点分析
[工具2]: 优缺点分析

### 2. 实施路线图
阶段1: [时间] - [任务]
阶段2: [时间] - [任务]

### 3. 成本效益分析
投资成本: $_______
预期收益: $_______
ROI周期: _______

## 后续步骤建议
1. 立即行动项
2. 中期计划
3. 长期规划
```

## 💰 定价和收费

### 收费标准
1. **基础咨询**: $99 (60分钟)
2. **团队咨询**: $199 (90分钟)  
3. **企业咨询**: $499 (120分钟)
4. **全面审计**: $799 (按项目)

### 支付方式
1. **在线支付**: Stripe/PayPal
2. **企业支付**: 银行转账/发票
3. **套餐支付**: 预付费套餐

### 退款政策
1. **100%满意度保证**: 咨询后7天内可申请退款
2. **取消政策**: 预约前24小时可免费取消
3. **改期政策**: 提前12小时可免费改期

## 🛠️ 技术工具

### 咨询工具栈
1. **预约系统**: Calendly/Acuity Scheduling
2. **视频会议**: Zoom/Google Meet
3. **文档协作**: Google Docs/Notion
4. **支付系统**: Stripe/PayPal
5. **CRM系统**: HubSpot/Notion

### 分析工具
1. **工具对比**: 自研对比分析工具
2. **成本计算**: ROI计算器
3. **方案生成**: 自动报告生成器

## 📈 质量保证

### 咨询师资质
1. **AI工具专家**: 3年以上AI工具使用经验
2. **行业认证**: 相关技术认证
3. **案例经验**: 成功咨询案例

### 质量控制
1. **标准化流程**: 统一的咨询流程
2. **质量检查**: 报告审核机制
3. **客户反馈**: 满意度调查

### 持续改进
1. **案例复盘**: 每月案例复盘会
2. **知识更新**: 每月工具更新学习
3. **流程优化**: 基于反馈持续优化

---

**版本**: 1.0.0  
**更新日期**: 2026年5月18日  
**下一次更新**: 2026年6月18日
"""
        
        docs_file = os.path.join(self.workspace, "docs", "consultation_operations.md")
        os.makedirs(os.path.dirname(docs_file), exist_ok=True)
        
        with open(docs_file, 'w', encoding='utf-8') as f:
            f.write(docs_content)
        
        return docs_file

def main():
    """主函数"""
    workspace = "/root/.openclaw/workspace"
    service = ConsultationService(workspace)
    results = service.run()
    
    print(f"\n📊 设置完成统计:")
    print(f"   咨询服务: {len(results['services'])} 个")
    print(f"   套餐计划: {len(results['packages'])} 个")
    print(f"   预约页面: {results['booking_page']}")
    print(f"   配置文件: {results['config_file']}")
    
    print(f"\n💡 立即测试:")
    print(f"   1. 查看预约页面: pages/consultation/index.html")
    print(f"   2. 查看服务配置: config/services/consultation_services.json")
    print(f"   3. 查看操作手册: docs/consultation_operations.md")

if __name__ == "__main__":
    main()