/**
 * AI工具数据爬取器
 * 用于收集和更新AI工具信息
 */

const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs').promises;
const path = require('path');

class AIToolsScraper {
  constructor() {
    this.baseConfig = {
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      timeout: 30000,
      maxRetries: 3
    };
    
    // AI工具来源列表
    this.sources = {
      'futurepedia': 'https://www.futurepedia.io/',
      'theresanaiforthat': 'https://theresanaiforthat.com/',
      'aitoolhunt': 'https://aitoolhunt.com/',
      'producthunt': 'https://www.producthunt.com/search?q=AI+tools'
    };
  }
  
  /**
   * 从多个来源收集AI工具信息
   */
  async collectAITools() {
    console.log('开始收集AI工具信息...');
    
    const tools = new Map();
    
    try {
      // 从各个来源收集
      for (const [sourceName, sourceUrl] of Object.entries(this.sources)) {
        console.log(`从 ${sourceName} 收集数据...`);
        
        try {
          const sourceTools = await this.scrapeSource(sourceName, sourceUrl);
          
          // 合并到工具列表
          for (const tool of sourceTools) {
            if (!tools.has(tool.name)) {
              tools.set(tool.name, {
                ...tool,
                sources: [sourceName]
              });
            } else {
              // 添加来源信息
              const existing = tools.get(tool.name);
              if (!existing.sources.includes(sourceName)) {
                existing.sources.push(sourceName);
              }
              
              // 补充缺失的信息
              Object.keys(tool).forEach(key => {
                if (!existing[key] && tool[key]) {
                  existing[key] = tool[key];
                }
              });
            }
          }
          
          console.log(`从 ${sourceName} 收集到 ${sourceTools.length} 个工具`);
        } catch (error) {
          console.error(`从 ${sourceName} 收集失败:`, error.message);
          continue;
        }
        
        // 避免请求过快
        await this.delay(2000);
      }
      
      // 转换为数组并按流行度排序
      const toolsArray = Array.from(tools.values());
      toolsArray.sort((a, b) => {
        // 按评分、评论数、来源数量排序
        const scoreA = (a.rating || 0) * 10 + (a.reviewCount || 0) + a.sources.length;
        const scoreB = (b.rating || 0) * 10 + (b.reviewCount || 0) + b.sources.length;
        return scoreB - scoreA;
      });
      
      console.log(`共收集到 ${toolsArray.length} 个AI工具`);
      
      // 保存到文件
      await this.saveTools(toolsArray);
      
      return toolsArray;
      
    } catch (error) {
      console.error('收集AI工具失败:', error);
      throw error;
    }
  }
  
  /**
   * 从特定来源爬取工具信息
   */
  async scrapeSource(sourceName, url) {
    try {
      const response = await axios.get(url, {
        headers: { 'User-Agent': this.baseConfig.userAgent },
        timeout: this.baseConfig.timeout
      });
      
      const $ = cheerio.load(response.data);
      const tools = [];
      
      switch (sourceName) {
        case 'futurepedia':
          // Futurepedia页面解析
          $('.tool-card').each((i, element) => {
            const tool = {
              name: $(element).find('.tool-name').text().trim(),
              category: $(element).find('.tool-category').text().trim(),
              description: $(element).find('.tool-description').text().trim(),
              url: $(element).find('a').attr('href'),
              pricing: $(element).find('.pricing-badge').text().trim(),
              rating: parseFloat($(element).find('.rating').text()) || null
            };
            
            if (tool.name && tool.url) {
              tools.push(tool);
            }
          });
          break;
          
        case 'theresanaiforthat':
          // There's An AI For That解析
          $('.tool-item').each((i, element) => {
            const tool = {
              name: $(element).find('.tool-title').text().trim(),
              category: $(element).find('.tool-category').text().trim(),
              description: $(element).find('.tool-description').text().trim(),
              url: $(element).find('a').attr('href'),
              tags: $(element).find('.tool-tags').text().split(',').map(t => t.trim())
            };
            
            if (tool.name && tool.url) {
              tools.push(tool);
            }
          });
          break;
          
        // 其他来源的解析逻辑...
          
        default:
          // 通用解析
          $('a[href*="tool"], a[href*="ai"]').each((i, element) => {
            const href = $(element).attr('href');
            const text = $(element).text().trim();
            
            if (text && href && text.length > 3 && text.length < 100) {
              tools.push({
                name: text,
                url: href.startsWith('http') ? href : new URL(href, url).href,
                source: sourceName
              });
            }
          });
      }
      
      return tools.slice(0, 50); // 限制数量
      
    } catch (error) {
      console.error(`爬取 ${sourceName} 失败:`, error.message);
      return [];
    }
  }
  
  /**
   * 获取工具详细信息
   */
  async getToolDetails(toolName, toolUrl) {
    try {
      console.log(`获取 ${toolName} 的详细信息...`);
      
      const response = await axios.get(toolUrl, {
        headers: { 'User-Agent': this.baseConfig.userAgent },
        timeout: this.baseConfig.timeout
      });
      
      const $ = cheerio.load(response.data);
      
      // 尝试提取关键信息
      const details = {
        name: toolName,
        url: toolUrl,
        description: this.extractDescription($),
        pricing: this.extractPricing($),
        features: this.extractFeatures($),
        affiliateAvailable: this.checkAffiliateAvailability($),
        lastUpdated: new Date().toISOString()
      };
      
      return details;
      
    } catch (error) {
      console.error(`获取 ${toolName} 详情失败:`, error.message);
      return {
        name: toolName,
        url: toolUrl,
        error: '无法获取详情'
      };
    }
  }
  
  /**
   * 提取描述信息
   */
  extractDescription($) {
    // 尝试多个选择器
    const selectors = [
      'meta[name="description"]',
      'meta[property="og:description"]',
      '.description',
      '#description',
      'p:first',
      'article p'
    ];
    
    for (const selector of selectors) {
      const text = $(selector).first().text().trim();
      if (text && text.length > 50 && text.length < 500) {
        return text;
      }
    }
    
    return '';
  }
  
  /**
   * 提取定价信息
   */
  extractPricing($) {
    const pricingText = $('*:contains("$"), *:contains("price"), *:contains("pricing")')
      .filter((i, el) => $(el).text().includes('$') || $(el).text().toLowerCase().includes('pricing'))
      .first()
      .text()
      .trim();
    
    if (pricingText) {
      // 提取价格信息
      const priceMatch = pricingText.match(/\$\d+(\.\d+)?(\/\w+)?/);
      return priceMatch ? priceMatch[0] : '未提供定价';
    }
    
    return '未提供定价';
  }
  
  /**
   * 提取功能特性
   */
  extractFeatures($) {
    const features = [];
    
    // 查找列表项
    $('li, .feature, .benefit').each((i, el) => {
      const text = $(el).text().trim();
      if (text && text.length > 10 && text.length < 200) {
        features.push(text);
      }
    });
    
    return features.slice(0, 10); // 最多10个特性
  }
  
  /**
   * 检查是否有Affiliate项目
   */
  checkAffiliateAvailability($) {
    const html = $.html().toLowerCase();
    const keywords = ['affiliate', 'referral', 'partner', 'commission', 'earn'];
    
    return keywords.some(keyword => html.includes(keyword));
  }
  
  /**
   * 保存工具数据到文件
   */
  async saveTools(tools) {
    const dataDir = path.join(__dirname, '..', 'data');
    await fs.mkdir(dataDir, { recursive: true });
    
    const filePath = path.join(dataDir, 'ai_tools.json');
    await fs.writeFile(filePath, JSON.stringify(tools, null, 2));
    
    console.log(`工具数据已保存到: ${filePath}`);
    
    // 同时生成Markdown格式
    await this.generateMarkdown(tools);
  }
  
  /**
   * 生成Markdown格式的工具列表
   */
  async generateMarkdown(tools) {
    const contentDir = path.join(__dirname, '..', 'content', 'tools');
    await fs.mkdir(contentDir, { recursive: true });
    
    let markdown = '# AI工具列表\n\n';
    markdown += `> 最后更新: ${new Date().toLocaleString('zh-CN')}\n\n`;
    markdown += '| 工具名称 | 类别 | 定价 | 评分 | Affiliate |\n';
    markdown += '|----------|------|------|------|-----------|\n';
    
    tools.forEach(tool => {
      const name = tool.name || '未知';
      const category = tool.category || '未分类';
      const pricing = tool.pricing || '未提供';
      const rating = tool.rating ? `${tool.rating}/5` : '-';
      const affiliate = tool.affiliateAvailable ? '✅' : '❌';
      
      markdown += `| ${name} | ${category} | ${pricing} | ${rating} | ${affiliate} |\n`;
    });
    
    const mdPath = path.join(contentDir, 'ai_tools_list.md');
    await fs.writeFile(mdPath, markdown, 'utf-8');
    
    console.log(`Markdown列表已生成: ${mdPath}`);
  }
  
  /**
   * 延迟函数
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// 命令行接口
if (require.main === module) {
  const scraper = new AIToolsScraper();
  
  const args = process.argv.slice(2);
  const command = args[0];
  
  async function main() {
    try {
      if (command === 'collect') {
        await scraper.collectAITools();
      } else if (command === 'details') {
        const toolName = args[1];
        const toolUrl = args[2];
        
        if (!toolName || !toolUrl) {
          console.error('请提供工具名称和URL');
          console.error('用法: node src/ai_tools_scraper.js details <工具名称> <URL>');
          process.exit(1);
        }
        
        const details = await scraper.getToolDetails(toolName, toolUrl);
        console.log(JSON.stringify(details, null, 2));
      } else {
        console.log('AI工具爬取器');
        console.log('用法:');
        console.log('  node src/ai_tools_scraper.js collect     - 收集所有AI工具');
        console.log('  node src/ai_tools_scraper.js details <名称> <URL> - 获取工具详情');
      }
    } catch (error) {
      console.error('执行失败:', error);
      process.exit(1);
    }
  }
  
  main();
}

module.exports = AIToolsScraper;