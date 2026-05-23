/**
 * AI工具发现系统 - 多来源智能发现
 * 替代和扩展原有的爬虫系统
 */

const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs').promises;
const path = require('path');

class AIDiscoverySystem {
  constructor() {
    // 完善的请求配置
    this.config = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
      },
      timeout: 45000,
      maxRetries: 3
    };
    
    // 多类别AI工具来源
    this.discoverySources = {
      // 类别1: 专业AI工具目录（最可靠）
      ai_directories: {
        'futuretools': {
          name: 'FutureTools',
          url: 'https://www.futuretools.io/',
          type: 'directory',
          reliability: 'high',
          selector: '.tool-card, .product-item',
          description: '专注于未来技术的工具目录'
        },
        'aitoolsdirectory': {
          name: 'AI Tools Directory',
          url: 'https://www.aitoolsdirectory.com/',
          type: 'directory',
          reliability: 'high',
          selector: '.tool-listing, .tool-item',
          description: '全面的AI工具分类目录'
        },
        'toolfinderai': {
          name: 'Tool Finder AI',
          url: 'https://www.toolfinder.ai/',
          type: 'directory',
          reliability: 'medium',
          selector: '.tool-card, .app-card',
          description: 'AI工具搜索引擎'
        }
      },
      
      // 类别2: GitHub仓库和开源项目
      github_repos: {
        'awesome_ai': {
          name: 'Awesome AI',
          url: 'https://github.com/topics/awesome-ai',
          type: 'github',
          reliability: 'very-high',
          selector: '.Box-row',
          description: 'GitHub上的AI工具合集'
        },
        'ai_startups': {
          name: 'AI Startups',
          url: 'https://github.com/topics/ai-startups',
          type: 'github',
          reliability: 'high',
          selector: '.Box-row',
          description: 'AI创业公司和技术'
        },
        'machine_learning': {
          name: 'Machine Learning',
          url: 'https://github.com/topics/machine-learning',
          type: 'github',
          reliability: 'very-high',
          selector: '.Box-row',
          description: '机器学习相关项目'
        }
      },
      
      // 类别3: 科技媒体和博客
      tech_media: {
        'techcrunch_ai': {
          name: 'TechCrunch AI',
          url: 'https://techcrunch.com/tag/artificial-intelligence/',
          type: 'media',
          reliability: 'high',
          selector: 'article, .post-block',
          description: '科技媒体AI报道'
        },
        'venturebeat_ai': {
          name: 'VentureBeat AI',
          url: 'https://venturebeat.com/category/ai/',
          type: 'media',
          reliability: 'high',
          selector: 'article, .ArticleListing',
          description: '创投媒体AI新闻'
        }
      },
      
      // 类别4: 社区和论坛
      communities: {
        'reddit_machinelearning': {
          name: 'Reddit MachineLearning',
          url: 'https://www.reddit.com/r/MachineLearning/',
          type: 'community',
          reliability: 'medium',
          selector: '[data-testid="post-title"]',
          description: 'Reddit机器学习社区'
        },
        'reddit_artificial': {
          name: 'Reddit Artificial',
          url: 'https://www.reddit.com/r/artificial/',
          type: 'community',
          reliability: 'medium',
          selector: '[data-testid="post-title"]',
          description: 'Reddit人工智能社区'
        },
        'hackernews_ai': {
          name: 'Hacker News AI',
          url: 'https://news.ycombinator.com/item?id=35034692',
          type: 'community',
          reliability: 'high',
          selector: '.athing',
          description: 'Hacker News AI讨论'
        }
      },
      
      // 类别5: API和数据集
      api_datasets: {
        'ai_apis': {
          name: 'AI APIs',
          url: 'https://rapidapi.com/collections/ai',
          type: 'api',
          reliability: 'very-high',
          selector: '.api-item, .collection-item',
          description: 'RapidAPI上的AI相关API'
        },
        'kaggle_datasets': {
          name: 'Kaggle AI Datasets',
          url: 'https://www.kaggle.com/datasets?tags=ai',
          type: 'dataset',
          reliability: 'very-high',
          selector: '.sc-iIPllB',
          description: 'Kaggle上的AI数据集'
        }
      },
      
      // 类别6: 投资机构组合
      vc_portfolios: {
        'a16z_ai': {
          name: 'a16z AI Investments',
          url: 'https://a16z.com/category/ai/',
          type: 'vc',
          reliability: 'very-high',
          selector: '.post-item, article',
          description: 'a16z投资的AI公司'
        },
        'ycombinator_ai': {
          name: 'Y Combinator AI',
          url: 'https://www.ycombinator.com/companies?query=AI',
          type: 'vc',
          reliability: 'very-high',
          selector: '.company-name',
          description: 'Y Combinator孵化的AI公司'
        }
      }
    };
    
    // 发现策略配置
    this.discoveryStrategies = {
      daily: ['ai_directories', 'github_repos'], // 每日检查
      weekly: ['tech_media', 'communities'],      // 每周检查
      monthly: ['api_datasets', 'vc_portfolios']  // 每月检查
    };
  }
  
  /**
   * 智能发现AI工具
   */
  async discoverAITools(strategy = 'daily') {
    console.log(`🚀 启动AI工具发现系统 - ${strategy}策略`);
    console.log('='.repeat(60));
    
    const tools = new Map();
    const categories = this.discoveryStrategies[strategy] || this.discoveryStrategies.daily;
    
    for (const category of categories) {
      console.log(`\n📂 探索类别: ${category.replace('_', ' ').toUpperCase()}`);
      
      const sources = this.discoverySources[category];
      if (!sources) continue;
      
      for (const [sourceKey, sourceConfig] of Object.entries(sources)) {
        console.log(`  🔍 来源: ${sourceConfig.name}`);
        
        try {
          const discoveredTools = await this.scrapeSource(sourceConfig);
          
          if (discoveredTools.length === 0) {
            console.log(`    ⚠️  未发现工具`);
            continue;
          }
          
          // 处理发现的工具
          for (const tool of discoveredTools) {
            const toolKey = `${tool.name}-${tool.url}`;
            
            if (!tools.has(toolKey)) {
              tools.set(toolKey, {
                ...tool,
                discoveredFrom: [sourceConfig.name],
                discoveryDate: new Date().toISOString(),
                discoveryConfidence: this.calculateConfidence(sourceConfig.reliability)
              });
            } else {
              const existing = tools.get(toolKey);
              existing.discoveredFrom.push(sourceConfig.name);
              existing.discoveryConfidence = Math.max(
                existing.discoveryConfidence,
                this.calculateConfidence(sourceConfig.reliability)
              );
            }
          }
          
          console.log(`    ✅ 发现 ${discoveredTools.length} 个工具`);
          
          // 智能延迟
          await this.randomDelay(2000, 5000);
          
        } catch (error) {
          console.log(`    ❌ 错误: ${error.message}`);
          continue;
        }
      }
    }
    
    // 转换和排序
    const toolsArray = Array.from(tools.values());
    toolsArray.sort((a, b) => {
      // 按置信度、来源数量、发现时间排序
      const scoreA = (a.discoveryConfidence || 0) * 10 + a.discoveredFrom.length;
      const scoreB = (b.discoveryConfidence || 0) * 10 + b.discoveredFrom.length;
      return scoreB - scoreA;
    });
    
    console.log('\n' + '='.repeat(60));
    console.log(`🎉 发现完成！共发现 ${toolsArray.length} 个潜在AI工具`);
    
    // 生成发现报告
    await this.generateDiscoveryReport(toolsArray, strategy);
    
    // 保存到数据库
    await this.saveToDatabase(toolsArray);
    
    return toolsArray;
  }
  
  /**
   * 从特定来源爬取
   */
  async scrapeSource(sourceConfig) {
    try {
      const response = await axios.get(sourceConfig.url, this.config);
      const $ = cheerio.load(response.data);
      
      const tools = [];
      const elements = $(sourceConfig.selector);
      
      elements.each((i, element) => {
        const tool = this.parseElement($, element, sourceConfig);
        if (tool && tool.name && this.isAITool(tool)) {
          tools.push(tool);
        }
      });
      
      // 对于GitHub特殊处理
      if (sourceConfig.type === 'github') {
        return this.processGitHubTools(tools, $);
      }
      
      return tools.slice(0, 20); // 限制数量
      
    } catch (error) {
      console.error(`爬取 ${sourceConfig.name} 失败:`, error.message);
      return [];
    }
  }
  
  /**
   * 解析元素
   */
  parseElement($, element, sourceConfig) {
    const baseTool = {
      name: $(element).find('h1, h2, h3, h4, .title, .name').first().text().trim(),
      url: $(element).find('a').first().attr('href'),
      description: $(element).find('p, .description, .summary').first().text().trim(),
      source: sourceConfig.name,
      sourceType: sourceConfig.type
    };
    
    // 特殊处理不同类型的来源
    switch (sourceConfig.type) {
      case 'github':
        baseTool.stars = $(element).find('[aria-label*="star"]').text().trim();
        baseTool.language = $(element).find('[itemprop="programmingLanguage"]').text().trim();
        break;
        
      case 'media':
        baseTool.date = $(element).find('time, .date').text().trim();
        baseTool.author = $(element).find('.author, .byline').text().trim();
        break;
        
      case 'community':
        baseTool.votes = $(element).closest('div').find('[aria-label*="vote"]').text().trim();
        baseTool.comments = $(element).closest('div').find('[href*="comments"]').text().trim();
        break;
        
      case 'vc':
        baseTool.stage = this.extractStage($(element).text());
        baseTool.founded = this.extractYear($(element).text());
        break;
    }
    
    // 确保URL完整
    if (baseTool.url && !baseTool.url.startsWith('http')) {
      baseTool.url = new URL(baseTool.url, sourceConfig.url).href;
    }
    
    return baseTool;
  }
  
  /**
   * 处理GitHub工具
   */
  processGitHubTools(tools, $) {
    return tools
      .filter(tool => {
        // 过滤非AI项目
        const name = tool.name.toLowerCase();
        const desc = (tool.description || '').toLowerCase();
        
        const aiKeywords = ['ai', 'artificial', 'machine learning', 'deep learning', 'nlp', 'computer vision', 'chatgpt', 'gpt', 'llm', 'neural'];
        return aiKeywords.some(keyword => name.includes(keyword) || desc.includes(keyword));
      })
      .map(tool => ({
        ...tool,
        category: this.classifyGitHubProject(tool)
      }));
  }
  
  /**
   * 判断是否是AI工具
   */
  isAITool(tool) {
    if (!tool.name || tool.name.length < 2 || tool.name.length > 100) {
      return false;
    }
    
    // 排除明显非工具的名称
    const excluded = ['home', 'about', 'contact', 'login', 'signup', 'privacy', 'terms'];
    if (excluded.some(word => tool.name.toLowerCase().includes(word))) {
      return false;
    }
    
    // 检查AI关键词
    const aiKeywords = [
      'ai', 'artificial', 'intelligence', 'machine', 'deep', 'learning',
      'nlp', 'natural language', 'computer vision', 'chatbot', 'gpt',
      'transformer', 'neural', 'model', 'algorithm', 'automation',
      'predictive', 'analytics', 'cognitive', 'robotics', 'vision'
    ];
    
    const text = (tool.name + ' ' + (tool.description || '')).toLowerCase();
    return aiKeywords.some(keyword => text.includes(keyword));
  }
  
  /**
   * 分类GitHub项目
   */
  classifyGitHubProject(tool) {
    const text = (tool.name + ' ' + (tool.description || '')).toLowerCase();
    
    if (text.includes('chat') || text.includes('gpt') || text.includes('llm')) {
      return '对话AI';
    } else if (text.includes('vision') || text.includes('image') || text.includes('video')) {
      return '计算机视觉';
    } else if (text.includes('speech') || text.includes('audio') || text.includes('voice')) {
      return '语音识别';
    } else if (text.includes('nlp') || text.includes('natural language') || text.includes('text')) {
      return '自然语言处理';
    } else if (text.includes('data') || text.includes('analytics') || text.includes('prediction')) {
      return '数据分析';
    } else {
      return 'AI工具';
    }
  }
  
  /**
   * 提取公司阶段
   */
  extractStage(text) {
    const stages = ['seed', 'series a', 'series b', 'series c', 'growth', 'late stage'];
    const lowerText = text.toLowerCase();
    
    for (const stage of stages) {
      if (lowerText.includes(stage)) {
        return stage.toUpperCase();
      }
    }
    
    return '未知';
  }
  
  /**
   * 提取成立年份
   */
  extractYear(text) {
    const match = text.match(/20\d{2}/);
    return match ? match[0] : '未知';
  }
  
  /**
   * 计算置信度
   */
  calculateConfidence(reliability) {
    const confidenceMap = {
      'very-high': 0.9,
      'high': 0.7,
      'medium': 0.5,
      'low': 0.3
    };
    
    return confidenceMap[reliability] || 0.5;
  }
  
  /**
   * 随机延迟
   */
  async randomDelay(minMs, maxMs) {
    const delay = minMs + Math.random() * (maxMs - minMs);
    await new Promise(resolve => setTimeout(resolve, delay));
  }
  
  /**
   * 生成发现报告
   */
  async generateDiscoveryReport(tools, strategy) {
    const reportDir = path.join(__dirname, '..', 'reports', 'discovery');
    await fs.mkdir(reportDir, { recursive: true });
    
    const now = new Date();
    const timestamp = now.toISOString().replace(/[:.]/g, '-');
    
    let report = `# AI工具发现报告\n\n`;
    report += `## 📋 报告摘要\n\n`;
    report += `- **发现策略**: ${strategy}\n`;
    report += `- **发现时间**: ${now.toLocaleString('zh-CN')}\n`;
    report += `- **发现总数**: ${tools.length}\n`;
    report += `- **高置信度**: ${tools.filter(t => t.discoveryConfidence >= 0.7).length}\n`;
    report += `- **新发现**: ${tools.filter(t => t.discoveryDate.includes(now.toISOString().split('T')[0])).length}\n\n`;
    
    // 按来源统计
    report += `## 📊 来源贡献\n\n`;
    const sourceStats = {};
    tools.forEach(tool => {
      tool.discoveredFrom.forEach(source => {
        sourceStats[source] = (sourceStats[source] || 0) + 1;
      });
    });
    
    Object.entries(sourceStats)
      .sort((a, b) => b[1] - a[1])
      .forEach(([source, count]) => {
        report += `- **${source}**: ${count} 个工具\n`;
      });
    
    // 按类别统计
    report += `\n## 🗂️ 工具分类\n\n`;
    const categoryStats = {};
    tools.forEach(tool => {
      const category = tool.category || '未分类';
      categoryStats[category] = (categoryStats[category] || 0) + 1;
    });
    
    Object.entries(categoryStats)
      .sort((a, b) => b[1] - a[1])
      .forEach(([category, count]) => {
        const percentage = ((count / tools.length) * 100).toFixed(1);
        report += `- **${category}**: ${count} 个工具 (${percentage}%)\n`;
      });
    
    // 高质量工具列表
    const highConfidenceTools = tools.filter(t => t.discoveryConfidence >= 0.7);
    if (highConfidenceTools.length > 0) {
      report += `\n## 🌟 高质量发现 (前10名)\n\n`;
      report += '| 工具名称 | 类别 | 置信度 | 来源 |\n';
      report += '|----------|------|--------|------|\n';
      
      highConfidenceTools.slice(0, 10).forEach(tool => {
        report += `| ${tool.name} | ${tool.category || '未分类'} | ${(tool.discoveryConfidence * 100).toFixed(0)}% | ${tool.discoveredFrom.slice(0, 2).join(', ')} |\n`;
      });
    }
    
    // 建议行动
    report += `\n## 🎯 建议行动\n\n`;
    report += `1. **优先评估**: ${highConfidenceTools.slice(0, 3).map(t => t.name).join(', ')}\n`;
    report += `2. **扩大发现**: 考虑添加更多来源如学术论文、专利数据库\n`;
    report += `3. **自动化跟进**: 对高质量工具设置自动监控\n`;
    report += `4. **人工审核**: 对置信度≥80%的工具进行人工验证\n`;
    
    const reportPath = path.join(reportDir, `discovery_${strategy}_${timestamp}.md`);
    await fs.writeFile(reportPath, report, 'utf-8');
    
    console.log(`📄 发现报告已保存: ${reportPath}`);
    
    return reportPath;
  }
  
  /**
   * 保存到数据库
   */
  async saveToDatabase(tools) {
    try {
      const dbPath = path.join(__dirname, '..', 'data', 'discovered_tools.json');
      
      // 读取现有数据
      let existingData = { tools: [], lastUpdated: '' };
      try {
        const existingContent = await fs.readFile(dbPath, 'utf-8');
        existingData = JSON.parse(existingContent);
      } catch (error) {
        // 文件不存在，创建新文件
      }
      
      // 合并工具（避免重复）
      const existingTools = new Map();
      existingData.tools.forEach(tool => {
        existingTools.set(`${tool.name}-${tool.url}`, tool);
      });
      
      tools.forEach(tool => {
        const key = `${tool.name}-${tool.url}`;
        if (!existingTools.has(key)) {
          existingTools.set(key, tool);
        } else {
          // 更新现有工具
          const existing = existingTools.get(key);
          existing.discoveredFrom = [...new Set([...existing.discoveredFrom, ...tool.discoveredFrom])];
          existing.discoveryConfidence = Math.max(existing.discoveryConfidence, tool.discoveryConfidence);
        }
      });
      
      // 保存更新后的数据
      const updatedData = {
        tools: Array.from(existingTools.values()),
        lastUpdated: new Date().toISOString(),
        totalTools: existingTools.size,
        stats: {
          byCategory: this.calculateStats(Array.from(existingTools.values())),
          bySource: this.calculateSourceStats(Array.from(existingTools.values()))
        }
      };
      
      await fs.writeFile(dbPath, JSON.stringify(updatedData, null, 2), 'utf-8');
      
      console.log(`💾 已保存 ${tools.length} 个工具到数据库，总计 ${existingTools.size} 个工具`);
      
    } catch (error) {
      console.error('保存到数据库失败:', error.message);
    }
  }
  
  /**
   * 计算统计信息
   */
  calculateStats(tools) {
    const stats = {};
    tools.forEach(tool => {
      const category = tool.category || '未分类';
      stats[category] = (stats[category] || 0) + 1;
    });
    return stats;
  }
  
  /**
   * 计算来源统计
   */
  calculateSourceStats(tools) {
    const stats = {};
    tools.forEach(tool => {
      tool.discoveredFrom.forEach(source => {
        stats[source] = (stats[source] || 0) + 1;
      });
    });
    return stats;
  }
}

// 命令行接口
if (require.main === module) {
  const discoverySystem = new AIDiscoverySystem();
  
  const args = process.argv.slice(2);
  const command = args[0] || 'daily';
  
  async function main() {
    try {
      if (['daily', 'weekly', 'monthly', 'full'].includes(command)) {
        console.log(`使用 ${command} 发现策略...`);
        await discoverySystem.discoverAITools(command);
      } else {
        console.log('AI工具发现系统');
        console.log('用法:');
        console.log('  node src/ai_discovery_system.js daily    - 每日发现（默认）');
        console.log('  node src/ai_discovery_system.js weekly   - 每周发现');
        console.log('  node src/ai_discovery_system.js monthly  - 每月发现');
        console.log('  node src/ai_discovery_system.js full     - 完整发现');
      }
    } catch (error) {
      console.error('执行失败:', error);
      process.exit(1);
    }
  }
  
  main();
}

module.exports = AIDiscoverySystem;