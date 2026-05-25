// 检查网站更新状态的脚本
const axios = require('axios');

async function checkWebsite() {
    console.log('🌐 检查网站更新状态...\n');
    
    const urls = [
        'https://ai.link.cn/',
        'https://ai.link.cn/pages/tools/'
    ];
    
    for (const url of urls) {
        try {
            console.log(`📡 检查: ${url}`);
            const response = await axios.get(url, {
                timeout: 10000,
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            });
            
            const html = response.data;
            
            // 检查工具数量显示
            const countPatterns = [
                /收录(\d+)个/,
                /收录了(\d+)个/,
                /收录 (\d+) 个/,
                /(\d+)个.*?AI工具/,
                /(\d+).*?个工具/
            ];
            
            let foundCount = null;
            for (const pattern of countPatterns) {
                const match = html.match(pattern);
                if (match && match[1]) {
                    foundCount = match[1];
                    break;
                }
            }
            
            // 检查meta描述
            const metaDescMatch = html.match(/<meta[^>]*name="description"[^>]*content="([^"]*)"[^>]*>/i);
            const metaDesc = metaDescMatch ? metaDescMatch[1] : '';
            
            // 检查缓存头
            const cacheHeaders = {
                'age': response.headers['age'],
                'cache-control': response.headers['cache-control'],
                'x-vercel-cache': response.headers['x-vercel-cache']
            };
            
            console.log(`   ✅ 状态码: ${response.status}`);
            console.log(`   📊 页面大小: ${html.length} 字符`);
            
            if (foundCount) {
                console.log(`   🔢 检测到工具数量: ${foundCount} 个`);
                
                if (parseInt(foundCount) >= 65) {
                    console.log(`   🎉 成功: 网站显示 ${foundCount} 个工具 (目标: 65个)`);
                } else {
                    console.log(`   ⚠️  注意: 网站显示 ${foundCount} 个工具 (但数据库有65个)`);
                }
            } else {
                console.log(`   ❓ 未检测到明确的工具数量显示`);
            }
            
            if (metaDesc) {
                console.log(`   📝 Meta描述: ${metaDesc.substring(0, 80)}...`);
                
                if (metaDesc.includes('65个') || metaDesc.includes('65 个')) {
                    console.log(`   ✅ Meta描述已更新为65个工具`);
                } else if (metaDesc.includes('11个') || metaDesc.includes('11 个')) {
                    console.log(`   ❌ Meta描述还是11个工具 (需要更新)`);
                }
            }
            
            console.log(`   🕒 缓存状态: ${cacheHeaders['x-vercel-cache'] || '未知'}`);
            if (cacheHeaders['age']) {
                const ageHours = Math.floor(cacheHeaders['age'] / 3600);
                console.log(`   ⏰ 缓存年龄: ${cacheHeaders['age']}秒 (约${ageHours}小时)`);
            }
            
            console.log('');
            
        } catch (error) {
            console.log(`   ❌ 检查失败: ${error.message}\n`);
        }
    }
    
    console.log('📋 建议:');
    console.log('1. 如果网站还是显示11个工具，可能需要:');
    console.log('   - 等待Vercel部署完成 (通常需要1-5分钟)');
    console.log('   - 手动刷新网站缓存 (Ctrl+F5或Cmd+Shift+R)');
    console.log('   - 在Vercel控制台手动触发重新部署');
    console.log('2. 如果显示65个工具，问题已解决！');
    console.log('3. 检查 https://vercel.com 查看部署状态');
}

checkWebsite().catch(console.error);