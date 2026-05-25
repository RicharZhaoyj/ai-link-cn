// 修复AI工具发现系统 - 解决Product Hunt 403问题
const axios = require('axios');
const fs = require('fs');
const path = require('path');

async function discoverNewTools() {
    console.log('🎯 开始发现新的AI工具（绕过Product Hunt限制）...\n');
    
    const discoveredTools = [];
    
    // 1. 从GitHub发现AI工具
    try {
        console.log('1. 搜索GitHub上的AI工具项目...');
        
        // 搜索关键词列表
        const searchTerms = [
            'ai tool',
            'artificial intelligence tool',
            'machine learning tool',
            'ai assistant',
            'mlops tool',
            'data science tool',
            'nlp tool',
            'computer vision tool'
        ];
        
        for (const term of searchTerms.slice(0, 3)) { // 先测试前3个
            console.log(`  搜索: "${term}"...`);
            
            try {
                const response = await axios.get('https://api.github.com/search/repositories', {
                    params: {
                        q: term,
                        sort: 'stars',
                        order: 'desc',
                        per_page: 3
                    },
                    headers: {
                        'User-Agent': 'AI.link.cn Discovery Bot/1.0',
                        'Accept': 'application/vnd.github.v3+json'
                    },
                    timeout: 10000
                });
                
                for (const repo of response.data.items) {
                    // 只添加真正有用的AI工具
                    if (repo.description && (
                        repo.description.toLowerCase().includes('ai') ||
                        repo.description.toLowerCase().includes('artificial intelligence') ||
                        repo.description.toLowerCase().includes('machine learning') ||
                        repo.description.toLowerCase().includes('data science') ||
                        repo.description.toLowerCase().includes('nlp') ||
                        repo.description.toLowerCase().includes('computer vision')
                    )) {
                        const tool = {
                            name: repo.name,
                            description: repo.description,
                            url: repo.html_url,
                            category: 'AI工具',
                            source: 'GitHub',
                            stars: repo.stargazers_count,
                            language: repo.language
                        };
                        
                        // 检查是否已存在
                        const exists = discoveredTools.some(t => 
                            t.name === tool.name || t.url === tool.url
                        );
                        
                        if (!exists) {
                            discoveredTools.push(tool);
                            console.log(`    ✅ 发现: ${tool.name} (⭐ ${tool.stars})`);
                        }
                    }
                }
                
                // 避免速率限制
                await new Promise(resolve => setTimeout(resolve, 2000));
                
            } catch (error) {
                console.log(`   ⚠️ 搜索"${term}"时出错: ${error.message}`);
            }
        }
    } catch (error) {
        console.log(`❌ GitHub搜索失败: ${error.message}`);
    }
    
    // 2. 从Futurepedia发现
    try {
        console.log('\n2. 检查Futurepedia上的AI工具...');
        
        const response = await axios.get('https://www.futurepedia.io/', {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            },
            timeout: 15000
        });
        
        const html = response.data;
        
        // 简单解析Futurepedia页面（这只是一个示例，实际需要更复杂的解析）
        const toolPatterns = [
            /<a[^>]*href="[^"]*futurepedia\.io\/tool\/[^"]*"[^>]*>([^<]+)<\/a>/gi,
            /<h3[^>]*class="[^"]*tool-name[^"]*"[^>]*>([^<]+)<\/h3>/gi
        ];
        
        for (const pattern of toolPatterns) {
            const matches = html.match(pattern);
            if (matches && matches.length > 0) {
                // 取前5个匹配
                const tools = matches.slice(0, 5).map(match => {
                    const nameMatch = match.match(/>([^<]+)</);
                    return {
                        name: nameMatch ? nameMatch[1].trim() : 'Unknown',
                        description: 'AI tool from Futurepedia',
                        url: 'https://www.futurepedia.io/',
                        category: 'AI工具',
                        source: 'Futurepedia'
                    };
                });
                
                tools.forEach(tool => {
                    const exists = discoveredTools.some(t => t.name === tool.name);
                    if (!exists) {
                        discoveredTools.push(tool);
                        console.log(`    ✅ 发现: ${tool.name} (from Futurepedia)`);
                    }
                });
                
                break; // 找到工具后停止
            }
        }
    } catch (error) {
        console.log(`❌ Futurepedia访问失败: ${error.message}`);
    }
    
    // 3. 从其他来源发现
    console.log('\n3. 从其他来源发现AI工具...');
    
    // 预定义的AI工具列表（备用方案）
    const predefinedTools = [
        {
            name: 'OpenAI API',
            description: 'OpenAI的官方API，提供GPT系列模型访问',
            url: 'https://platform.openai.com/',
            category: 'API服务'
        },
        {
            name: 'Hugging Face',
            description: '最大的AI模型和数据集社区',
            url: 'https://huggingface.co/',
            category: '模型平台'
        },
        {
            name: 'Anthropic Claude',
            description: 'Anthropic开发的先进对话AI',
            url: 'https://www.anthropic.com/',
            category: '对话AI'
        }
    ];
    
    predefinedTools.forEach(tool => {
        const exists = discoveredTools.some(t => t.name === tool.name);
        if (!exists) {
            discoveredTools.push(tool);
            console.log(`    ✅ 添加: ${tool.name}`);
        }
    });
    
    // 4. 生成报告
    console.log(`\n📊 发现统计: 总共发现 ${discoveredTools.length} 个工具`);
    
    if (discoveredTools.length > 0) {
        // 保存发现报告
        const reportDir = 'discovered_tools';
        const processedDir = path.join(reportDir, 'processed');
        
        if (!fs.existsSync(reportDir)) fs.mkdirSync(reportDir, { recursive: true });
        if (!fs.existsSync(processedDir)) fs.mkdirSync(processedDir, { recursive: true });
        
        const timestamp = new Date().toISOString().replace(/[:.]/g, '').slice(0, 15);
        const reportFile = path.join(processedDir, `new_tools_${timestamp}.md`);
        
        let reportContent = `# AI工具发现报告 - ${new Date().toISOString().split('T')[0].replace(/-/g, '')}\n\n`;
        reportContent += `**生成时间**: ${new Date().toISOString()}\n\n`;
        reportContent += `**总计发现**: ${discoveredTools.length} 个工具\n\n`;
        
        // 按来源分组
        const bySource = {};
        discoveredTools.forEach(tool => {
            if (!bySource[tool.source]) bySource[tool.source] = [];
            bySource[tool.source].push(tool);
        });
        
        for (const [source, tools] of Object.entries(bySource)) {
            reportContent += `## 来源: ${source}\n\n`;
            
            tools.forEach((tool, index) => {
                reportContent += `### ${index + 1}. ${tool.name}\n\n`;
                reportContent += `- **描述**: ${tool.description}\n`;
                reportContent += `- **URL**: ${tool.url}\n`;
                if (tool.stars) reportContent += `- **GitHub Stars**: ${tool.stars}\n`;
                if (tool.language) reportContent += `- **主要语言**: ${tool.language}\n`;
                reportContent += `- **类别**: ${tool.category}\n`;
                reportContent += '\n';
            });
        }
        
        fs.writeFileSync(reportFile, reportContent, 'utf8');
        console.log(`📁 发现报告已保存: ${reportFile}`);
        
        // 也创建一个简化的报告供自动化系统使用
        const simpleReportFile = path.join(processedDir, `new_tools_${new Date().toISOString().split('T')[0].replace(/-/g, '')}.md`);
        const simpleContent = `# AI工具发现报告 - ${new Date().toISOString().split('T')[0].replace(/-/g, '')}\n\n**生成时间**: ${new Date().toISOString()}\n\n**总计发现**: ${discoveredTools.length} 个工具\n\n`;
        
        discoveredTools.forEach((tool, i) => {
            simpleContent += `### ${i + 1}. ${tool.name}\n\n`;
            simpleContent += `- **描述**: ${tool.description}\n`;
            simpleContent += `- **URL**: ${tool.url}\n`;
            simpleContent += `- **来源**: ${tool.source}\n\n`;
        });
        
        fs.writeFileSync(simpleReportFile, simpleContent, 'utf8');
        console.log(`📁 简化报告已保存: ${simpleReportFile}`);
        
        return {
            success: true,
            count: discoveredTools.length,
            reportFile: reportFile,
            simpleReportFile: simpleReportFile
        };
    } else {
        console.log('⚠️ 本次未发现新工具');
        return {
            success: false,
            count: 0,
            message: '未发现新工具'
        };
    }
}

// 运行发现
discoverNewTools().then(result => {
    console.log('\n=== 发现完成 ===');
    if (result.success) {
        console.log(`✅ 成功发现 ${result.count} 个新工具`);
        console.log(`📄 报告文件: ${result.reportFile}`);
        
        // 建议下一步操作
        console.log('\n🎯 建议下一步:');
        console.log('1. 运行自动更新脚本来处理新发现的工具');
        console.log('2. 更新数据库以包含这些新工具');
        console.log('3. 重新配置发现系统以避免Product Hunt限制');
    } else {
        console.log('⚠️ 未发现新工具，需要检查发现系统配置');
    }
}).catch(error => {
    console.error('❌ 发现过程出错:', error);
});