#!/usr/bin/env node
/**
 * 每日AI工具发现脚本
 * 集成到自动化系统中
 */

const AIDiscoverySystem = require('../src/ai_discovery_system.js');
const fs = require('fs').promises;
const path = require('path');

class DailyAIDiscovery {
  constructor() {
    this.discoverySystem = new AIDiscoverySystem();
    this.logDir = path.join(__dirname, '..', 'logs', 'discovery');
    this.dataDir = path.join(__dirname, '..', 'data');
  }
  
  async run() {
    console.log('🚀 启动每日AI工具发现');
    console.log('='.repeat(60));
    
    const startTime = Date.now();
    
    try {
      // 创建必要的目录
      await fs.mkdir(this.logDir, { recursive: true });
      await fs.mkdir(this.dataDir, { recursive: true });
      
      // 执行每日发现
      console.log('\n📅 执行每日发现策略...');
      const discoveredTools = await this.discoverySystem.discoverAITools('daily');
      
      // 更新主数据库
      await this.updateMainDatabase(discoveredTools);
      
      // 生成今日发现摘要
      await this.generateDailySummary(discoveredTools);
      
      // 检查是否有新工具
      const newTools = await this.identifyNewTools(discoveredTools);
      
      // 如果有新工具，准备更新网站
      if (newTools.length > 0) {
        console.log(`\n🎉 发现 ${newTools.length} 个新工具！`);
        await this.prepareWebsiteUpdate(newTools);
      } else {
        console.log('\n⚠️  今日没有发现新工具');
      }
      
      const executionTime = ((Date.now() - startTime) / 1000).toFixed(2);
      console.log(`\n✅ 每日发现完成！执行时间: ${executionTime}秒`);
      
      return {
        success: true,
        totalDiscovered: discoveredTools.length,
        newTools: newTools.length,
        executionTime
      };
      
    } catch (error) {
      console.error('❌ 每日发现失败:', error);
      
      // 记录错误
      await this.logError(error);
      
      return {
        success: false,
        error: error.message,
        executionTime: ((Date.now() - startTime) / 1000).toFixed(2)
      };
    }
  }
  
  /**
   * 更新主数据库
   */
  async updateMainDatabase(newTools) {
    const dbPath = path.join(this.dataDir, 'ai_tools_database.json');
    
    try {
      // 读取现有数据库
      let database = { tools: [], stats: {} };
      try {
        const content = await fs.readFile(dbPath, 'utf-8');
        database = JSON.parse(content);
      } catch (error) {
        console.log('创建新的数据库文件...');
      }
      
      // 合并工具
      const existingMap = new Map();
      database.tools.forEach(tool => {
        existingMap.set(tool.id || tool.name, tool);
      });
      
      let newCount = 0;
      let updatedCount = 0;
      
      for (const tool of newTools) {
        const toolId = this.generateToolId(tool.name);
        
        if (!existingMap.has(toolId)) {
          // 新工具
          const enhancedTool = this.enhanceToolData(tool, toolId);
          database.tools.push(enhancedTool);
          existingMap.set(toolId, enhancedTool);
          newCount++;
        } else {
          // 更新现有工具
          const existing = existingMap.get(toolId);
          this.mergeToolData(existing, tool);
          updatedCount++;
        }
      }
      
      // 更新统计信息
      database.stats = this.calculateDatabaseStats(database.tools);
      database.lastUpdated = new Date().toISOString();
      database.lastDiscovery = {
        date: new Date().toISOString().split('T')[0],
        newTools: newCount,
        updatedTools: updatedCount,
        totalTools: database.tools.length
      };
      
      // 保存数据库
      await fs.writeFile(dbPath, JSON.stringify(database, null, 2), 'utf-8');
      
      console.log(`💾 数据库更新: ${newCount} 个新工具, ${updatedCount} 个更新工具`);
      
    } catch (error) {
      console.error('更新数据库失败:', error.message);
    }
  }
  
  /**
   * 生成工具ID
   */
  generateToolId(name) {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
  }
  
  /**
   * 增强工具数据
   */
  enhanceToolData(tool, toolId) {
    return {
      id: toolId,
      name: tool.name,
      category: tool.category || this.classifyTool(tool),
      description: tool.description || '',
      url: tool.url || '',
      pricing: '未提供',
      rating: null,
      features: [],
      discoveredFrom: tool.discoveredFrom || [],
      discoveryConfidence: tool.discoveryConfidence || 0.5,
      firstDiscovered: new Date().toISOString(),
      lastUpdated: new Date().toISOString(),
      status: 'discovered', // discovered, reviewed, published
      reviewUrl: `/pages/tools/${toolId}.html`
    };
  }
  
  /**
   * 合并工具数据
   */
  mergeToolData(existing, newData) {
    // 合并来源
    if (newData.discoveredFrom) {
      existing.discoveredFrom = [...new Set([...existing.discoveredFrom, ...newData.discoveredFrom])];
    }
    
    // 更新置信度
    if (newData.discoveryConfidence && newData.discoveryConfidence > (existing.discoveryConfidence || 0)) {
      existing.discoveryConfidence = newData.discoveryConfidence;
    }
    
    // 补充缺失的信息
    if (!existing.description && newData.description) {
      existing.description = newData.description;
    }
    
    if (!existing.category && newData.category) {
      existing.category = newData.category;
    }
    
    existing.lastUpdated = new Date().toISOString();
  }
  
  /**
   * 分类工具
   */
  classifyTool(tool) {
    const text = (tool.name + ' ' + (tool.description || '')).toLowerCase();
    
    const categories = {
      '对话AI': ['chat', 'gpt', 'llm', '对话', '聊天', 'assistant'],
      '图像生成': ['image', 'picture', 'photo', 'art', 'drawing', 'vision'],
      '写作助手': ['write', 'grammar', 'text', 'content', 'editor'],
      '编程助手': ['code', 'programming', 'developer', 'copilot'],
      '视频处理': ['video', 'movie', 'clip', 'animation'],
      '音频处理': ['audio', 'sound', 'voice', 'music', 'speech'],
      '数据分析': ['data', 'analytics', 'insight', 'report'],
      '营销工具': ['marketing', 'seo', 'social', 'ads', 'campaign']
    };
    
    for (const [category, keywords] of Object.entries(categories)) {
      if (keywords.some(keyword => text.includes(keyword))) {
        return category;
      }
    }
    
    return '其他AI工具';
  }
  
  /**
   * 计算数据库统计
   */
  calculateDatabaseStats(tools) {
    const stats = {
      totalTools: tools.length,
      byCategory: {},
      byStatus: {},
      byDiscoveryConfidence: {
        high: tools.filter(t => (t.discoveryConfidence || 0) >= 0.7).length,
        medium: tools.filter(t => (t.discoveryConfidence || 0) >= 0.4 && (t.discoveryConfidence || 0) < 0.7).length,
        low: tools.filter(t => (t.discoveryConfidence || 0) < 0.4).length
      }
    };
    
    tools.forEach(tool => {
      // 按类别
      const category = tool.category || '未分类';
      stats.byCategory[category] = (stats.byCategory[category] || 0) + 1;
      
      // 按状态
      const status = tool.status || 'unknown';
      stats.byStatus[status] = (stats.byStatus[status] || 0) + 1;
    });
    
    return stats;
  }
  
  /**
   * 生成每日摘要
   */
  async generateDailySummary(tools) {
    const summaryDir = path.join(this.logDir, 'summaries');
    await fs.mkdir(summaryDir, { recursive: true });
    
    const today = new Date().toISOString().split('T')[0];
    
    let summary = `# 每日AI工具发现摘要 - ${today}\n\n`;
    summary += `## 📊 发现统计\n\n`;
    summary += `- **发现时间**: ${new Date().toLocaleString('zh-CN')}\n`;
    summary += `- **发现工具总数**: ${tools.length}\n`;
    summary += `- **高置信度工具**: ${tools.filter(t => (t.discoveryConfidence || 0) >= 0.7).length}\n`;
    summary += `- **中等置信度工具**: ${tools.filter(t => (t.discoveryConfidence || 0) >= 0.4 && (t.discoveryConfidence || 0) < 0.7).length}\n`;
    summary += `- **低置信度工具**: ${tools.filter(t => (t.discoveryConfidence || 0) < 0.4).length}\n\n`;
    
    // 高质量发现
    const highConfidenceTools = tools.filter(t => (t.discoveryConfidence || 0) >= 0.7);
    if (highConfidenceTools.length > 0) {
      summary += `## 🌟 高质量发现\n\n`;
      summary += '| 工具名称 | 类别 | 置信度 | 描述 |\n';
      summary += '|----------|------|--------|------|\n';
      
      highConfidenceTools.slice(0, 10).forEach(tool => {
        const description = (tool.description || '').slice(0, 100) + (tool.description && tool.description.length > 100 ? '...' : '');
        summary += `| ${tool.name} | ${tool.category || '未分类'} | ${Math.round((tool.discoveryConfidence || 0) * 100)}% | ${description} |\n`;
      });
    }
    
    // 建议
    summary += `\n## 💡 建议行动\n\n`;
    if (highConfidenceTools.length > 0) {
      summary += `1. **优先评估**: ${highConfidenceTools.slice(0, 3).map(t => t.name).join(', ')}\n`;
    }
    summary += `2. **更新网站**: 如果有新工具，更新网站工具列表\n`;
    summary += `3. **深入调研**: 对高质量工具进行详细研究\n`;
    summary += `4. **监控变化**: 关注工具更新和发展\n`;
    
    const summaryPath = path.join(summaryDir, `summary_${today}.md`);
    await fs.writeFile(summaryPath, summary, 'utf-8');
    
    console.log(`📝 每日摘要已生成: ${summaryPath}`);
    
    return summaryPath;
  }
  
  /**
   * 识别新工具
   */
  async identifyNewTools(discoveredTools) {
    const dbPath = path.join(this.dataDir, 'ai_tools_database.json');
    
    try {
      // 读取现有数据库
      let existingTools = [];
      try {
        const content = await fs.readFile(dbPath, 'utf-8');
        const database = JSON.parse(content);
        existingTools = database.tools || [];
      } catch (error) {
        // 数据库文件不存在，所有工具都是新的
        return discoveredTools;
      }
      
      // 创建现有工具ID集合
      const existingIds = new Set();
      existingTools.forEach(tool => {
        existingIds.add(tool.id || this.generateToolId(tool.name));
      });
      
      // 过滤新工具
      const newTools = discoveredTools.filter(tool => {
        const toolId = this.generateToolId(tool.name);
        return !existingIds.has(toolId);
      });
      
      return newTools;
      
    } catch (error) {
      console.error('识别新工具失败:', error.message);
      return discoveredTools;
    }
  }
  
  /**
   * 准备网站更新
   */
  async prepareWebsiteUpdate(newTools) {
    console.log('\n🔄 准备网站更新...');
    
    // 创建新工具信息文件
    const updateDir = path.join(__dirname, '..', 'updates', new Date().toISOString().split('T')[0]);
    await fs.mkdir(updateDir, { recursive: true });
    
    // 生成新工具JSON文件
    const newToolsData = {
      date: new Date().toISOString(),
      tools: newTools.map(tool => ({
        id: this.generateToolId(tool.name),
        name: tool.name,
        category: tool.classifyTool(tool),
        description: tool.description || '',
        url: tool.url || '',
        discoveredFrom: tool.discoveredFrom || [],
        confidence: tool.discoveryConfidence || 0.5
      })),
      total: newTools.length
    };
    
    const toolsFilePath = path.join(updateDir, 'new_tools.json');
    await fs.writeFile(toolsFilePath, JSON.stringify(newToolsData, null, 2), 'utf-8');
    
    // 生成更新脚本
    const updateScript = this.generateUpdateScript(newToolsData);
    const scriptPath = path.join(updateDir, 'update_website.js');
    await fs.writeFile(scriptPath, updateScript, 'utf-8');
    
    console.log(`📁 更新文件已准备: ${updateDir}`);
    console.log(`📄 新工具数据: ${toolsFilePath}`);
    console.log(`⚡ 更新脚本: ${scriptPath}`);
    
    return {
      updateDir,
      toolsFilePath,
      scriptPath,
      newToolsCount: newTools.length
    };
  }
  
  /**
   * 生成更新脚本
   */
  generateUpdateScript(toolsData) {
    return `/**
 * 网站更新脚本 - 添加新发现的AI工具
 * 生成时间: ${new Date().toLocaleString('zh-CN')}
 */

const fs = require('fs');
const path = require('path');

// 新工具数据
const newTools = ${JSON.stringify(toolsData.tools, null, 2)};

async function updateWebsite() {
  console.log('开始更新网站...');
  
  try {
    // 1. 更新主数据库
    const dbPath = path.join(__dirname, '..', 'ai_tools_database.json');
    let database = { tools: [] };
    
    try {
      const content = fs.readFileSync(dbPath, 'utf-8');
      database = JSON.parse(content);
    } catch (error) {
      console.log('创建新的数据库文件...');
    }
    
    // 添加新工具
    newTools.forEach(tool => {
      const existingIndex = database.tools.findIndex(t => t.id === tool.id);
      if (existingIndex === -1) {
        database.tools.push({
          ...tool,
          addedDate: new Date().toISOString().split('T')[0],
          status: 'new',
          reviewUrl: \`/pages/tools/\${tool.id}.html\`
        });
      }
    });
    
    // 更新统计信息
    database.lastUpdated = new Date().toISOString();
    database.stats = {
      totalTools: database.tools.length,
      newTools: newTools.length,
      updated: new Date().toLocaleString('zh-CN')
    };
    
    fs.writeFileSync(dbPath, JSON.stringify(database, null, 2), 'utf-8');
    console.log(\`✅ 数据库更新完成: 新增 \${newTools.length} 个工具\`);
    
    // 2. 更新网站页面（此处可扩展）
    console.log('ℹ️  网站页面更新需要手动完成');
    console.log('建议步骤:');
    console.log('1. 为每个新工具创建评测页面');
    console.log('2. 更新首页工具展示');
    console.log('3. 更新工具列表页面');
    console.log('4. 添加SEO优化');
    
    return { success: true, newTools: newTools.length };
    
  } catch (error) {
    console.error('更新失败:', error);
    return { success: false, error: error.message };
  }
}

// 执行更新
if (require.main === module) {
  updateWebsite();
}

module.exports = updateWebsite;`;
  }
  
  /**
   * 记录错误
   */
  async logError(error) {
    const errorLogPath = path.join(this.logDir, 'errors.log');
    const errorEntry = `[${new Date().toISOString()}] ${error.message}\n${error.stack}\n\n`;
    
    try {
      await fs.appendFile(errorLogPath, errorEntry, 'utf-8');
    } catch (logError) {
      console.error('记录错误失败:', logError.message);
    }
  }
}

// 命令行接口
if (require.main === module) {
  const dailyDiscovery = new DailyAIDiscovery();
  
  async function main() {
    const result = await dailyDiscovery.run();
    
    if (result.success) {
      console.log('\n🎯 每日发现任务完成！');
      console.log(`📊 统计: ${result.totalDiscovered} 个工具发现, ${result.newTools} 个新工具`);
      process.exit(0);
    } else {
      console.error('\n❌ 每日发现任务失败');
      console.error(`错误: ${result.error}`);
      process.exit(1);
    }
  }
  
  main();
}

module.exports = DailyAIDiscovery;