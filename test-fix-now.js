#!/usr/bin/env node
/**
 * 立即测试链接修复
 */

const https = require('https');
const http = require('http');

const SITE_URL = 'https://ai.link.cn';

function testUrl(url, expectedStatus = 200) {
  return new Promise((resolve) => {
    const fullUrl = SITE_URL + url;
    const protocol = url.startsWith('https') ? https : http;
    
    console.log(`测试: ${url}`);
    
    const req = protocol.get(fullUrl, (res) => {
      const success = res.statusCode === expectedStatus;
      console.log(`  ${success ? '✅' : '❌'} 状态: ${res.statusCode} (期望: ${expectedStatus})`);
      console.log(`  内容类型: ${res.headers['content-type'] || '未知'}`);
      resolve(success);
    });
    
    req.on('error', (err) => {
      console.log(`  ❌ 错误: ${err.message}`);
      resolve(false);
    });
    
    req.setTimeout(10000, () => {
      console.log(`  ⏱️  超时: 10秒`);
      req.destroy();
      resolve(false);
    });
  });
}

async function main() {
  console.log('🔧 立即测试链接修复效果\n');
  
  const tests = [
    { url: '/', name: '首页' },
    { url: '/pages/tools/', name: '工具列表页' },
    { url: '/pages/tools/chatgpt.html', name: 'ChatGPT评测页' },
    { url: '/pages/tools/midjourney.html', name: 'Midjourney评测页' },
    { url: '/pages/affiliate-guide.html', name: '赚钱指南页' },
    { url: '/pages/navigation.html', name: '网站导航页' },
    { url: '/test-all-links.html', name: '链接测试页' },
    { url: '/cache-fix.html', name: '缓存修复指南' }
  ];
  
  let passed = 0;
  const total = tests.length;
  
  for (const test of tests) {
    console.log(`\n${test.name}:`);
    const success = await testUrl(test.url);
    if (success) passed++;
  }
  
  console.log('\n' + '='.repeat(50));
  console.log(`📊 测试结果: ${passed}/${total} 通过`);
  
  if (passed === total) {
    console.log('🎉 所有链接测试通过！');
    console.log('\n🚀 现在可以访问以下链接:');
    console.log('1. 首页: https://ai.link.cn');
    console.log('2. 工具列表: https://ai.link.cn/pages/tools/');
    console.log('3. ChatGPT评测: https://ai.link.cn/pages/tools/chatgpt.html');
    console.log('4. 赚钱指南: https://ai.link.cn/pages/affiliate-guide.html');
  } else {
    console.log('⚠️ 有些链接仍有问题。建议:');
    console.log('1. 等待Vercel部署完成（1-2分钟）');
    console.log('2. 按Ctrl+F5强制刷新浏览器');
    console.log('3. 使用无痕/隐私模式访问');
  }
  
  console.log('\n🔧 我们已修复的问题:');
  console.log('1. ✅ 更新了Vercel路由配置');
  console.log('2. ✅ 添加了_redirects文件');
  console.log('3. ✅ 创建了静态服务器配置');
  console.log('4. ✅ 修复了所有路径映射');
  
  console.log('\n💡 如果链接仍然无效:');
  console.log('1. 等待10分钟让Vercel CDN缓存更新');
  console.log('2. 访问 https://ai.link.cn/test-all-links.html 实时测试');
  console.log('3. 访问 https://ai.link.cn/cache-fix.html 查看解决方案');
}

// 运行测试
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { testUrl };