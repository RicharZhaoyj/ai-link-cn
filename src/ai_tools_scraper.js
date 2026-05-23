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
      // 完整的浏览器请求头，避免被识别为爬虫
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
      },
      timeout: 60000, // 增加超时时间
      maxRetries: 5,  // 增加重试次数
      delayBetweenRequests: 3000, // 请求之间延迟3秒
      useProxy: false, // 可选：启用代理
      proxyUrl: null   // 代理URL
    };
    
    // 优化的AI工具来源列表（优先使用API或友好网站）
    this.sources = {
      // API友好型来源
      'github_trending': 'https://github.com/trending?since=daily&spoken_language_code=en&q=AI',
      'awesome_ai': 'https://github.com/topics/awesome-ai',
      
      // 专门AI工具目录
      'futurepedia': 'https://www.futurepedia.io/',
      'theresanaiforthat': 'https://theresanaiforthat.com/',
      'aitoolhunt': 'https://aitoolhunt.com/',
      'aitoolsdirectory': 'https://www.aitoolsdirectory.com/',
      'ai_toolkit': 'https://aitoolkit.org/',
      
      // 谨慎使用的来源（可能需要更复杂的处理）
      'producthunt': {
        url: 'https://www.producthunt.com/search?q=AI+tools',
        useApi: false,
        requiresAuth: false,
        difficulty: 'high' // Product Hunt反爬虫严格
      },
      
      // 新增：社交媒体和社区来源
      'reddit_ai': 'https://www.reddit.com/r/artificial/top/?t=week',
      'hackernews_ai': 'https://news.ycombinator.com/item?id=35034692' // AI相关讨论
    };
    
    // Product Hunt特定的请求头（如果需要）
    this.productHuntHeaders = {
      ...this.baseConfig.headers,
      'Referer': 'https://www.producthunt.com/',
      'Origin': 'https://www.producthunt.com'
    };
  }
  
  /**
   * 从多个来源收集AI工具信息 - 智能版
   */
  async collectAITools() {
    console.log('🧠 开始智能收集AI工具信息...');
    console.log('='.repeat(50));
    
    const tools = new Map();
    let totalCollected = 0;
    
    try {
      // 智能排序来源（从易到难）
      const sourceEntries = Object.entries(this.sources);
      
      // 先处理容易的来源（GitHub、API友好网站）
      const easySources = sourceEntries.filter(([name, config]) => {
        const difficulty = config.difficulty || 'medium';
        return difficulty === 'low' || name.includes('github');
      });
      
      // 然后处理中等难度的来源
      const mediumSources = sourceEntries.filter(([name, config]) => {
        const difficulty = config.difficulty || 'medium';
        return difficulty === 'medium' && !easySources.some(e => e[0] === name);
      });
      
      // 最后处理困难的来源（如Product Hunt）
      const hardSources = sourceEntries.filter(([name, config]) => {
        const difficulty = config.difficulty || 'medium';
        return difficulty === 'high' || name === 'producthunt';
      });
      
      const orderedSources = [...easySources, ...mediumSources, ...hardSources];
      
      for (const [sourceName, sourceConfig] of orderedSources) {
        console.log(`\n🔍 来源 ${sourceName} (${totalCollected + 1}/${orderedSources.length})`);
        
        try {
          // 根据来源难度调整策略
          const sourceTools = await this.scrapeSource(sourceName, sourceConfig);
          
          if (sourceTools.length === 0) {
            console.log(`  ⚠️  未找到工具，跳过此来源`);
            continue;
          }
          
          // 合并到工具列表
          for (const tool of sourceTools) {
            const toolName = tool.name.trim();
            
            if (!tools.has(toolName)) {
              tools.set(toolName, {
                ...tool,
                sources: [sourceName],
                popularity: 1, // 初始流行度
                firstSeen: new Date().toISOString()
              });
            } else {
              // 添加来源信息并增加流行度
              const existing = tools.get(toolName);
              if (!existing.sources.includes(sourceName)) {
                existing.sources.push(sourceName);
              }
              existing.popularity += 1;
              
              // 智能补充缺失的信息
              this.mergeToolInfo(existing, tool);
            }
          }
          
          console.log(`  ✅ 收集到 ${sourceTools.length} 个工具`);
          totalCollected += sourceTools.length;
          
        } catch (error) {
          console.error(`  ❌ 从 ${sourceName} 收集失败:`, error.message);
          
          // 对于重要来源，尝试简单回退
          if (sourceName === 'producthunt' || sourceName === 'futurepedia') {
            console.log(`  🔧 尝试简单回退策略...`);
            const fallbackTools = await this.simpleFallback(sourceName);
            if (fallbackTools.length > 0) {
              console.log(`  ⚡ 回退策略找到 ${fallbackTools.length} 个工具`);
            }
          }
          
          continue;
        }
        
        // 智能延迟 - 根据来源难度调整
        const difficulty = typeof sourceConfig === 'object' && sourceConfig.difficulty 
          ? sourceConfig.difficulty 
          : 'medium';
        
        if (difficulty === 'high') {
          await this.smartDelay(5000, 10000); // 高难度网站需要更长时间
        } else if (difficulty === 'medium') {
          await this.smartDelay(3000, 6000);
        } else {
          await this.smartDelay(1000, 3000);
        }
      }
      
      // 转换为数组并按流行度排序
      const toolsArray = Array.from(tools.values());
      
      // 智能排序算法
      toolsArray.sort((a, b) => {
        // 综合评分系统
        const scoreA = this.calculateToolScore(a);
        const scoreB = this.calculateToolScore(b);
        return scoreB - scoreA;
      });
      
      console.log('\n' + '='.repeat(50));
      console.log(`🎉 收集完成！共收集到 ${toolsArray.length} 个AI工具`);
      console.log('📊 工具统计:');
      
      // 统计各来源贡献
      const sourceStats = {};
      toolsArray.forEach(tool => {
        tool.sources.forEach(source => {
          sourceStats[source] = (sourceStats[source] || 0) + 1;
        });
      });
      
      Object.entries(sourceStats).forEach(([source, count]) => {
        console.log(`  ${source}: ${count} 个工具`);
      });
      
      // 保存到文件
      await this.saveTools(toolsArray);
      
      // 生成摘要报告
      await this.generateSummaryReport(toolsArray);
      
      return toolsArray;
      
    } catch (error) {
      console.error('❌ 收集AI工具失败:', error);
      
      // 尝试紧急回退
      console.log('🆘 尝试紧急回退策略...');
      try {
        const emergencyTools = await this.emergencyFallback();
        if (emergencyTools.length > 0) {
          console.log(`⚡ 紧急回退找到 ${emergencyTools.length} 个工具`);
          await this.saveTools(emergencyTools);
          return emergencyTools;
        }
      } catch (fallbackError) {
        console.error('紧急回退也失败了:', fallbackError.message);
      }
      
      throw error;
    }
  }
  
  /**
   * 计算工具综合评分
   */
  calculateToolScore(tool) {
    let score = 0;
    
    // 来源多样性（不同来源越多分越高）
    score += tool.sources.length * 5;
    
    // 流行度（被多个来源提及）
    score += (tool.popularity || 1) * 3;
    
    // 评分（如果有）
    if (tool.rating) {
      score += tool.rating * 10;
    }
    
    // 信息完整性
    if (tool.description && tool.description.length > 50) score += 5;
    if (tool.category) score += 3;
    if (tool.pricing) score += 2;
    if (tool.url && tool.url.includes('http')) score += 1;
    
    // 名称质量（排除明显非工具的名称）
    const name = tool.name.toLowerCase();
    if (name.includes('http') || name.includes('.com')) score -= 10;
    if (name.length < 3 || name.length > 100) score -= 5;
    
    return score;
  }
  
  /**
   * 智能合并工具信息
   */
  mergeToolInfo(existing, newTool) {
    // 合并描述（取更长的）
    if (newTool.description && 
        (!existing.description || newTool.description.length > existing.description.length)) {
      existing.description = newTool.description;
    }
    
    // 合并类别（如果原来的没有）
    if (!existing.category && newTool.category) {
      existing.category = newTool.category;
    }
    
    // 合并定价信息
    if (!existing.pricing && newTool.pricing) {
      existing.pricing = newTool.pricing;
    }
    
    // 合并评分（取更高的）
    if (newTool.rating && (!existing.rating || newTool.rating > existing.rating)) {
      existing.rating = newTool.rating;
    }
    
    // 合并URL（如果原来的无效）
    if ((!existing.url || existing.url.includes('undefined')) && newTool.url) {
      existing.url = newTool.url;
    }
    
    // 最后更新时间
    existing.lastUpdated = new Date().toISOString();
  }
  
  /**
   * 简单回退策略
   */
  async simpleFallback(sourceName) {
    try {
      // 对于重要来源，使用简单搜索作为回退
      const searchQueries = {
        'producthunt': ['AI tools', 'artificial intelligence', 'machine learning'],
        'futurepedia': ['AI directory', 'AI tools list'],
        'github': ['awesome-ai', 'AI repositories']
      };
      
      const queries = searchQueries[sourceName] || ['AI'];
      const tools = [];
      
      // 这里可以扩展为实际搜索逻辑
      // 目前返回空数组，但留下扩展接口
      
      return tools;
      
    } catch (error) {
      console.error(`简单回退失败:`, error.message);
      return [];
    }
  }
  
  /**
   * 紧急回退策略
   */
  async emergencyFallback() {
    console.log('执行紧急回退策略...');
    
    // 返回预定义的AI工具列表（硬编码备用）
    const emergencyTools = [
      {
        name: 'ChatGPT',
        url: 'https://chat.openai.com',
        description: 'OpenAI的对话式AI助手',
        category: '对话AI',
        sources: ['emergency'],
        popularity: 1
      },
      {
        name: 'Midjourney',
        url: 'https://www.midjourney.com',
        description: '文本到图像AI生成器',
        category: '图像生成',
        sources: ['emergency'],
        popularity: 1
      },
      {
        name: 'GitHub Copilot',
        url: 'https://github.com/features/copilot',
        description: 'AI编程助手',
        category: '编程助手',
        sources: ['emergency'],
        popularity: 1
      }
    ];
    
    return emergencyTools;
  }
  
  /**
   * 智能延迟函数 - 模拟人类浏览行为
   */
  async smartDelay(minMs = 2000, maxMs = 5000) {
    const delay = minMs + Math.random() * (maxMs - minMs);
    console.log(`延迟 ${Math.round(delay)}ms...`);
    await this.delay(delay);
  }
  
  /**
   * 从特定来源爬取工具信息 - 智能版
   */
  async scrapeSource(sourceName, sourceConfig) {
    try {
      // 处理不同的配置格式
      const url = typeof sourceConfig === 'string' ? sourceConfig : sourceConfig.url;
      const difficulty = sourceConfig.difficulty || 'medium';
      
      console.log(`从 ${sourceName} 收集数据 (难度: ${difficulty})...`);
      
      // 根据难度调整策略
      let config = {
        headers: this.baseConfig.headers,
        timeout: this.baseConfig.timeout
      };
      
      // 特殊处理Product Hunt
      if (sourceName === 'producthunt') {
        config.headers = this.productHuntHeaders;
        config.timeout = 90000; // 更长的超时时间
        
        // 添加随机延迟，模拟人类浏览
        await this.smartDelay(5000, 10000);
        
        // 尝试使用API替代（如果有的话）
        const apiResult = await this.tryProductHuntApi();
        if (apiResult && apiResult.length > 0) {
          console.log(`使用API从Product Hunt收集到 ${apiResult.length} 个工具`);
          return apiResult;
        }
      }
      
      // 模拟人类浏览行为：随机滚动
      if (difficulty === 'high') {
        config.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01';
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
      }
      
      const response = await axios.get(url, config);
      
      // 随机延迟处理响应
      await this.delay(1000 + Math.random() * 2000);
      
      const $ = cheerio.load(response.data);
      const tools = [];
      
      // 根据来源类型使用不同的解析策略
      switch (sourceName) {
        case 'futurepedia':
          // Futurepedia页面解析
          $('.tool-card, article, .product-item').each((i, element) => {
            const tool = this.parseToolCard($, element, sourceName);
            if (tool.name && tool.url) {
              tools.push(tool);
            }
          });
          break;
          
        case 'theresanaiforthat':
          // There's An AI For That解析
          $('.tool-item, .app-card, .product-card').each((i, element) => {
            const tool = {
              name: $(element).find('.tool-title, h3, .title').text().trim(),
              category: $(element).find('.tool-category, .category, .tag').text().trim(),
              description: $(element).find('.tool-description, p, .description').text().trim(),
              url: $(element).find('a').attr('href'),
              tags: $(element).find('.tool-tags, .tags').text().split(',').map(t => t.trim()),
              rating: this.extractRating($(element))
            };
            
            if (tool.name && tool.url) {
              tools.push(tool);
            }
          });
          break;
          
        case 'github_trending':
        case 'awesome_ai':
          // GitHub页面解析
          $('article, .Box-row').each((i, element) => {
            const name = $(element).find('h2 a, h3 a').text().trim();
            const url = $(element).find('h2 a, h3 a').attr('href');
            
            if (name && url && (name.toLowerCase().includes('ai') || 
                name.toLowerCase().includes('artificial') ||
                name.toLowerCase().includes('machine'))) {
              tools.push({
                name: name,
                url: 'https://github.com' + url,
                description: $(element).find('p').text().trim(),
                stars: $(element).find('[aria-label*="star"]').text().trim(),
                language: $(element).find('[itemprop="programmingLanguage"]').text().trim(),
                source: sourceName
              });
            }
          });
          break;
          
        case 'producthunt':
          // Product Hunt的智能解析
          const productHuntTools = this.parseProductHunt($, sourceName);
          tools.push(...productHuntTools);
          break;
          
        case 'reddit_ai':
          // Reddit解析
          $('[data-testid="post-title"]').each((i, element) => {
            const title = $(element).text().trim();
            const url = $(element).attr('href');
            
            if (title && url && (title.toLowerCase().includes('ai') || 
                title.toLowerCase().includes('tool') ||
                title.toLowerCase().includes('openai'))) {
              tools.push({
                name: title,
                url: 'https://www.reddit.com' + url,
                upvotes: $(element).closest('div').find('[aria-label="upvote"]').text().trim(),
                source: sourceName
              });
            }
          });
          break;
          
        default:
          // 通用智能解析
          tools.push(...this.genericScraping($, url, sourceName));
      }
      
      console.log(`从 ${sourceName} 收集到 ${tools.length} 个工具`);
      
      // 过滤和去重
      const uniqueTools = this.deduplicateTools(tools);
      
      return uniqueTools.slice(0, 30); // 限制数量
      
    } catch (error) {
      console.error(`爬取 ${sourceName} 失败:`, error.message);
      
      // 对于困难网站，尝试备用策略
      if (sourceName === 'producthunt') {
        return await this.fallbackProductHuntStrategy();
      }
      
      return [];
    }
  }
  
  /**
   * 解析Product Hunt页面
   */
  parseProductHunt($, sourceName) {
    const tools = [];
    
    // 尝试多种选择器（Product Hunt经常更改HTML结构）
    const selectors = [
      '[data-test*="post"]',
      '.postItem',
      '.styles_item__',
      'article',
      '.post-card',
      '.product-item'
    ];
    
    for (const selector of selectors) {
      $(selector).each((i, element) => {
        const name = $(element).find('h3, [data-test*="post-name"], .post-name').text().trim();
        const url = $(element).find('a').attr('href');
        
        if (name && url) {
          // 过滤非AI工具
          const lowercaseName = name.toLowerCase();
          if (lowercaseName.includes('ai') || 
              lowercaseName.includes('artificial') ||
              lowercaseName.includes('machine learning') ||
              lowercaseName.includes('chatgpt') ||
              lowercaseName.includes('gpt')) {
            
            const tool = {
              name: name,
              url: url.startsWith('http') ? url : 'https://www.producthunt.com' + url,
              description: $(element).find('p, .description').text().trim(),
              upvotes: $(element).find('[data-test*="vote-count"], .vote-count').text().trim(),
              tagline: $(element).find('.tagline, .description-short').text().trim(),
              source: sourceName
            };
            
            tools.push(tool);
          }
        }
      });
      
      if (tools.length > 0) break; // 找到有效选择器就停止
    }
    
    return tools;
  }
  
  /**
   * Product Hunt备用策略
   */
  async fallbackProductHuntStrategy() {
    console.log('使用Product Hunt备用策略...');
    
    try {
      // 尝试搜索"AI"相关话题
      const topics = ['artificial-intelligence', 'machine-learning', 'chatgpt', 'openai'];
      const tools = [];
      
      for (const topic of topics) {
        const url = `https://www.producthunt.com/topics/${topic}`;
        
        try {
          const response = await axios.get(url, {
            headers: this.productHuntHeaders,
            timeout: 30000
          });
          
          const $ = cheerio.load(response.data);
          const topicTools = this.parseProductHunt($, 'producthunt_topic');
          tools.push(...topicTools);
          
          await this.smartDelay(3000, 6000); // 话题之间延迟
          
        } catch (error) {
          console.error(`获取话题 ${topic} 失败:`, error.message);
          continue;
        }
      }
      
      return tools.slice(0, 20);
      
    } catch (error) {
      console.error('Product Hunt备用策略失败:', error.message);
      return [];
    }
  }
  
  /**
   * 尝试使用Product Hunt API
   */
  async tryProductHuntApi() {
    // 注意：Product Hunt API需要认证
    // 这里只是示例，实际使用时需要API密钥
    console.log('尝试使用Product Hunt API...');
    
    // 如果没有API密钥，返回空数组
    return [];
  }
  
  /**
   * 解析工具卡片
   */
  parseToolCard($, element, sourceName) {
    return {
      name: $(element).find('.tool-name, h3, .title, .name').text().trim(),
      category: $(element).find('.tool-category, .category, .tag').text().trim(),
      description: $(element).find('.tool-description, p, .description').text().trim(),
      url: $(element).find('a').attr('href'),
      pricing: $(element).find('.pricing-badge, .price, .pricing').text().trim(),
      rating: this.extractRating($(element)),
      source: sourceName
    };
  }
  
  /**
   * 提取评分
   */
  extractRating($element) {
    const ratingText = $element.find('.rating, [class*="star"], [class*="rate"]').text().trim();
    if (ratingText) {
      const match = ratingText.match(/(\d+(\.\d+)?)\/5/);
      if (match) return parseFloat(match[1]);
      
      const starMatch = ratingText.match(/(\d+(\.\d+)?)\s*[★☆]/);
      if (starMatch) return parseFloat(starMatch[1]);
    }
    return null;
  }
  
  /**
   * 通用智能解析
   */
  genericScraping($, url, sourceName) {
    const tools = [];
    
    // 多种选择器尝试
    const linkSelectors = [
      'a[href*="tool"]',
      'a[href*="ai"]',
      'a[href*="chat"]',
      'a[href*="gpt"]',
      'a[href*="openai"]',
      '.product-link',
      '.tool-link',
      'article a',
      '.card a'
    ];
    
    for (const selector of linkSelectors) {
      $(selector).each((i, element) => {
        const href = $(element).attr('href');
        const text = $(element).text().trim();
        
        if (text && href && text.length > 3 && text.length < 100) {
          // 检查是否是AI相关
          const lowerText = text.toLowerCase();
          if (lowerText.includes('ai') || 
              lowerText.includes('artificial') ||
              lowerText.includes('chat') ||
              lowerText.includes('gpt') ||
              lowerText.includes('bot')) {
            
            tools.push({
              name: text,
              url: href.startsWith('http') ? href : new URL(href, url).href,
              source: sourceName
            });
          }
        }
      });
      
      if (tools.length > 10) break; // 找到足够链接就停止
    }
    
    return tools;
  }
  
  /**
   * 去重工具
   */
  deduplicateTools(tools) {
    const seen = new Set();
    return tools.filter(tool => {
      const key = tool.name.toLowerCase() + (tool.url || '');
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
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
   * 生成摘要报告
   */
  async generateSummaryReport(tools) {
    const reportDir = path.join(__dirname, '..', 'reports');
    await fs.mkdir(reportDir, { recursive: true });
    
    const now = new Date();
    const reportDate = now.toISOString().split('T')[0];
    
    let report = `# AI工具发现报告 - ${reportDate}\n\n`;
    report += `## 📊 执行摘要\n\n`;
    report += `- **发现时间**: ${now.toLocaleString('zh-CN')}\n`;
    report += `- **发现工具总数**: ${tools.length}\n`;
    report += `- **高质量工具**: ${tools.filter(t => t.rating >= 4).length}\n`;
    report += `- **新增工具**: ${tools.filter(t => !t.firstSeen || t.firstSeen.includes(reportDate)).length}\n\n`;
    
    // 按类别统计
    report += `## 🗂️ 类别分布\n\n`;
    const categories = {};
    tools.forEach(tool => {
      const cat = tool.category || '未分类';
      categories[cat] = (categories[cat] || 0) + 1;
    });
    
    Object.entries(categories)
      .sort((a, b) => b[1] - a[1])
      .forEach(([cat, count]) => {
        const percentage = ((count / tools.length) * 100).toFixed(1);
        report += `- **${cat}**: ${count} 个工具 (${percentage}%)\n`;
      });
    
    // 热门工具
    report += `\n## 🔥 热门工具 (前10名)\n\n`;
    const topTools = tools.slice(0, 10);
    report += '| 排名 | 工具名称 | 评分 | 类别 | 来源数量 |\n';
    report += '|------|----------|------|------|----------|\n';
    
    topTools.forEach((tool, index) => {
      report += `| ${index + 1} | ${tool.name} | ${tool.rating || '-'} | ${tool.category || '未分类'} | ${tool.sources.length} |\n`;
    });
    
    // 新发现工具
    const newTools = tools.filter(t => t.firstSeen && t.firstSeen.includes(reportDate));
    if (newTools.length > 0) {
      report += `\n## 🆕 新发现工具\n\n`;
      newTools.forEach(tool => {
        report += `- **${tool.name}**: ${tool.description || '无描述'} [🔗](${tool.url})\n`;
      });
    }
    
    // 建议
    report += `\n## 💡 建议和下一步行动\n\n`;
    report += `1. **优先评测**: ${topTools.slice(0, 3).map(t => t.name).join(', ')}\n`;
    report += `2. **扩大来源**: 考虑添加更多来源如AI Aggregator、VC投资组合\n`;
    report += `3. **质量审核**: 对评分≥4.5的工具进行人工审核\n`;
    report += `4. **Affiliate检查**: 检查热门工具是否有Affiliate项目\n`;
    
    const reportPath = path.join(reportDir, `discovery_report_${reportDate}.md`);
    await fs.writeFile(reportPath, report, 'utf-8');
    
    console.log(`📄 摘要报告已生成: ${reportPath}`);
    
    // 同时生成Markdown格式的工具列表
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
    markdown += `> 共收录 ${tools.length} 个AI工具\n\n`;
    
    markdown += '| 工具名称 | 类别 | 描述 | 定价 | 评分 | 来源 |\n';
    markdown += '|----------|------|------|------|------|------|\n';
    
    tools.forEach(tool => {
      const name = tool.name || '未知';
      const category = tool.category || '未分类';
      const description = (tool.description || '无描述').slice(0, 80) + '...';
      const pricing = tool.pricing || '未提供';
      const rating = tool.rating ? `${tool.rating.toFixed(1)}/5` : '-';
      const sources = tool.sources?.join(', ') || '未知';
      
      markdown += `| ${name} | ${category} | ${description} | ${pricing} | ${rating} | ${sources} |\n`;
    });
    
    const mdPath = path.join(contentDir, 'ai_tools_list.md');
    await fs.writeFile(mdPath, markdown, 'utf-8');
    
    console.log(`📝 Markdown列表已生成: ${mdPath}`);
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