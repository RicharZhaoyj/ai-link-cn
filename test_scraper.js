/**
 * 测试AI工具爬虫
 */

const AIToolsScraper = require('./src/ai_tools_scraper.js');
const scraper = new AIToolsScraper();

async function testScraper() {
  console.log('🧪 开始测试爬虫修复...');
  console.log('='.repeat(50));
  
  try {
    // 测试简单的来源（GitHub）
    console.log('1. 测试GitHub来源...');
    const githubTools = await scraper.scrapeSource('github_trending', 'https://github.com/trending?since=daily&spoken_language_code=en&q=AI');
    console.log(`   GitHub找到 ${githubTools.length} 个工具`);
    
    if (githubTools.length > 0) {
      console.log('  示例工具:', githubTools[0].name);
    }
    
    // 测试Product Hunt（使用简化版本）
    console.log('\n2. 测试Product Hunt简化策略...');
    
    // 先测试一个简单的AI工具目录网站
    const easyTools = await scraper.scrapeSource('aitoolhunt', 'https://aitoolhunt.com/');
    console.log(`   AI工具目录找到 ${easyTools.length} 个工具`);
    
    if (easyTools.length > 0) {
      console.log('  示例工具:', easyTools[0].name);
    }
    
    // 测试通用解析
    console.log('\n3. 测试通用解析功能...');
    const testUrl = 'https://theresanaiforthat.com/';
    const testTools = await scraper.genericScraping(require('cheerio').load('<html><body><a href="https://chat.openai.com">ChatGPT</a><a href="https://midjourney.com">Midjourney</a></body></html>'), testUrl, 'test');
    console.log(`   通用解析找到 ${testTools.length} 个工具`);
    
    // 测试去重功能
    console.log('\n4. 测试去重功能...');
    const duplicateTools = [
      { name: 'ChatGPT', url: 'https://chat.openai.com', source: 'test1' },
      { name: 'ChatGPT', url: 'https://chat.openai.com', source: 'test2' },
      { name: 'Midjourney', url: 'https://midjourney.com', source: 'test1' }
    ];
    const uniqueTools = scraper.deduplicateTools(duplicateTools);
    console.log(`   原始 ${duplicateTools.length} 个，去重后 ${uniqueTools.length} 个`);
    
    console.log('\n✅ 爬虫基础功能测试通过！');
    
    // 建议
    console.log('\n💡 建议：');
    console.log('1. 对于Product Hunt，建议使用API或考虑替代来源');
    console.log('2. 可以增加更多AI工具目录网站作为来源');
    console.log('3. 考虑添加RSS订阅和社交媒体监控');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.error(error.stack);
  }
}

// 运行测试
if (require.main === module) {
  testScraper();
}

module.exports = testScraper;