// 深度检查网站所有页面
const axios = require('axios');

async function deepCheck() {
    console.log('🔍 深度检查网站工具显示问题\n');
    
    // 可能显示工具数量的页面
    const pages = [
        { url: 'https://ai.link.cn/', name: '首页' },
        { url: 'https://ai.link.cn/index_seo_optimized.html', name: 'SEO优化首页' },
        { url: 'https://ai.link.cn/index_rich.html', name: '丰富版首页' },
        { url: 'https://ai.link.cn/pages/tools/', name: '工具列表页' }
    ];
    
    for (const page of pages) {
        try {
            console.log(`📄 检查: ${page.name} (${page.url})`);
            const response = await axios.get(page.url, {
                timeout: 10000,
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Cache-Control': 'no-cache'
                }
            });
            
            const html = response.data;
            
            // 检查所有可能显示数字的地方
            const patterns = [
                { regex: /收录(\d+)个/, desc: '收录X个' },
                { regex: /收录了(\d+)个/, desc: '收录了X个' },
                { regex: /收录 (\d+) 个/, desc: '收录 X 个' },
                { regex: /(\d+)个.*?AI工具/, desc: 'X个AI工具' },
                { regex: /(\d+).*?个工具/, desc: 'X个工具' },
                { regex: /收录工具: (\d+)个/, desc: '收录工具: X个' },
                { regex: /<span[^>]*class="[^"]*stat-value[^"]*"[^>]*>(\d+)个<\/span>/, desc: '统计值: X个' }
            ];
            
            const foundNumbers = [];
            for (const pattern of patterns) {
                const matches = html.match(new RegExp(pattern.regex, 'g'));
                if (matches) {
                    for (const match of matches) {
                        const numMatch = match.match(/(\d+)/);
                        if (numMatch) {
                            foundNumbers.push({
                                number: parseInt(numMatch[1]),
                                text: match.substring(0, 50) + '...',
                                pattern: pattern.desc
                            });
                        }
                    }
                }
            }
            
            if (foundNumbers.length > 0) {
                console.log(`   📊 发现的数字显示:`);
                foundNumbers.forEach(item => {
                    const status = item.number === 65 ? '✅' : item.number === 11 ? '❌' : '⚠️';
                    console.log(`     ${status} ${item.pattern}: ${item.number}个 - "${item.text}"`);
                });
                
                // 检查是否有11个
                const has11 = foundNumbers.some(item => item.number === 11);
                if (has11) {
                    console.log(`   🚨 发现11个工具显示! 需要修复`);
                } else if (foundNumbers.some(item => item.number === 65)) {
                    console.log(`   ✅ 页面显示65个工具 - 正确`);
                }
            } else {
                console.log(`   ℹ️  未检测到工具数量显示`);
            }
            
            // 检查缓存状态
            const cacheAge = response.headers['age'];
            if (cacheAge) {
                const ageMinutes = Math.floor(cacheAge / 60);
                console.log(`   🕒 缓存年龄: ${ageMinutes}分钟`);
            }
            
            console.log('');
            
        } catch (error) {
            if (error.response && error.response.status === 404) {
                console.log(`   ⚠️  页面不存在 (404)`);
            } else {
                console.log(`   ❌ 检查失败: ${error.message}`);
            }
            console.log('');
        }
    }
    
    console.log('📋 问题诊断:');
    console.log('1. 如果任何页面显示11个工具:');
    console.log('   - Vercel可能还在使用旧缓存');
    console.log('   - 需要等待部署完成 (通常1-5分钟)');
    console.log('   - 或手动清除Vercel缓存');
    console.log('');
    console.log('2. 如果所有页面都显示65个工具:');
    console.log('   ✅ 问题已完全解决！');
    console.log('');
    console.log('3. 如果页面不存在 (404):');
    console.log('   - 该文件可能不是网站实际使用的');
    console.log('   - 可以忽略该页面');
}

deepCheck().catch(console.error);