#!/usr/bin/env node
const axios = require('axios');
const cheerio = require('cheerio');

// 测试多个AI工具发现网站
async function testDiscoverySources() {
  console.log('🚀 开始测试AI工具发现来源...\n');
  
  const sources = [
    {
      name: 'Product Hunt AI',
      url: 'https://www.producthunt.com/collections/artificial-intelligence',
      description: 'Product Hunt AI工具集合'
    },
    {
      name: 'FutureTools',
      url: 'https://www.futuretools.io/',
      description: '未来技术工具目录'
    },
    {
      name: 'AI Tools Directory',
      url: 'https://www.aitoolsdirectory.com/',
      description: 'AI工具目录'
    },
    {
      name: 'There\'s An AI For That',
      url: 'https://theresanaiforthat.com/',
      description: 'AI工具搜索引擎'
    }
  ];
  
  let totalToolsFound = 0;
  
  for (const source of sources) {
    try {
      console.log(`📡 测试: ${source.name} (${source.url})`);
      
      const response = await axios.get(source.url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
          'Accept-Encoding': 'gzip, deflate, br',
          'Connection': 'keep-alive',
          'Upgrade-Insecure-Requests': '1'
        },
        timeout: 30000
      });
      
      if (response.status === 200) {
        const $ = cheerio.load(response.data);
        let toolsFound = 0;
        
        // 根据不同网站选择不同的选择器
        switch (source.name) {
          case 'Product Hunt AI':
            toolsFound = $('.styles_item__Sn_12').length;
            break;
          case 'FutureTools':
            toolsFound = $('.tool-card').length;
            break;
          case 'AI Tools Directory':
            toolsFound = $('.tool-listing').length;
            break;
          case 'There\'s An AI For That':
            toolsFound = $('.tool-card').length;
            break;
          default:
            toolsFound = $('[class*="tool"], [class*="product"], .card, .item').length;
        }
        
        console.log(`   ✅ 成功访问 | 发现工具数: ${toolsFound}`);
        totalToolsFound += toolsFound;
      } else {
        console.log(`   ❌ 访问失败 | 状态码: ${response.status}`);
      }
    } catch (error) {
      if (error.response) {
        console.log(`   ❌ HTTP错误 | 状态码: ${error.response.status}`);
      } else if (error.code === 'ECONNABORTED') {
        console.log(`   ⏱️  超时 | ${error.message}`);
      } else {
        console.log(`   ❌ 网络错误 | ${error.message}`);
      }
    }
    
    // 等待2秒避免频率过高
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  console.log(`\n📊 总计: ${totalToolsFound} 个潜在工具被发现`);
  console.log('\n💡 建议:');
  console.log('1. 检查爬虫配置和请求头');
  console.log('2. 尝试使用代理或VPN');
  console.log('3. 考虑使用官方API（如果有）');
  console.log('4. 增加更多AI工具发现来源');
}

// 执行测试
testDiscoverySources().catch(console.error);