/**
 * AI工具内容生成器
 * 用于生成高质量的内容文章
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

class ContentGenerator {
  constructor() {
    this.templatesDir = path.join(__dirname, '..', 'templates');
    this.contentDir = path.join(__dirname, '..', 'content');
    this.seoKeywords = {};
  }
  
  /**
   * 初始化内容生成器
   */
  async initialize() {
    try {
      // 加载SEO关键词
      await this.loadSEOKeywords();
      
      // 确保目录存在
      await fs.mkdir(this.contentDir, { recursive: true });
      await fs.mkdir(this.templatesDir, { recursive: true });
      
      console.log('内容生成器初始化完成');
      
    } catch (error) {
      console.error('初始化内容生成器失败:', error);
      await this.createDefaultTemplates();
    }
  }
  
  /**
   * 加载SEO关键词
   */
  async loadSEOKeywords() {
    try {
      const keywordsFile = path.join(__dirname, '..', 'config', 'seo_keywords.json');
      const data = await fs.readFile(keywordsFile, 'utf-8');
      this.seoKeywords = JSON.parse(data);
    } catch (error) {
      console.log('SEO关键词文件不存在，使用默认关键词');
      this.seoKeywords = this.getDefaultKeywords();
    }
  }
  
  /**
   * 获取默认SEO关键词
   */
  getDefaultKeywords() {
    return {
      primary: ['AI工具', '人工智能工具', 'AI软件', 'AI应用'],
      secondary: ['最佳', '评测', '比较', '推荐', '教程', '使用指南', '2025'],
      categories: {
        '写作': ['AI写作工具', '文案生成', '内容创作', '语法检查'],
        '图像': ['AI图像生成', '图片编辑', '艺术创作', '设计工具'],
        '代码': ['AI编程工具', '代码生成', '开发辅助', '编程助手'],
        '视频': ['AI视频生成', '视频编辑', '动画制作', '视频工具'],
        '音频': ['AI音频工具', '语音合成', '音乐生成', '声音编辑']
      }
    };
  }
  
  /**
   * 创建默认模板
   */
  async createDefaultTemplates() {
    const templates = {
      'tool_review.md': this.getToolReviewTemplate(),
      'comparison.md': this.getComparisonTemplate(),
      'tutorial.md': this.getTutorialTemplate(),
      'news.md': this.getNewsTemplate()
    };
    
    for (const [filename, content] of Object.entries(templates)) {
      const filepath = path.join(this.templatesDir, filename);
      await fs.writeFile(filepath, content, 'utf-8');
    }
    
    console.log('已创建默认模板');
  }
  
  /**
   * 生成工具评测文章
   */
  async generateToolReview(toolInfo, category = 'general') {
    const template = await this.loadTemplate('tool_review.md');
    
    // 生成SEO标题
    const seoTitle = this.generateSEOTitle(toolInfo.name, '评测');
    
    // 生成关键词
    const keywords = this.generateKeywords(toolInfo.name, category, '评测');
    
    // 生成内容
    const content = template
      .replace('{{TITLE}}', seoTitle)
      .replace('{{TOOL_NAME}}', toolInfo.name)
      .replace('{{TOOL_DESCRIPTION}}', toolInfo.description || '')
      .replace('{{TOOL_URL}}', toolInfo.url || '')
      .replace('{{PRICING}}', toolInfo.pricing || '未提供定价信息')
      .replace('{{CATEGORY}}', category)
      .replace('{{KEYWORDS}}', keywords.join(', '))
      .replace('{{DATE}}', new Date().toLocaleDateString('zh-CN'))
      .replace('{{AFFILIATE_LINK}}', toolInfo.affiliateUrl || toolInfo.url || '');
    
    // 添加内容部分
    const sections = this.generateReviewSections(toolInfo);
    const fullContent = content.replace('{{CONTENT_SECTIONS}}', sections);
    
    // 生成文件名
    const filename = this.generateFilename(toolInfo.name, 'review');
    const filepath = path.join(this.contentDir, 'tools', filename);
    
    // 确保目录存在
    await fs.mkdir(path.dirname(filepath), { recursive: true });
    
    // 写入文件
    await fs.writeFile(filepath, fullContent, 'utf-8');
    
    console.log(`已生成评测文章: ${filepath}`);
    
    return {
      filename,
      filepath,
      title: seoTitle,
      wordCount: this.countWords(fullContent)
    };
  }
  
  /**
   * 生成评测内容部分
   */
  generateReviewSections(toolInfo) {
    const sections = [];
    
    // 功能介绍
    sections.push(`## 功能介绍\n\n${toolInfo.description || '该工具提供了多种AI功能。'}\n`);
    
    // 主要特性
    if (toolInfo.features && toolInfo.features.length > 0) {
      sections.push('## 主要特性\n\n');
      toolInfo.features.forEach(feature => {
        sections.push(`- ${feature}\n`);
      });
      sections.push('\n');
    }
    
    // 定价分析
    sections.push('## 定价分析\n\n');
    sections.push(`当前定价方案: ${toolInfo.pricing || '未提供详细定价信息'}\n\n`);
    
    // 优缺点分析
    sections.push('## 优缺点分析\n\n### ✅ 优点\n\n');
    sections.push('- 功能强大，效果出色\n');
    sections.push('- 用户界面友好，易于使用\n');
    sections.push('- 社区活跃，资源丰富\n\n');
    
    sections.push('### ❌ 缺点\n\n');
    sections.push('- 定价相对较高\n');
    sections.push('- 部分高级功能需要学习\n');
    sections.push('- 可能需要较高的硬件配置\n\n');
    
    // 使用建议
    sections.push('## 使用建议\n\n');
    sections.push('### 适合人群\n\n');
    sections.push('- 内容创作者和写作者\n');
    sections.push('- 设计师和艺术家\n');
    sections.push('- 开发者和技术人员\n');
    sections.push('- 学生和教育工作者\n\n');
    
    sections.push('### 最佳使用场景\n\n');
    sections.push('1. **日常内容创作**: 快速生成文章、博客、社交媒体内容\n');
    sections.push('2. **专业项目**: 协助完成复杂的设计或开发任务\n');
    sections.push('3. **学习研究**: 作为学习和探索AI技术的工具\n\n');
    
    // 替代方案
    sections.push('## 替代方案\n\n');
    sections.push('如果你在寻找类似的工具，可以考虑以下替代方案:\n\n');
    sections.push('1. **[替代工具1]**: 更侧重于[某方面]\n');
    sections.push('2. **[替代工具2]**: 定价更经济\n');
    sections.push('3. **[替代工具3]**: 更适合[特定需求]\n\n');
    
    // 总结
    sections.push('## 总结\n\n');
    sections.push(`${toolInfo.name} 是一款功能强大的AI工具，适合需要高质量AI辅助的用户。虽然定价可能较高，但其功能和效果值得投资。\n\n`);
    
    sections.push('> 💡 **提示**: 通过我们的链接注册，你可能会获得专属优惠或额外功能。\n');
    
    return sections.join('');
  }
  
  /**
   * 生成比较文章
   */
  async generateComparison(tools, category = 'general') {
    const template = await this.loadTemplate('comparison.md');
    
    // 生成SEO标题
    const toolNames = tools.map(t => t.name).join(' vs ');
    const seoTitle = `${toolNames} 比较: 哪个更适合你？`;
    
    // 生成内容
    let content = template
      .replace('{{TITLE}}', seoTitle)
      .replace('{{TOOLS}}', toolNames)
      .replace('{{CATEGORY}}', category)
      .replace('{{DATE}}', new Date().toLocaleDateString('zh-CN'));
    
    // 生成比较表格
    const comparisonTable = this.generateComparisonTable(tools);
    content = content.replace('{{COMPARISON_TABLE}}', comparisonTable);
    
    // 生成分析部分
    const analysis = this.generateComparisonAnalysis(tools);
    content = content.replace('{{ANALYSIS}}', analysis);
    
    // 生成文件名
    const filename = this.generateFilename(toolNames.replace(/ vs /g, '-vs-'), 'comparison');
    const filepath = path.join(this.contentDir, 'comparisons', filename);
    
    // 确保目录存在
    await fs.mkdir(path.dirname(filepath), { recursive: true });
    
    // 写入文件
    await fs.writeFile(filepath, content, 'utf-8');
    
    console.log(`已生成比较文章: ${filepath}`);
    
    return {
      filename,
      filepath,
      title: seoTitle,
      wordCount: this.countWords(content)
    };
  }
  
  /**
   * 生成比较表格
   */
  generateComparisonTable(tools) {
    let table = '| 特性 | ' + tools.map(t => t.name).join(' | ') + ' |\n';
    table += '|------|' + tools.map(() => '------').join('|') + '|\n';
    
    // 价格比较
    table += `| 价格 | ${tools.map(t => t.pricing || '未提供').join(' | ')} |\n`;
    
    // 主要功能
    table += `| 主要功能 | ${tools.map(t => t.description?.substring(0, 50) + '...' || '未提供').join(' | ')} |\n`;
    
    // 适合人群
    table += `| 适合人群 | ${tools.map(() => '内容创作者、设计师、开发者').join(' | ')} |\n`;
    
    // 免费试用
    table += `| 免费试用 | ${tools.map(() => '✅ 可用').join(' | ')} |\n`;
    
    // 移动端支持
    table += `| 移动端支持 | ${tools.map(() => '✅ 支持').join(' | ')} |\n`;
    
    return table;
  }
  
  /**
   * 生成比较分析
   */
  generateComparisonAnalysis(tools) {
    const sections = [];
    
    tools.forEach((tool, index) => {
      sections.push(`### ${tool.name}\n\n`);
      sections.push(`**优点**:\n\n`);
      sections.push('- 功能全面，效果出色\n');
      sections.push('- 用户界面友好\n');
      sections.push('- 社区支持良好\n\n`);
      
      sections.push(`**缺点**:\n\n`);
      sections.push('- 定价可能较高\n');
      sections.push('- 需要学习成本\n\n`);
      
      sections.push(`**最佳使用场景**: ${tool.description?.substring(0, 100) || '通用AI辅助'}\n\n`);
      
      if (index < tools.length - 1) {
        sections.push('---\n\n');
      }
    });
    
    // 总结建议
    sections.push('## 总结建议\n\n');
    
    if (tools.length === 2) {
      sections.push(`1. **如果你注重[某方面]**，选择 ${tools[0].name}\n`);
      sections.push(`2. **如果你需要[另一功能]**，选择 ${tools[1].name}\n`);
    } else {
      sections.push('根据你的具体需求和预算，选择最适合的工具:\n\n');
      tools.forEach(tool => {
        sections.push(`- **${tool.name}**: ${tool.pricing || '未提供定价'} - ${tool.description?.substring(0, 80) || ''}\n`);
      });
    }
    
    return sections.join('');
  }
  
  /**
   * 生成SEO标题
   */
  generateSEOTitle(toolName, type) {
    const prefixes = [
      `${toolName} ${type}: `,
      `${toolName} - `,
      `${toolName}完全${type}: `,
      `最全面的${toolName}${type}: `
    ];
    
    const suffixes = [
      '2025最新评测',
      '功能详解与使用指南',
      '优缺点分析',
      '定价与使用建议',
      '完整使用教程'
    ];
    
    const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
    const suffix = suffixes[Math.floor(Math.random() * suffixes.length)];
    
    return prefix + suffix;
  }
  
  /**
   * 生成关键词
   */
  generateKeywords(toolName, category, type) {
    const keywords = [];
    
    // 主要关键词
    keywords.push(`${toolName} ${type}`);
    keywords.push(`${toolName} 评测`);
    keywords.push(`${toolName} 使用教程`);
    
    // 类别关键词
    if (this.seoKeywords.categories[category]) {
      keywords.push(...this.seoKeywords.categories[category]);
    }
    
    // 通用关键词
    keywords.push(...this.seoKeywords.primary);
    keywords.push(...this.seoKeywords.secondary.map(s => `${toolName} ${s}`));
    
    // 去重
    return [...new Set(keywords)];
  }
  
  /**
   * 生成文件名
   */
  generateFilename(toolName, type) {
    const slug = toolName.toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fa5]/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
    
    const date = new Date().toISOString().split('T')[0];
    const hash = crypto.createHash('md5').update(toolName + type).digest('hex').substring(0, 6);
    
    return `${date}-${slug}-${type}-${hash}.md`;
  }
  
  /**
   * 加载模板
   */
  async loadTemplate(templateName) {
    try {
      const filepath = path.join(this.templatesDir, templateName);
      return await fs.readFile(filepath, 'utf-8');
    } catch (error) {
      console.log(`模板 ${templateName} 不存在，使用默认模板`);
      return this.getDefaultTemplate(templateName);
    }
  }
  
  /**
   * 获取默认模板
   */
  getDefaultTemplate(templateName) {
    switch (templateName) {
      case 'tool_review.md':
        return this.getToolReviewTemplate();
      case 'comparison.md':
        return this.getComparisonTemplate();
      default:
        return '# 内容模板\n\n{{CONTENT}}';
    }
  }
  
  /**
   * 工具评测模板
   */
  getToolReviewTemplate() {
    return `---
title: "{{TITLE}}"
date: {{DATE}}
author: AI.link.cn
categories: ["{{CATEGORY}}"]
tags: [{{KEYWORDS}}]
affiliate_link: "{{AFFILIATE_LINK}}"
tool_url: "{{TOOL_URL}}"
---

# {{TITLE}}

> 💡 **本文最后更新于**: {{DATE}}
> 📊 **工具**: {{TOOL_NAME}}
> 💰 **定价**: {{PRICING}}

{{TOOL_DESCRIPTION}}

{{CONTENT_SECTIONS}}

---

## 相关资源

- [{{TOOL_NAME}} 官方网站]({{TOOL_URL}})
- [查看更多AI工具评测](/tools)
- [订阅我们的新闻通讯](/subscribe)

---

**免责声明**: 本文包含Affiliate链接，如果您通过我们的链接购买，我们可能会获得佣金。这不会影响您的购买价格。

> 🎯 **开始使用**: [立即体验{{TOOL_NAME}} →]({{AFFILIATE_LINK}})
`;
  }
  
  /**
   * 比较文章模板
   */
  getComparisonTemplate() {
    return `---
title: "{{TITLE}}"
date: {{DATE}}
author: AI.link.cn
categories: ["{{CATEGORY}}"]
tags: ["AI工具比较", "{{TOOLS}}"]
---

# {{TITLE}}

> 📊 **比较工具**: {{TOOLS}}
> 📅 **更新时间**: {{DATE}}

选择合适的AI工具可能很困难。本文将对 {{TOOLS}} 进行详细比较，帮助你做出最佳选择。

{{COMPARISON_TABLE}}

{{ANALYSIS}}

---

## 常见问题

### Q: 我应该选择哪个工具？
A: 这取决于你的具体需求、预算和使用场景。参考上面的详细比较做出决定。

### Q: 这些工具都有免费试用吗？
A: 大多数AI工具都提供免费试用或免费版本，建议先试用再决定购买。

### Q: 如何获得最佳价格？
A: 关注官方优惠活动，或通过我们的Affiliate链接注册，有时会有专属优惠。

---

**相关阅读**:
- [查看更多工具比较](/comparisons)
- [{{CATEGORY}}类工具推荐](/category/{{CATEGORY}})

> 💡 **提示**: 所有工具都提供免费试用，建议先试用再决定购买。
`;
  }
  
  /**
   * 教程模板
   */
  getTutorialTemplate() {
    return `# {{TITLE}}

{{INTRODUCTION}}

## 准备工作

{{PREREQUISITES}}

## 步骤详解

{{STEPS}}

## 总结

{{CONCLUSION}}
`;
  }
  
  /**
   * 新闻模板
   */
  getNewsTemplate() {
    return `# {{TITLE}}

{{SUMMARY}}

## 主要内容

{{CONTENT}}

## 影响分析

{{IMPACT}}

## 相关链接

{{LINKS}}
`;
  }
  
  /**
   * 统计字数
   */
  countWords(text) {
    return text.split(/\s+/).length;
  }
}

// 命令行接口
if (require.main === module) {
  const generator = new ContentGenerator();
  
  const args = process.argv.slice(2);
  const command = args[0];
  
  async function main() {
    await generator.initialize();
    
    try {
      if (command === 'review') {
        const toolName = args[1];
        const toolUrl = args[2];
        const category = args[3] || 'general';
        
        if (!toolName) {
          console.error('请提供工具名称');
          console.error('用法: node src/content_generator.js review <工具名称> [URL] [类别]');
          process.exit(1);
        }
        
        const toolInfo = {
          name: toolName,
          url: toolUrl,
          description: `${toolName}是一款功能强大的AI工具，提供多种人工智能功能。`,
          pricing: '免费试用，付费版$20/月起',
          features: [
            '智能内容生成',
            '多语言支持',
            '高质量输出',
            '用户友好界面'
          ]
        };
        
        const result = await generator.generateToolReview(toolInfo, category);
        console.log('评测文章已生成:', result);
        
      } else if (command === 'compare') {
        const toolNames = args.slice(1);
        
        if (toolNames.length < 2) {
          console.error('请提供至少两个工具名称');
          console.error('用法: node src/content_generator.js compare <工具1> <工具2> [工具3...]');
          process.exit(1);
        }
        
        const tools = toolNames.map(name => ({
          name,
          description: `${name}是一款AI工具`,
          pricing: '免费试用，付费版$20/月起'
        }));
        
        const result = await generator.generateComparison(tools);
        console.log('比较文章已生成:', result);
        
      } else if (command === 'template') {
        const templateName = args[1];
        
        if (!templateName) {
          console.error('请提供模板名称');
          console.error('用法: node src/content_generator.js template <模板名称>');
          process.exit(1);
        }
        
        const template = await generator.loadTemplate(templateName);
        console.log(template);
        
      } else {
        console.log('内容生成器');
        console.log('用法:');
        console.log('  node src/content_generator.js review <工具名称> [URL] [类别] - 生成工具评测');
        console.log('  node src/content_generator.js compare <工具1> <工具2> ... - 生成比较文章');
        console.log('  node src/content_generator.js template <名称> - 查看模板');
      }
    } catch (error) {
      console.error('执行失败:', error);
      process.exit(1);
    }
  }
  
  main();
}

module.exports = ContentGenerator;