// 测试AI工具发现脚本
const axios = require('axios');
const fs = require('fs');

async function testDiscovery() {
    console.log('=== 测试AI工具发现系统 ===\n');
    
    // 测试GitHub搜索AI工具
    try {
        console.log('1. 测试GitHub API搜索AI工具...');
        const response = await axios.get('https://api.github.com/search/repositories', {
            params: {
                q: 'ai tool',
                sort: 'stars',
                order: 'desc',
                per_page: 5
            },
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/vnd.github.v3+json'
            }
        });
        
        console.log(`✅ GitHub API请求成功: ${response.data.items.length} 个仓库`);
        response.data.items.forEach((item, i) => {
            console.log(`   ${i+1}. ${item.name} - ${item.description?.substring(0, 100)}... (⭐ ${item.stargazers_count})`);
        });
    } catch (error) {
        console.log(`❌ GitHub API请求失败: ${error.message}`);
    }
    
    console.log('\n2. 测试Futurepedia...');
    try {
        // 简单测试Futurepedia页面是否可访问
        const response = await axios.get('https://www.futurepedia.io/', {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        });
        
        console.log(`✅ Futurepedia请求成功: 状态码 ${response.status}, 页面大小 ${response.data.length} 字符`);
        
        // 检查是否包含AI工具相关内容
        const hasAITools = response.data.includes('AI tools') || response.data.includes('artificial intelligence');
        console.log(`   ${hasAITools ? '✅' : '⚠️'} 页面包含AI工具相关内容: ${hasAITools ? '是' : '可能不是AI工具页面'}`);
    } catch (error) {
        console.log(`❌ Futurepedia请求失败: ${error.message}`);
    }
    
    console.log('\n3. 检查当前数据库状态...');
    try {
        const dbPath = 'ai_tools_database.json';
        if (fs.existsSync(dbPath)) {
            const data = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
            const tools = data.tools || [];
            console.log(`✅ 数据库存在，包含 ${tools.length} 个工具`);
            
            // 按添加日期统计
            const today = new Date().toISOString().split('T')[0];
            const recentTools = tools.filter(t => t.addedDate === today);
            console.log(`   今日添加的工具: ${recentTools.length} 个`);
            
            if (recentTools.length > 0) {
                recentTools.forEach((tool, i) => {
                    console.log(`     ${i+1}. ${tool.name} - ${tool.category}`);
                });
            } else {
                console.log('   今日没有添加新工具');
            }
        } else {
            console.log('❌ 数据库文件不存在');
        }
    } catch (error) {
        console.log(`❌ 读取数据库失败: ${error.message}`);
    }
    
    console.log('\n4. 检查自动化脚本输出目录...');
    const outputDirs = [
        'discovered_tools',
        'discovered_tools/processed',
        'logs'
    ];
    
    outputDirs.forEach(dir => {
        const exists = fs.existsSync(dir);
        console.log(`   ${exists ? '✅' : '❌'} ${dir}: ${exists ? '存在' : '不存在'}`);
    });
    
    console.log('\n=== 测试完成 ===');
}

// 运行测试
testDiscovery().catch(console.error);