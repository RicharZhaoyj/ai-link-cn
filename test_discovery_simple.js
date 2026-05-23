#!/usr/bin/env node
/**
 * 简化版发现系统测试
 */

const axios = require('axios');
const cheerio = require('cheerio');

async function testSimpleDiscovery() {
  console.log('🧪 测试简化版AI工具发现...');
  console.log('='.repeat(50));
  
  // 测试配置
  const config = {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    },
    timeout: 30000
  };
  
  // 测试一些可靠的网站（避免那些会返回403的）
  const testSites = [
    {
      name: 'GitHub Trending AI',
      url: 'https://github.com/trending?since=daily&spoken_language_code=en',
      selector: '.Box-row'
    },
    {
      name: 'Awesome AI (GitHub)',
      url: 'https://github.com/topics/awesome-ai',
      selector: '.Box-row'
    },
    {
      name: 'FutureTools',
      url: 'https://www.futuretools.io/',
      selector: '.tool-card, article, .product-item'
    }
  ];
  
  let totalTools = 0;
  
  for (const site of testSites) {
    console.log(`\n🔍 测试: ${site.name}`);
    console.log(`   URL: ${site.url}`);
    
    try {
      const response = await axios.get(site.url, config);
      const $ = cheerio.load(response.data);
      
      // 根据网站类型解析
      let toolsFound = 0;
      let sampleTool = '';
      
      if (site.name.includes('GitHub')) {
        $(site.selector).each((i, element) => {
          const name = $(element).find('h2 a, h3 a').text().trim();
          const url = $(element).find('h2 a, h3 a').attr('href');
          
          if (name && url && (name.toLowerCase().includes('ai') || 
              name.toLowerCase().includes('artificial') ||
              name.toLowerCase().includes('machine'))) {
            toolsFound++;
            if (toolsFound === 1) sampleTool = name;
          }
        });
      } else {
        // 通用解析
        $(site.selector).each((i, element) => {
          const name = $(element).find('h1, h2, h3, h4, .title, .name').first().text().trim();
          if (name && name.length > 3) {
            toolsFound++;
            if (toolsFound === 1) sampleTool = name;
          }
        });
      }
      
      console.log(`   ✅ 找到 ${toolsFound} 个工具`);
      if (toolsFound > 0 && sampleTool) {
        console.log(`   示例: ${sampleTool}`);
      }
      
      totalTools += toolsFound;
      
      // 延迟以避免请求过快
      await new Promise(resolve => setTimeout(resolve, 2000));
      
    } catch (error) {
      console.log(`   ❌ 错误: ${error.message}`);
      if (error.response) {
        console.log(`     状态码: ${error.response.status}`);
      }
    }
  }
  
  console.log('\n' + '='.repeat(50));
  console.log(`📊 总计: ${totalTools} 个工具`);
  
  if (totalTools > 0) {
    console.log('✅ 发现系统基本功能正常');
    return { success: true, totalTools };
  } else {
    console.log('⚠️  未找到工具，可能需要调整来源或检查网络');
    return { success: false, totalTools: 0 };
  }
}

// 运行测试
if (require.main === module) {
  testSimpleDiscovery().then(result => {
    process.exit(result.success ? 0 : 1);
  });
}

module.exports = testSimpleDiscovery;