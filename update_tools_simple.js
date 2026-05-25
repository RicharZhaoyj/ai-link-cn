// 简单工具更新脚本 - 将新发现的工具添加到数据库和网站
const fs = require('fs');
const path = require('path');

async function updateTools() {
    console.log('🔄 开始更新AI工具数据库和网站...\n');
    
    // 1. 加载数据库
    const dbPath = 'ai_tools_database.json';
    let database = { tools: [] };
    
    if (fs.existsSync(dbPath)) {
        try {
            const data = fs.readFileSync(dbPath, 'utf8');
            database = JSON.parse(data);
            console.log(`✅ 数据库加载成功，现有 ${database.tools.length} 个工具`);
        } catch (error) {
            console.log(`❌ 读取数据库失败: ${error.message}`);
            return;
        }
    } else {
        console.log('⚠️ 数据库文件不存在，创建新数据库');
        database = { 
            tools: [],
            metadata: {
                lastUpdated: new Date().toISOString(),
                totalTools: 0
            }
        };
    }
    
    // 2. 解析发现报告
    const reportPath = 'discovered_tools/processed/new_tools_20260525.md';
    if (!fs.existsSync(reportPath)) {
        console.log(`❌ 发现报告文件不存在: ${reportPath}`);
        return;
    }
    
    const reportContent = fs.readFileSync(reportPath, 'utf8');
    console.log(`✅ 发现报告加载成功，大小: ${reportContent.length} 字符`);
    
    // 3. 解析发现报告中的工具
    const newTools = [];
    
    // 简单解析：查找工具名称和描述
    const toolSections = reportContent.split('### ');
    toolSections.shift(); // 移除开头的非工具内容
    
    for (const section of toolSections) {
        const lines = section.split('\n');
        const nameLine = lines[0].trim();
        if (!nameLine) continue;
        
        const name = nameLine.replace(/^\d+\.\s*/, '').trim();
        
        // 提取描述
        let description = '';
        let url = '';
        let category = 'AI工具';
        
        for (const line of lines) {
            if (line.includes('- **描述**:')) {
                description = line.replace('- **描述**:', '').trim();
            } else if (line.includes('- **URL**:')) {
                url = line.replace('- **URL**:', '').trim();
            } else if (line.includes('- **类别**:')) {
                category = line.replace('- **类别**:', '').trim();
            }
        }
        
        if (name && description && url) {
            const toolId = name.toLowerCase().replace(/[^a-z0-9]/g, '-');
            const today = new Date().toISOString().split('T')[0];
            
            const newTool = {
                id: toolId,
                name: name,
                description: description.substring(0, 200), // 限制长度
                category: category || 'AI工具',
                url: url,
                pricing: '免费/开源',
                rating: 4.0,
                pros: ['功能强大', '开源免费'],
                cons: ['可能需要技术知识'],
                addedDate: today,
                lastUpdated: today,
                featured: false,
                reviewUrl: `/pages/tools/${toolId}.html`,
                source: 'GitHub'
            };
            
            // 检查是否已存在
            const exists = database.tools.some(t => t.id === toolId || t.name === name);
            if (!exists) {
                newTools.push(newTool);
                console.log(`   ✅ 发现新工具: ${name}`);
            } else {
                console.log(`   ⏭️  跳过已存在的工具: ${name}`);
            }
        }
    }
    
    if (newTools.length === 0) {
        console.log('⚠️ 没有发现新的工具需要添加');
        return;
    }
    
    console.log(`\n📊 发现 ${newTools.length} 个新工具需要添加到数据库`);
    
    // 4. 添加到数据库
    database.tools.push(...newTools);
    database.metadata = {
        lastUpdated: new Date().toISOString(),
        totalTools: database.tools.length,
        categories: Array.from(new Set(database.tools.map(t => t.category)))
    };
    
    // 5. 保存数据库
    try {
        fs.writeFileSync(dbPath, JSON.stringify(database, null, 2), 'utf8');
        console.log(`✅ 数据库更新成功，现在有 ${database.tools.length} 个工具`);
    } catch (error) {
        console.log(`❌ 保存数据库失败: ${error.message}`);
        return;
    }
    
    // 6. 创建工具页面（简化版本）
    const pagesDir = 'pages/tools';
    if (!fs.existsSync(pagesDir)) {
        fs.mkdirSync(pagesDir, { recursive: true });
        console.log(`📁 创建页面目录: ${pagesDir}`);
    }
    
    // 只为前3个新工具创建示例页面
    const toolsToCreate = newTools.slice(0, 3);
    
    for (const tool of toolsToCreate) {
        const pagePath = path.join(pagesDir, `${tool.id}.html`);
        
        const pageContent = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${tool.name} - AI.link.cn</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
        .info { background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .url { color: #0066cc; text-decoration: none; }
        .url:hover { text-decoration: underline; }
        .back { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>${tool.name}</h1>
        
        <div class="info">
            <p><strong>描述:</strong> ${tool.description}</p>
            <p><strong>类别:</strong> ${tool.category}</p>
            <p><strong>网址:</strong> <a href="${tool.url}" class="url" target="_blank">${tool.url}</a></p>
            <p><strong>定价:</strong> ${tool.pricing}</p>
            <p><strong>评分:</strong> ${tool.rating}/5.0</p>
        </div>
        
        <h2>优点</h2>
        <ul>
            ${tool.pros.map(pro => `<li>${pro}</li>`).join('\n            ')}
        </ul>
        
        <h2>缺点</h2>
        <ul>
            ${tool.cons.map(con => `<li>${con}</li>`).join('\n            ')}
        </ul>
        
        <p><em>页面自动生成于 ${new Date().toLocaleString('zh-CN')}</em></p>
        
        <a href="/pages/tools/index.html" class="back">返回工具列表</a>
    </div>
</body>
</html>`;
        
        try {
            fs.writeFileSync(pagePath, pageContent, 'utf8');
            console.log(`   📄 创建页面: ${tool.id}.html`);
        } catch (error) {
            console.log(`   ❌ 创建页面失败 (${tool.name}): ${error.message}`);
        }
    }
    
    // 7. 更新工具列表页面
    const indexPagePath = path.join(pagesDir, 'index.html');
    const indexContent = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI工具大全 - AI.link.cn</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { color: #333; text-align: center; }
        .stats { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
        .tool-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .tool-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .tool-name { color: #0066cc; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
        .tool-desc { color: #666; margin-bottom: 15px; font-size: 14px; }
        .tool-cat { display: inline-block; background: #4CAF50; color: white; padding: 3px 10px; border-radius: 15px; font-size: 12px; }
        .update-info { text-align: center; margin-top: 30px; color: #888; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI工具大全</h1>
        
        <div class="stats">
            <h2>当前收录: ${database.tools.length} 个AI工具</h2>
            <p>最后更新: ${new Date().toLocaleString('zh-CN')}</p>
        </div>
        
        <div class="tool-grid">
            ${database.tools.map(tool => `
            <div class="tool-card">
                <div class="tool-name">${tool.name}</div>
                <div class="tool-desc">${tool.description.substring(0, 100)}...</div>
                <div>
                    <span class="tool-cat">${tool.category}</span>
                    <span style="float: right; color: #ff9800;">⭐ ${tool.rating}</span>
                </div>
                <a href="${tool.reviewUrl}" style="display: block; margin-top: 10px; color: #0066cc; text-decoration: none;">查看详情 →</a>
            </div>
            `).join('\n            ')}
        </div>
        
        <div class="update-info">
            <p>页面自动生成，每日更新 | AI.link.cn - 专业的AI工具评测和推荐平台</p>
        </div>
    </div>
</body>
</html>`;
    
    try {
        fs.writeFileSync(indexPagePath, indexContent, 'utf8');
        console.log(`✅ 更新工具列表页面: ${indexPagePath}`);
    } catch (error) {
        console.log(`❌ 更新工具列表页面失败: ${error.message}`);
    }
    
    // 8. 生成更新日志
    const logDir = 'logs';
    if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
    }
    
    const logFile = path.join(logDir, `manual_update_${new Date().toISOString().replace(/[:.]/g, '').slice(0, 15)}.log`);
    const logContent = `[${new Date().toISOString()}] 手动更新完成
新增工具: ${newTools.length}
工具总数: ${database.tools.length}
新增的工具: ${newTools.map(t => t.name).join(', ')}
数据库文件: ${dbPath}
工具列表页面: ${indexPagePath}
`;
    
    fs.writeFileSync(logFile, logContent, 'utf8');
    console.log(`📝 更新日志已保存: ${logFile}`);
    
    console.log('\n🎉 更新完成！');
    console.log(`📊 统计信息:`);
    console.log(`   - 数据库工具总数: ${database.tools.length}`);
    console.log(`   - 本次新增工具: ${newTools.length}`);
    console.log(`   - 创建页面: ${toolsToCreate.length} 个`);
    console.log(`   - 工具列表页面已更新`);
    
    console.log('\n🚀 下一步建议:');
    console.log('1. 提交更改到GitHub');
    console.log('2. 推送到Vercel部署');
    console.log('3. 检查网站更新效果');
}

// 运行更新
updateTools().catch(console.error);