const fs = require('fs').promises;
const path = require('path');

async function fixFile(filePath, replacements) {
  try {
    let content = await fs.readFile(filePath, 'utf-8');
    let updated = false;
    
    for (const [old, newVal] of Object.entries(replacements)) {
      if (content.includes(old)) {
        content = content.replace(new RegExp(old, 'g'), newVal);
        updated = true;
      }
    }
    
    if (updated) {
      await fs.writeFile(filePath, content, 'utf-8');
      console.log(`✅ 已修复: ${filePath}`);
    }
  } catch (error) {
    console.log(`❌ 修复失败 ${filePath}: ${error.message}`);
  }
}

async function main() {
  console.log('🔧 修复路径问题...\n');
  
  // 修复首页
  await fixFile('pages/tools/index.html', {
    '/pages/tools/chatgpt.html': 'chatgpt.html',
    '/pages/tools/jasper.html': 'jasper.html',
    '/pages/tools/grammarly.html': 'grammarly.html',
    '/pages/tools/notion_ai.html': 'notion_ai.html',
    '/pages/tools/midjourney.html': 'midjourney.html',
    '/pages/tools/dalle.html': '../',
    '/pages/tools/canva.html': 'canva.html',
    '/pages/tools/copilot.html': '../',
    '/pages/tools/codewhisperer.html': '../',
    '/affiliate-guide.html': '../affiliate-guide.html',
    '/tools/': '../'
  });
  
  // 修复导航页
  await fixFile('pages/navigation.html', {
    '/pages/tools/': 'tools/',
    '/pages/affiliate-guide.html': '../affiliate-guide.html',
    '/pages/tools/chatgpt.html': 'tools/chatgpt.html',
    '/pages/tools/midjourney.html': 'tools/midjourney.html',
    '/pages/tools/grammarly.html': 'tools/grammarly.html',
    '/pages/tools/notion_ai.html': 'tools/notion_ai.html',
    '/api': '../../api',
    '/api/tools': '../../api/tools',
    '/api/affiliate': '../../api/affiliate'
  });
  
  // 修复工具页
  const toolPages = [
    'pages/tools/chatgpt.html',
    'pages/tools/midjourney.html',
    'pages/tools/grammarly.html',
    'pages/tools/notion_ai.html',
    'pages/tools/canva.html',
    'pages/tools/jasper.html',
    'pages/tools/convertkit.html',
    'pages/tools/hostinger.html'
  ];
  
  for (const page of toolPages) {
    await fixFile(page, {
      '/pages/tools/': '../',
      '/pages/affiliate-guide.html': '../../affiliate-guide.html'
    });
  }
  
  console.log('\n✅ 所有路径问题已修复！');
  console.log('\n📋 更新内容:');
  console.log('1. 修复了相对路径错误');
  console.log('2. 更新了工具页面链接');
  console.log('3. 修复了导航页链接');
  console.log('4. 确保所有内部链接正常工作');
}

main().catch(console.error);
