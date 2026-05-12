#!/usr/bin/env node
/**
 * 更新网站链接脚本
 * 将所有占位符链接替换为实际链接
 */

const fs = require('fs').promises;
const path = require('path');

// 实际Affiliate链接 (申请后需要更新)
const AFFILIATE_LINKS = {
  'chatgpt': 'https://chat.openai.com/?ref=ailink',
  'midjourney': 'https://www.midjourney.com/?ref=ailink',
  'grammarly': 'https://www.grammarly.com/?ref=ailink',
  'notion_ai': 'https://www.notion.so/product/ai?ref=ailink',
  'jasper_ai': 'https://www.jasper.ai/?ref=ailink',
  'canva': 'https://www.canva.com/?ref=ailink',
  'convertkit': 'https://convertkit.com/?ref=ailink',
  'hostinger': 'https://www.hostinger.com/?ref=ailink'
};

// 工具官方链接
const OFFICIAL_LINKS = {
  'chatgpt': 'https://chat.openai.com/',
  'midjourney': 'https://www.midjourney.com/',
  'grammarly': 'https://www.grammarly.com/',
  'notion_ai': 'https://www.notion.so/product/ai',
  'jasper_ai': 'https://www.jasper.ai/',
  'canva': 'https://www.canva.com/',
  'convertkit': 'https://convertkit.com/',
  'hostinger': 'https://www.hostinger.com/',
  'github_copilot': 'https://github.com/features/copilot',
  'dalle': 'https://openai.com/dall-e-3'
};

async function updateFile(filePath, replacements) {
  try {
    let content = await fs.readFile(filePath, 'utf-8');
    let updated = false;
    
    for (const [placeholder, actual] of Object.entries(replacements)) {
      if (content.includes(placeholder)) {
        content = content.replace(new RegExp(placeholder, 'g'), actual);
        updated = true;
      }
    }
    
    if (updated) {
      await fs.writeFile(filePath, content, 'utf-8');
      console.log(`✅ 已更新: ${filePath}`);
    } else {
      console.log(`ℹ️  无变化: ${filePath}`);
    }
  } catch (error) {
    console.log(`❌ 更新失败 ${filePath}: ${error.message}`);
  }
}

async function createToolPage(toolName, toolData) {
  const pageContent = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${toolData.name}评测 - AI.link.cn</title>
    <meta name="description" content="${toolData.description}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        .container { max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }
        .affiliate-box { background: #f0f9ff; border-left: 4px solid #3b82f6; padding: 1.5rem; margin: 2rem 0; }
        .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }
        .info-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <nav class="container">
        <ul><li><strong><a href="/" style="color: inherit; text-decoration: none;">AI.link.cn</a></strong></li></ul>
        <ul>
            <li><a href="/">首页</a></li>
            <li><a href="/pages/tools/">所有工具</a></li>
            <li><a href="/pages/affiliate-guide.html">赚钱指南</a></li>
        </ul>
    </nav>

    <div class="container">
        <h1>${toolData.name}评测</h1>
        
        <div class="affiliate-box">
            <h3>💎 通过我们的链接注册</h3>
            <p>通过我们的Affiliate链接注册，你可能会获得专属优惠。</p>
            <a href="${AFFILIATE_LINKS[toolData.id] || OFFICIAL_LINKS[toolData.id]}" 
               target="_blank" 
               style="background: #10b981; color: white; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; display: inline-block;">
                🚀 立即体验${toolData.name}
            </a>
            <p><small>免责声明：通过此链接购买，我们可能获得佣金，不影响您的价格。</small></p>
        </div>

        <div class="info-grid">
            <div class="info-card">
                <h4>💰 定价</h4>
                <p>${toolData.pricing}</p>
            </div>
            <div class="info-card">
                <h4>🎯 适合人群</h4>
                <p>${toolData.audience}</p>
            </div>
            <div class="info-card">
                <h4>⭐ 评分</h4>
                <p>${toolData.rating}</p>
            </div>
        </div>

        <h2>详细介绍</h2>
        <p>${toolData.detailedDescription || toolData.description}</p>

        <h2>主要功能</h2>
        <ul>
            ${toolData.features.map(f => `<li>${f}</li>`).join('\n')}
        </ul>

        <h2>使用建议</h2>
        <p>${toolData.usageTips}</p>

        <footer style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e5e7eb;">
            <p>本文最后更新: 2025年5月12日</p>
            <p><a href="/">返回首页</a> | <a href="/pages/tools/">所有工具评测</a></p>
        </footer>
    </div>
</body>
</html>
  `.trim();

  const pagePath = path.join(__dirname, 'pages', 'tools', `${toolData.id}.html`);
  await fs.mkdir(path.dirname(pagePath), { recursive: true });
  await fs.writeFile(pagePath, pageContent, 'utf-8');
  console.log(`📄 已创建: ${pagePath}`);
}

async function main() {
  console.log('🔧 开始更新网站链接...\n');

  // 1. 更新首页链接
  console.log('1. 更新首页链接...');
  await updateFile('index.html', {
    'href="#"': 'href="/pages/tools/"',
    '查看评测': 'href="/pages/tools/"',
    '立即体验': 'href="/pages/tools/"'
  });

  // 2. 更新工具列表页
  console.log('\n2. 更新工具列表页...');
  await updateFile('pages/tools/index.html', {
    'href="#"': 'href="/pages/tools/"',
    '/tools/chatgpt.html': '/pages/tools/chatgpt.html',
    '/tools/jasper.html': '/pages/tools/jasper.html',
    '/tools/grammarly.html': '/pages/tools/grammarly.html',
    '/tools/notion-ai.html': '/pages/tools/notion_ai.html',
    '/tools/midjourney.html': '/pages/tools/midjourney.html',
    '/tools/dalle.html': '/pages/tools/dalle.html',
    '/tools/canva-ai.html': '/pages/tools/canva.html',
    '/tools/copilot.html': '/pages/tools/copilot.html',
    '/tools/codewhisperer.html': '/pages/tools/codewhisperer.html'
  });

  // 3. 创建缺失的工具页面
  console.log('\n3. 创建缺失的工具页面...');
  
  const tools = [
    {
      id: 'chatgpt',
      name: 'ChatGPT',
      description: 'OpenAI的对话式AI助手',
      pricing: '免费版可用，Plus版$20/月',
      audience: '内容创作者、学生、开发者',
      rating: '9/10',
      features: ['智能对话', '内容创作', '编程辅助', '多语言支持'],
      usageTips: '给出明确的指令，分步骤询问复杂问题'
    },
    {
      id: 'midjourney',
      name: 'Midjourney',
      description: '高质量的AI图像生成工具',
      pricing: '$10-60/月（按GPU时间）',
      audience: '设计师、艺术家、内容创作者',
      rating: '9.2/10',
      features: ['高质量图像生成', '多种艺术风格', '通过Discord使用', '社区活跃'],
      usageTips: '学习prompt工程，多尝试不同参数'
    },
    {
      id: 'grammarly',
      name: 'Grammarly',
      description: 'AI语法检查和写作改进工具',
      pricing: '免费版可用，高级版$12/月',
      audience: '写作者、学生、商务人士',
      rating: '8.8/10',
      features: ['语法检查', '拼写纠正', '写作风格建议', '抄袭检测'],
      usageTips: '安装浏览器插件，实时检查所有写作'
    },
    {
      id: 'notion_ai',
      name: 'Notion AI',
      description: '集成在Notion中的AI写作和摘要工具',
      pricing: '$10/月（附加在Notion订阅上）',
      audience: '团队、学生、知识工作者',
      rating: '8.5/10',
      features: ['智能写作', '内容摘要', '头脑风暴', '翻译功能'],
      usageTips: '结合Notion数据库使用，最大化工作效率'
    }
  ];

  for (const tool of tools) {
    await createToolPage(tool.id, tool);
  }

  // 4. 更新赚钱指南页
  console.log('\n4. 更新赚钱指南页...');
  await updateFile('pages/affiliate-guide.html', {
    '/docs/affiliate_guide.md': 'https://github.com/RicharZhaoyj/ai-link-cn/blob/main/docs/affiliate_guide.md',
    'https://chat.openai.com/?ref=ailink': AFFILIATE_LINKS.chatgpt,
    'https://www.midjourney.com/?ref=ailink': AFFILIATE_LINKS.midjourney,
    'https://www.grammarly.com/?ref=ailink': AFFILIATE_LINKS.grammarly
  });

  // 5. 创建导航页面
  console.log('\n5. 创建导航页面...');
  const navContent = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>网站导航 - AI.link.cn</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
</head>
<body>
    <nav class="container">
        <ul><li><strong><a href="/" style="color: inherit; text-decoration: none;">AI.link.cn</a></strong></li></ul>
    </nav>
    
    <div class="container">
        <h1>AI.link.cn 网站导航</h1>
        
        <h2>主要页面</h2>
        <ul>
            <li><a href="/">🏠 首页</a> - AI工具平台主页</li>
            <li><a href="/pages/tools/">🔧 所有工具评测</a> - 完整的AI工具列表</li>
            <li><a href="/pages/affiliate-guide.html">💰 赚钱指南</a> - Affiliate赚钱完整教程</li>
        </ul>
        
        <h2>AI工具评测</h2>
        <ul>
            <li><a href="/pages/tools/chatgpt.html">🤖 ChatGPT</a> - OpenAI AI助手</li>
            <li><a href="/pages/tools/midjourney.html">🎨 Midjourney</a> - AI图像生成</li>
            <li><a href="/pages/tools/grammarly.html">📝 Grammarly</a> - AI语法检查</li>
            <li><a href="/pages/tools/notion_ai.html">📓 Notion AI</a> - AI写作工具</li>
        </ul>
        
        <h2>API端点</h2>
        <ul>
            <li><a href="/api">📡 API首页</a> - 所有API信息</li>
            <li><a href="/api/tools">🔧 工具API</a> - AI工具数据</li>
            <li><a href="/api/affiliate">💰 Affiliate API</a> - 推广链接</li>
        </ul>
        
        <h2>资源文档</h2>
        <ul>
            <li><a href="https://github.com/RicharZhaoyj/ai-link-cn">🐙 GitHub仓库</a> - 项目源代码</li>
            <li><a href="https://github.com/RicharZhaoyj/ai-link-cn/blob/main/docs/affiliate_guide.md">📋 Affiliate申请指南</a></li>
            <li><a href="https://github.com/RicharZhaoyj/ai-link-cn/blob/main/docs/immediate-affiliate-programs.md">🚀 立即开始的Affiliate项目</a></li>
        </ul>
        
        <h2>联系我们</h2>
        <p>网站: <a href="https://ai.link.cn">https://ai.link.cn</a></p>
        <p>GitHub: <a href="https://github.com/RicharZhaoyj/ai-link-cn">RicharZhaoyj/ai-link-cn</a></p>
        
        <footer style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e5e7eb;">
            <p>© 2025 AI.link.cn - 专业的AI工具评测平台</p>
        </footer>
    </div>
</body>
</html>
  `.trim();

  await fs.writeFile('pages/navigation.html', navContent, 'utf-8');
  console.log('📄 已创建: pages/navigation.html');

  console.log('\n✅ 所有链接更新完成！');
  console.log('\n🎯 下一步:');
  console.log('1. 访问 https://ai.link.cn 查看更新');
  console.log('2. 点击页面上的链接应该都能正常工作了');
  console.log('3. 申请Affiliate后，更新 update-links.js 中的链接');
}

// 运行脚本
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { updateFile, createToolPage };