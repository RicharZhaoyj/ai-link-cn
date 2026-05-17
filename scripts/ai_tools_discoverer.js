#!/usr/bin/env node

/**
 * AI工具发现和监控脚本
 * 自动发现新的AI工具，定期更新内容库
 */

const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs').promises;
const path = require('path');

// 配置
const CONFIG = {
    // 搜索频率（分钟）
    checkInterval: 60 * 24, // 每天检查一次
    
    // 监控源
    sources: [
        {
            name: 'Futurepedia',
            url: 'https://www.futurepedia.io/',
            type: 'website',
            selector: '.tool-card'
        },
        {
            name: "There's An AI For That",
            url: 'https://theresanaiforthat.com/',
            type: 'website',
            selector: '.tool-item'
        },
        {
            name: 'Product Hunt AI',
            url: 'https://www.producthunt.com/topics/ai',
            type: 'website',
            selector: '.styles_item__Dk_nz'
        },
        {
            name: 'AI Valley',
            url: 'https://aivalley.ai/',
            type: 'website',
            selector: '.tool-card'
        }
    ],
    
    // 输出目录
    outputDir: './discovered_tools',
    
    // 数据库文件
    databaseFile: './ai_tools_database.json',
    
    // 日志文件
    logFile: './discovery_log.json'
};

// 工具数据库
let toolDatabase = {
    tools: [],
    lastUpdated: null,
    stats: {
        totalTools: 0,
        newThisWeek: 0,
        newThisMonth: 0,
        categories: {}
    }
};

class AIToolsDiscoverer {
    constructor() {
        this.initialize();
    }
    
    async initialize() {
        console.log('🚀 AI工具发现器初始化...');
        
        // 创建输出目录
        await this.ensureDirectory(CONFIG.outputDir);
        
        // 加载现有数据库
        await this.loadDatabase();
        
        console.log(`📊 已加载 ${toolDatabase.tools.length} 个工具到数据库`);
    }
    
    async ensureDirectory(dirPath) {
        try {
            await fs.mkdir(dirPath, { recursive: true });
        } catch (error) {
            console.error(`创建目录失败: ${dirPath}`, error);
        }
    }
    
    async loadDatabase() {
        try {
            const data = await fs.readFile(CONFIG.databaseFile, 'utf8');
            toolDatabase = JSON.parse(data);
            console.log('✅ 数据库加载成功');
        } catch (error) {
            console.log('📝 创建新数据库');
            await this.saveDatabase();
        }
    }
    
    async saveDatabase() {
        try {
            toolDatabase.lastUpdated = new Date().toISOString();
            await fs.writeFile(CONFIG.databaseFile, JSON.stringify(toolDatabase, null, 2), 'utf8');
            console.log('💾 数据库保存成功');
        } catch (error) {
            console.error('❌ 保存数据库失败:', error);
        }
    }
    
    async logDiscovery(tool, source) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            source: source.name,
            tool: tool.name,
            url: tool.url,
            status: tool.isNew ? 'new' : 'existing'
        };
        
        try {
            const logPath = path.join(CONFIG.outputDir, 'discovery_log.json');
            let logs = [];
            
            try {
                const logData = await fs.readFile(logPath, 'utf8');
                logs = JSON.parse(logData);
            } catch (error) {
                // 文件不存在，创建新的
            }
            
            logs.push(logEntry);
            
            // 只保留最近100条日志
            if (logs.length > 100) {
                logs = logs.slice(-100);
            }
            
            await fs.writeFile(logPath, JSON.stringify(logs, null, 2), 'utf8');
        } catch (error) {
            console.error('记录日志失败:', error);
        }
    }
    
    async scrapeFuturepedia() {
        console.log('🔍 扫描 Futurepedia...');
        
        try {
            const response = await axios.get(CONFIG.sources[0].url, {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            });
            
            const $ = cheerio.load(response.data);
            const tools = [];
            
            $('.tool-card').each((index, element) => {
                try {
                    const name = $(element).find('h3').text().trim();
                    const url = $(element).find('a').attr('href');
                    const description = $(element).find('p').text().trim();
                    const category = $(element).find('.category').text().trim();
                    
                    if (name && url) {
                        tools.push({
                            name,
                            url: url.startsWith('http') ? url : `https://www.futurepedia.io${url}`,
                            description: description || '暂无描述',
                            category: category || '未分类',
                            source: 'Futurepedia',
                            discoveredAt: new Date().toISOString(),
                            status: 'new'
                        });
                    }
                } catch (error) {
                    console.error('解析工具失败:', error);
                }
            });
            
            console.log(`✅ 从 Futurepedia 发现 ${tools.length} 个工具`);
            return tools;
        } catch (error) {
            console.error('❌ 扫描 Futurepedia 失败:', error.message);
            return [];
        }
    }
    
    async scrapeProductHunt() {
        console.log('🔍 扫描 Product Hunt AI...');
        
        try {
            const response = await axios.get(CONFIG.sources[2].url, {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            });
            
            const $ = cheerio.load(response.data);
            const tools = [];
            
            $('.styles_item__Dk_nz').each((index, element) => {
                try {
                    const name = $(element).find('.styles_fontSize16__xqA6z').text().trim();
                    const url = $(element).find('a').attr('href');
                    const description = $(element).find('.styles_fontSize14__R7_0U').text().trim();
                    const votes = $(element).find('.styles_voteCount__NYmlS').text().trim();
                    
                    if (name && url) {
                        tools.push({
                            name,
                            url: url.startsWith('http') ? url : `https://www.producthunt.com${url}`,
                            description: description || '暂无描述',
                            votes: votes || '0',
                            source: 'Product Hunt',
                            discoveredAt: new Date().toISOString(),
                            status: 'new'
                        });
                    }
                } catch (error) {
                    console.error('解析工具失败:', error);
                }
            });
            
            console.log(`✅ 从 Product Hunt 发现 ${tools.length} 个工具`);
            return tools;
        } catch (error) {
            console.error('❌ 扫描 Product Hunt 失败:', error.message);
            return [];
        }
    }
    
    async discoverNewTools() {
        console.log('🎯 开始发现新的AI工具...');
        
        const allTools = [];
        
        // 扫描 Futurepedia
        const futurepediaTools = await this.scrapeFuturepedia();
        allTools.push(...futurepediaTools);
        
        // 扫描 Product Hunt
        const productHuntTools = await this.scrapeProductHunt();
        allTools.push(...productHuntTools);
        
        // 去重和检查是否已存在
        const uniqueTools = this.deduplicateTools(allTools);
        const newTools = this.filterNewTools(uniqueTools);
        
        console.log(`📊 发现统计:`);
        console.log(`  总共发现: ${allTools.length} 个工具`);
        console.log(`  去重后: ${uniqueTools.length} 个工具`);
        console.log(`  新工具: ${newTools.length} 个`);
        
        // 保存新工具
        if (newTools.length > 0) {
            await this.saveNewTools(newTools);
        }
        
        return newTools;
    }
    
    deduplicateTools(tools) {
        const uniqueMap = new Map();
        
        tools.forEach(tool => {
            const key = tool.name.toLowerCase().trim();
            if (!uniqueMap.has(key)) {
                uniqueMap.set(key, tool);
            }
        });
        
        return Array.from(uniqueMap.values());
    }
    
    filterNewTools(tools) {
        const existingNames = new Set(toolDatabase.tools.map(t => t.name.toLowerCase()));
        return tools.filter(tool => !existingNames.has(tool.name.toLowerCase()));
    }
    
    async saveNewTools(newTools) {
        console.log('💾 保存新工具到数据库...');
        
        // 添加到数据库
        newTools.forEach(tool => {
            toolDatabase.tools.push(tool);
            
            // 更新统计
            toolDatabase.stats.totalTools++;
            toolDatabase.stats.newThisWeek++;
            toolDatabase.stats.newThisMonth++;
            
            // 更新分类统计
            const category = tool.category || '未分类';
            if (!toolDatabase.stats.categories[category]) {
                toolDatabase.stats.categories[category] = 0;
            }
            toolDatabase.stats.categories[category]++;
        });
        
        // 保存数据库
        await this.saveDatabase();
        
        // 生成新工具报告
        await this.generateNewToolsReport(newTools);
        
        console.log(`✅ 成功保存 ${newTools.length} 个新工具`);
    }
    
    async generateNewToolsReport(tools) {
        console.log('📄 生成新工具报告...');
        
        const report = {
            generatedAt: new Date().toISOString(),
            totalNewTools: tools.length,
            tools: tools.map(tool => ({
                name: tool.name,
                url: tool.url,
                description: tool.description,
                category: tool.category,
                source: tool.source,
                discoveredAt: tool.discoveredAt
            })),
            summary: `发现 ${tools.length} 个新的AI工具，来自 ${new Set(tools.map(t => t.source)).size} 个来源`
        };
        
        // 生成Markdown报告
        const markdownReport = this.generateMarkdownReport(report);
        
        // 保存报告
        const reportPath = path.join(CONFIG.outputDir, `new_tools_${Date.now()}.md`);
        await fs.writeFile(reportPath, markdownReport, 'utf8');
        
        console.log(`📋 报告已保存: ${reportPath}`);
        
        return reportPath;
    }
    
    generateMarkdownReport(report) {
        const lines = [
            `# 新AI工具发现报告`,
            `生成时间: ${new Date(report.generatedAt).toLocaleString('zh-CN')}`,
            ``,
            `## 发现统计`,
            `- 发现工具总数: ${report.totalNewTools}`,
            `- 报告生成时间: ${new Date().toLocaleString('zh-CN')}`,
            ``,
            `## 新工具列表`,
            ``
        ];
        
        // 按来源分组
        const toolsBySource = {};
        report.tools.forEach(tool => {
            if (!toolsBySource[tool.source]) {
                toolsBySource[tool.source] = [];
            }
            toolsBySource[tool.source].push(tool);
        });
        
        // 添加每个来源的工具
        Object.entries(toolsBySource).forEach(([source, tools]) => {
            lines.push(`### ${source} (${tools.length}个)`);
            lines.push(``);
            
            tools.forEach(tool => {
                lines.push(`#### ${tool.name}`);
                lines.push(`- **分类**: ${tool.category}`);
                lines.push(`- **描述**: ${tool.description || '暂无描述'}`);
                lines.push(`- **链接**: [访问官网](${tool.url})`);
                lines.push(`- **发现时间**: ${new Date(tool.discoveredAt).toLocaleString('zh-CN')}`);
                lines.push(``);
            });
        });
        
        lines.push(`## 下一步行动建议`);
        lines.push(``);
        lines.push(`1. **优先评测**: 选择3-5个最有潜力的工具进行深度评测`);
        lines.push(`2. **快速介绍**: 为所有新工具创建简要介绍页面`);
        lines.push(`3. **社交媒体分享**: 分享最有意思的新工具`);
        lines.push(`4. **用户调研**: 了解用户对这些新工具的兴趣程度`);
        lines.push(``);
        lines.push(`---`);
        lines.push(`*本报告由AI工具发现器自动生成*`);
        
        return lines.join('\n');
    }
    
    async analyzeToolPotential(tool) {
        // 简单的潜力分析
        const potentialScore = {
            nameLength: tool.name.length > 5 && tool.name.length < 30 ? 2 : 1,
            hasDescription: tool.description && tool.description.length > 20 ? 2 : 1,
            hasCategory: tool.category && tool.category !== '未分类' ? 2 : 1,
            popularSource: ['Product Hunt', 'Futurepedia'].includes(tool.source) ? 2 : 1,
            urlValid: tool.url && tool.url.startsWith('http') ? 2 : 1
        };
        
        const totalScore = Object.values(potentialScore).reduce((a, b) => a + b, 0);
        const maxScore = 10;
        
        return {
            score: totalScore,
            maxScore: maxScore,
            percentage: Math.round((totalScore / maxScore) * 100),
            factors: potentialScore
        };
    }
    
    async generateContentIdeas(tools) {
        console.log('💡 生成内容创意...');
        
        const contentIdeas = [];
        
        for (const tool of tools.slice(0, 10)) { // 只分析前10个
            const potential = await this.analyzeToolPotential(tool);
            
            if (potential.percentage >= 60) {
                contentIdeas.push({
                    tool: tool.name,
                    potential: potential.percentage,
                    contentIdeas: [
                        `"${tool.name}初体验：新发布的AI工具有哪些亮点？"`,
                        `"对比分析：${tool.name} vs 传统工具的优势"`,
                        `"实用教程：如何用${tool.name}提升工作效率"`,
                        `"行业应用：${tool.name}在不同场景下的使用案例"`
                    ],
                    priority: potential.percentage >= 80 ? '高' : potential.percentage >= 60 ? '中' : '低'
                });
            }
        }
        
        // 生成内容创意报告
        const ideasReport = this.generateContentIdeasReport(contentIdeas);
        const ideasPath = path.join(CONFIG.outputDir, `content_ideas_${Date.now()}.md`);
        await fs.writeFile(ideasPath, ideasReport, 'utf8');
        
        console.log(`💡 已生成 ${contentIdeas.length} 个内容创意`);
        
        return ideasPath;
    }
    
    generateContentIdeasReport(ideas) {
        const lines = [
            `# AI工具内容创意报告`,
            `生成时间: ${new Date().toLocaleString('zh-CN')}`,
            ``,
            `## 概述`,
            `基于新发现的AI工具，生成了以下内容创意：`,
            ``
        ];
        
        // 按优先级分组
        const ideasByPriority = {
            '高': [],
            '中': [],
            '低': []
        };
        
        ideas.forEach(idea => {
            ideasByPriority[idea.priority].push(idea);
        });
        
        // 添加高优先级创意
        if (ideasByPriority['高'].length > 0) {
            lines.push(`## 🚀 高优先级内容创意`);
            lines.push(``);
            
            ideasByPriority['高'].forEach((idea, index) => {
                lines.push(`### ${index + 1}. ${idea.tool} (潜力: ${idea.potential}%)`);
                lines.push(`**内容创意:**`);
                idea.contentIdeas.forEach(contentIdea => {
                    lines.push(`- ${contentIdea}`);
                });
                lines.push(``);
            });
        }
        
        // 添加中优先级创意
        if (ideasByPriority['中'].length > 0) {
            lines.push(`## ⚡ 中优先级内容创意`);
            lines.push(``);
            
            ideasByPriority['中'].forEach((idea, index) => {
                lines.push(`### ${ideasByPriority['高'].length + index + 1}. ${idea.tool} (潜力: ${idea.potential}%)`);
                lines.push(`**内容创意:**`);
                idea.contentIdeas.forEach(contentIdea => {
                    lines.push(`- ${contentIdea}`);
                });
                lines.push(``);
            });
        }
        
        lines.push(`## 📋 执行建议`);
        lines.push(``);
        lines.push(`1. **立即行动**: 选择2-3个高优先级工具开始评测`);
        lines.push(`2. **社交媒体预热**: 分享工具发现和初步印象`);
        lines.push(`3. **用户调研**: 调查用户对哪些工具最感兴趣`);
        lines.push(`4. **建立内容日历**: 规划未来2-4周的内容发布`);
        lines.push(``);
        lines.push(`---`);
        lines.push(`*本报告由AI工具发现器自动生成*`);
        
        return lines.join('\n');
    }
    
    async run() {
        console.log('🎬 开始执行AI工具发现任务...');
        
        try {
            // 发现新工具
            const newTools = await this.discoverNewTools();
            
            if (newTools.length > 0) {
                // 生成内容创意
                await this.generateContentIdeas(newTools);
                
                console.log('\n🎉 发现任务完成！');
                console.log(`发现 ${newTools.length} 个新工具`);
                console.log(`报告已保存到: ${CONFIG.outputDir}`);
            } else {
                console.log('\n📭 本次未发现新工具');
            }
            
            // 保存数据库
            await this.saveDatabase();
            
        } catch (error) {
            console.error('❌ 发现任务失败:', error);
        }
    }
}

// 执行脚本
async function main() {
    const discoverer = new AIToolsDiscoverer();
    await discoverer.run();
    
    // 如果是定时任务，可以设置定时器
    if (process.argv.includes('--schedule')) {
        console.log(`⏰ 已设置为定时任务，每 ${CONFIG.checkInterval} 分钟运行一次`);
        setInterval(async () => {
            await discoverer.run();
        }, CONFIG.checkInterval * 60 * 1000);
    }
}

// 处理命令行参数
if (require.main === module) {
    main().catch(console.error);
}

module.exports = AIToolsDiscoverer;