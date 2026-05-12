/**
 * Affiliate链接管理系统
 * 用于管理和跟踪Affiliate链接的性能
 */

const fs = require('fs').promises;
const path = require('path');

class AffiliateTracker {
  constructor() {
    this.affiliateConfigFile = path.join(__dirname, '..', 'config', 'affiliate_links.json');
    this.statsFile = path.join(__dirname, '..', 'data', 'affiliate_stats.json');
    this.affiliateLinks = new Map();
    this.stats = {
      totalClicks: 0,
      totalConversions: 0,
      totalRevenue: 0,
      byTool: {},
      byDate: {}
    };
  }
  
  /**
   * 初始化Affiliate管理器
   */
  async initialize() {
    try {
      // 加载配置
      await this.loadConfig();
      
      // 加载统计数据
      await this.loadStats();
      
      console.log('Affiliate管理器初始化完成');
      console.log(`已加载 ${this.affiliateLinks.size} 个Affiliate链接`);
      
    } catch (error) {
      console.error('初始化Affiliate管理器失败:', error);
      // 如果文件不存在，创建默认配置
      await this.createDefaultConfig();
    }
  }
  
  /**
   * 加载Affiliate配置
   */
  async loadConfig() {
    try {
      const data = await fs.readFile(this.affiliateConfigFile, 'utf-8');
      const config = JSON.parse(data);
      
      // 转换为Map以便快速查找
      this.affiliateLinks.clear();
      config.links.forEach(link => {
        this.affiliateLinks.set(link.id, link);
      });
      
    } catch (error) {
      console.log('Affiliate配置文件不存在，将创建默认配置');
      await this.createDefaultConfig();
    }
  }
  
  /**
   * 创建默认Affiliate配置
   */
  async createDefaultConfig() {
    const defaultLinks = [
      {
        id: 'chatgpt_plus',
        name: 'ChatGPT Plus',
        toolName: 'ChatGPT',
        type: 'subscription',
        url: 'https://chat.openai.com/',
        affiliateUrl: 'https://chat.openai.com/?ref=ailink',
        platform: 'OpenAI',
        commission: '$20-50/新用户',
        commissionType: 'per_signup',
        status: 'pending', // pending, active, inactive
        lastChecked: new Date().toISOString(),
        notes: '需要申请Affiliate项目'
      },
      {
        id: 'midjourney',
        name: 'Midjourney',
        toolName: 'Midjourney',
        type: 'subscription',
        url: 'https://www.midjourney.com/',
        affiliateUrl: 'https://www.midjourney.com/?ref=ailink',
        platform: 'Midjourney',
        commission: '20-30%月费分成',
        commissionType: 'percentage_recurring',
        status: 'pending',
        lastChecked: new Date().toISOString(),
        notes: 'Discord内申请'
      },
      {
        id: 'notion_ai',
        name: 'Notion AI',
        toolName: 'Notion',
        type: 'subscription',
        url: 'https://www.notion.so/product/ai',
        affiliateUrl: 'https://www.notion.so/product/ai?ref=ailink',
        platform: 'Notion',
        commission: '$10-20/新用户',
        commissionType: 'per_signup',
        status: 'pending',
        lastChecked: new Date().toISOString(),
        notes: '通过ShareASale平台'
      },
      {
        id: 'grammarly',
        name: 'Grammarly',
        toolName: 'Grammarly',
        type: 'subscription',
        url: 'https://www.grammarly.com/',
        affiliateUrl: 'https://www.grammarly.com/?ref=ailink',
        platform: 'Grammarly',
        commission: '20%年费分成',
        commissionType: 'percentage_one_time',
        status: 'pending',
        lastChecked: new Date().toISOString(),
        notes: '通过Impact平台'
      },
      {
        id: 'jasper_ai',
        name: 'Jasper AI',
        toolName: 'Jasper',
        type: 'subscription',
        url: 'https://www.jasper.ai/',
        affiliateUrl: 'https://www.jasper.ai/?ref=ailink',
        platform: 'Jasper',
        commission: '30%月费',
        commissionType: 'percentage_recurring',
        status: 'pending',
        lastChecked: new Date().toISOString(),
        notes: '高转化率'
      }
    ];
    
    const config = {
      version: '1.0.0',
      lastUpdated: new Date().toISOString(),
      links: defaultLinks
    };
    
    // 确保目录存在
    const configDir = path.dirname(this.affiliateConfigFile);
    await fs.mkdir(configDir, { recursive: true });
    
    // 写入配置文件
    await fs.writeFile(this.affiliateConfigFile, JSON.stringify(config, null, 2));
    
    // 加载到内存
    defaultLinks.forEach(link => {
      this.affiliateLinks.set(link.id, link);
    });
    
    console.log('已创建默认Affiliate配置');
  }
  
  /**
   * 加载统计数据
   */
  async loadStats() {
    try {
      const data = await fs.readFile(this.statsFile, 'utf-8');
      this.stats = JSON.parse(data);
    } catch (error) {
      console.log('统计数据文件不存在，将创建新文件');
      await this.saveStats();
    }
  }
  
  /**
   * 保存统计数据
   */
  async saveStats() {
    try {
      const dataDir = path.dirname(this.statsFile);
      await fs.mkdir(dataDir, { recursive: true });
      
      await fs.writeFile(this.statsFile, JSON.stringify(this.stats, null, 2));
    } catch (error) {
      console.error('保存统计数据失败:', error);
    }
  }
  
  /**
   * 获取Affiliate链接
   */
  getAffiliateLink(toolName) {
    // 查找匹配的工具
    for (const link of this.affiliateLinks.values()) {
      if (link.toolName.toLowerCase().includes(toolName.toLowerCase()) ||
          toolName.toLowerCase().includes(link.toolName.toLowerCase())) {
        return link;
      }
    }
    
    return null;
  }
  
  /**
   * 获取所有Affiliate链接
   */
  getAllAffiliateLinks() {
    return Array.from(this.affiliateLinks.values());
  }
  
  /**
   * 添加Affiliate链接
   */
  async addAffiliateLink(linkData) {
    const id = linkData.id || this.generateId(linkData.name);
    
    const newLink = {
      id,
      ...linkData,
      created: new Date().toISOString(),
      lastChecked: new Date().toISOString(),
      status: linkData.status || 'active'
    };
    
    this.affiliateLinks.set(id, newLink);
    
    // 更新配置文件
    await this.saveConfig();
    
    return newLink;
  }
  
  /**
   * 更新Affiliate链接
   */
  async updateAffiliateLink(id, updates) {
    if (!this.affiliateLinks.has(id)) {
      throw new Error(`Affiliate链接 ${id} 不存在`);
    }
    
    const link = this.affiliateLinks.get(id);
    const updatedLink = {
      ...link,
      ...updates,
      lastUpdated: new Date().toISOString()
    };
    
    this.affiliateLinks.set(id, updatedLink);
    
    // 更新配置文件
    await this.saveConfig();
    
    return updatedLink;
  }
  
  /**
   * 记录点击
   */
  async recordClick(affiliateId, source = 'direct') {
    const today = new Date().toISOString().split('T')[0];
    
    // 更新总点击
    this.stats.totalClicks += 1;
    
    // 更新工具统计
    if (!this.stats.byTool[affiliateId]) {
      this.stats.byTool[affiliateId] = {
        clicks: 0,
        conversions: 0,
        revenue: 0
      };
    }
    this.stats.byTool[affiliateId].clicks += 1;
    
    // 更新日期统计
    if (!this.stats.byDate[today]) {
      this.stats.byDate[today] = {
        clicks: 0,
        conversions: 0,
        revenue: 0
      };
    }
    this.stats.byDate[today].clicks += 1;
    
    // 保存统计数据
    await this.saveStats();
    
    return {
      affiliateId,
      clicks: this.stats.byTool[affiliateId].clicks,
      date: today
    };
  }
  
  /**
   * 记录转化
   */
  async recordConversion(affiliateId, revenue = 0, source = 'direct') {
    const today = new Date().toISOString().split('T')[0];
    
    // 更新总转化
    this.stats.totalConversions += 1;
    this.stats.totalRevenue += revenue;
    
    // 更新工具统计
    if (!this.stats.byTool[affiliateId]) {
      this.stats.byTool[affiliateId] = {
        clicks: 0,
        conversions: 0,
        revenue: 0
      };
    }
    this.stats.byTool[affiliateId].conversions += 1;
    this.stats.byTool[affiliateId].revenue += revenue;
    
    // 更新日期统计
    if (!this.stats.byDate[today]) {
      this.stats.byDate[today] = {
        clicks: 0,
        conversions: 0,
        revenue: 0
      };
    }
    this.stats.byDate[today].conversions += 1;
    this.stats.byDate[today].revenue += revenue;
    
    // 保存统计数据
    await this.saveStats();
    
    return {
      affiliateId,
      conversions: this.stats.byTool[affiliateId].conversions,
      revenue: this.stats.byTool[affiliateId].revenue,
      date: today
    };
  }
  
  /**
   * 获取统计报告
   */
  getStatsReport() {
    const report = {
      summary: {
        totalClicks: this.stats.totalClicks,
        totalConversions: this.stats.totalConversions,
        totalRevenue: this.stats.totalRevenue,
        conversionRate: this.stats.totalClicks > 0 
          ? (this.stats.totalConversions / this.stats.totalClicks * 100).toFixed(2) + '%'
          : '0%',
        averageRevenuePerClick: this.stats.totalClicks > 0
          ? (this.stats.totalRevenue / this.stats.totalClicks).toFixed(2)
          : 0
      },
      topPerformers: [],
      recentActivity: {}
    };
    
    // 找出表现最好的工具
    const toolStats = Object.entries(this.stats.byTool)
      .map(([id, stats]) => ({
        id,
        ...stats,
        conversionRate: stats.clicks > 0 ? (stats.conversions / stats.clicks * 100).toFixed(2) + '%' : '0%',
        averageRevenue: stats.conversions > 0 ? (stats.revenue / stats.conversions).toFixed(2) : 0
      }))
      .sort((a, b) => b.revenue - a.revenue);
    
    report.topPerformers = toolStats.slice(0, 5);
    
    // 最近30天的活动
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(today.getDate() - 30);
    
    report.recentActivity = Object.entries(this.stats.byDate)
      .filter(([date]) => new Date(date) >= thirtyDaysAgo)
      .reduce((acc, [date, stats]) => {
        acc[date] = stats;
        return acc;
      }, {});
    
    return report;
  }
  
  /**
   * 生成ID
   */
  generateId(name) {
    return name.toLowerCase()
      .replace(/[^a-z0-9]/g, '_')
      .replace(/_+/g, '_')
      .replace(/^_|_$/g, '');
  }
  
  /**
   * 保存配置
   */
  async saveConfig() {
    try {
      const config = {
        version: '1.0.0',
        lastUpdated: new Date().toISOString(),
        links: Array.from(this.affiliateLinks.values())
      };
      
      await fs.writeFile(this.affiliateConfigFile, JSON.stringify(config, null, 2));
    } catch (error) {
      console.error('保存Affiliate配置失败:', error);
    }
  }
}

// 命令行接口
if (require.main === module) {
  const tracker = new AffiliateTracker();
  
  const args = process.argv.slice(2);
  const command = args[0];
  
  async function main() {
    await tracker.initialize();
    
    try {
      if (command === 'list') {
        const links = tracker.getAllAffiliateLinks();
        console.log(JSON.stringify(links, null, 2));
        
      } else if (command === 'stats') {
        const report = tracker.getStatsReport();
        console.log(JSON.stringify(report, null, 2));
        
      } else if (command === 'click') {
        const affiliateId = args[1];
        const source = args[2] || 'direct';
        
        if (!affiliateId) {
          console.error('请提供Affiliate ID');
          console.error('用法: node src/affiliate_tracker.js click <affiliateId> [source]');
          process.exit(1);
        }
        
        const result = await tracker.recordClick(affiliateId, source);
        console.log('点击已记录:', result);
        
      } else if (command === 'conversion') {
        const affiliateId = args[1];
        const revenue = parseFloat(args[2]) || 0;
        const source = args[3] || 'direct';
        
        if (!affiliateId) {
          console.error('请提供Affiliate ID');
          console.error('用法: node src/affiliate_tracker.js conversion <affiliateId> [revenue] [source]');
          process.exit(1);
        }
        
        const result = await tracker.recordConversion(affiliateId, revenue, source);
        console.log('转化已记录:', result);
        
      } else if (command === 'add') {
        // 简化版添加命令，实际应用中应该有完整的表单
        const name = args[1];
        const url = args[2];
        
        if (!name || !url) {
          console.error('请提供工具名称和URL');
          console.error('用法: node src/affiliate_tracker.js add <名称> <URL>');
          process.exit(1);
        }
        
        const linkData = {
          name,
          url,
          toolName: name,
          type: 'subscription',
          status: 'pending'
        };
        
        const newLink = await tracker.addAffiliateLink(linkData);
        console.log('Affiliate链接已添加:', newLink);
        
      } else {
        console.log('Affiliate链接管理系统');
        console.log('用法:');
        console.log('  node src/affiliate_tracker.js list          - 列出所有链接');
        console.log('  node src/affiliate_tracker.js stats         - 查看统计报告');
        console.log('  node src/affiliate_tracker.js click <id>    - 记录点击');
        console.log('  node src/affiliate_tracker.js conversion <id> [revenue] - 记录转化');
        console.log('  node src/affiliate_tracker.js add <名称> <URL> - 添加新链接');
      }
    } catch (error) {
      console.error('执行失败:', error);
      process.exit(1);
    }
  }
  
  main();
}

module.exports = AffiliateTracker;