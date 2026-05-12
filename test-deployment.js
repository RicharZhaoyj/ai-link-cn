#!/usr/bin/env node

/**
 * 部署测试脚本
 * 验证所有功能和配置
 */

const fs = require('fs').promises;
const path = require('path');
const http = require('http');

async function runTests() {
  console.log('🚀 AI.link.cn 部署测试\n');
  
  const tests = [];
  const results = { passed: 0, failed: 0 };
  
  // 测试1: 检查核心文件
  tests.push(async () => {
    console.log('📁 测试1: 检查核心文件');
    const files = [
      'package.json',
      'index.html',
      'README.md',
      'vercel.json',
      'CNAME',
      'config/affiliate_links.json',
      'src/ai_tools_scraper.js'
    ];
    
    for (const file of files) {
      try {
        await fs.access(file);
        console.log(`  ✅ ${file}`);
      } catch {
        console.log(`  ❌ ${file} 不存在`);
        return false;
      }
    }
    return true;
  });
  
  // 测试2: 验证package.json
  tests.push(async () => {
    console.log('\n📦 测试2: 验证package.json');
    try {
      const pkg = JSON.parse(await fs.readFile('package.json', 'utf8'));
      
      console.log(`  项目名称: ${pkg.name}`);
      console.log(`  版本: ${pkg.version}`);
      console.log(`  描述: ${pkg.description.substring(0, 60)}...`);
      
      if (!pkg.scripts || !pkg.scripts.dev) {
        console.log('  ❌ 缺少dev脚本');
        return false;
      }
      
      console.log('  ✅ package.json 有效');
      return true;
    } catch (error) {
      console.log(`  ❌ 读取package.json失败: ${error.message}`);
      return false;
    }
  });
  
  // 测试3: 验证配置文件
  tests.push(async () => {
    console.log('\n⚙️ 测试3: 验证配置文件');
    
    const configs = [
      'config/affiliate_links.json',
      'config/tools_list.json',
      'config/seo_keywords.json'
    ];
    
    for (const configFile of configs) {
      try {
        const content = await fs.readFile(configFile, 'utf8');
        const data = JSON.parse(content);
        
        let isValid = false;
        if (configFile.includes('affiliate')) {
          isValid = Array.isArray(data.links) && data.links.length > 0;
          console.log(`  ${isValid ? '✅' : '❌'} ${path.basename(configFile)}: ${data.links?.length || 0} 个Affiliate链接`);
        } else if (configFile.includes('tools')) {
          isValid = data.categories && Object.keys(data.categories).length > 0;
          console.log(`  ${isValid ? '✅' : '❌'} ${path.basename(configFile)}: ${Object.keys(data.categories || {}).length} 个工具类别`);
        } else if (configFile.includes('seo')) {
          isValid = data.primary_keywords && data.primary_keywords.length > 0;
          console.log(`  ${isValid ? '✅' : '❌'} ${path.basename(configFile)}: ${data.primary_keywords?.length || 0} 个主要关键词`);
        }
        
        if (!isValid) return false;
      } catch (error) {
        console.log(`  ❌ ${path.basename(configFile)}: ${error.message}`);
        return false;
      }
    }
    
    return true;
  });
  
  // 测试4: 验证源代码
  tests.push(async () => {
    console.log('\n💻 测试4: 验证源代码');
    
    const sourceFiles = [
      'src/ai_tools_scraper.js',
      'src/affiliate_tracker.js',
      'src/content_generator.js',
      'scripts/dev-server.js'
    ];
    
    for (const sourceFile of sourceFiles) {
      try {
        const stats = await fs.stat(sourceFile);
        const content = await fs.readFile(sourceFile, 'utf8');
        
        console.log(`  ${content.length > 100 ? '✅' : '⚠️'} ${path.basename(sourceFile)}: ${stats.size} 字节, ${content.split('\n').length} 行`);
        
        if (content.length < 100) {
          console.log(`    警告: 文件可能过小`);
        }
      } catch (error) {
        console.log(`  ❌ ${path.basename(sourceFile)}: ${error.message}`);
        return false;
      }
    }
    
    return true;
  });
  
  // 测试5: 启动本地服务器
  tests.push(async () => {
    console.log('\n🌐 测试5: 本地服务器测试');
    
    return new Promise((resolve) => {
      const server = require('./scripts/dev-server.js');
      
      // 给服务器一点时间启动
      setTimeout(async () => {
        try {
          // 测试HTTP请求
          const options = {
            hostname: 'localhost',
            port: 3000,
            path: '/',
            method: 'GET',
            timeout: 5000
          };
          
          const req = http.request(options, (res) => {
            console.log(`  状态码: ${res.statusCode}`);
            
            if (res.statusCode === 200) {
              console.log('  ✅ 本地服务器响应正常');
              resolve(true);
            } else {
              console.log(`  ❌ 服务器返回错误状态: ${res.statusCode}`);
              resolve(false);
            }
          });
          
          req.on('error', (error) => {
            console.log(`  ❌ 服务器连接失败: ${error.message}`);
            console.log('  提示: 运行 "npm run dev" 启动服务器');
            resolve(false);
          });
          
          req.on('timeout', () => {
            console.log('  ❌ 服务器连接超时');
            resolve(false);
          });
          
          req.end();
          
        } catch (error) {
          console.log(`  ❌ 服务器测试失败: ${error.message}`);
          resolve(false);
        }
      }, 2000);
    });
  });
  
  // 运行所有测试
  for (let i = 0; i < tests.length; i++) {
    try {
      const passed = await tests[i]();
      if (passed) {
        results.passed++;
      } else {
        results.failed++;
      }
    } catch (error) {
      console.log(`  ❌ 测试${i + 1}执行错误: ${error.message}`);
      results.failed++;
    }
  }
  
  // 显示结果
  console.log('\n' + '='*60);
  console.log('📊 测试结果汇总');
  console.log('='*60);
  console.log(`✅ 通过的测试: ${results.passed}`);
  console.log(`❌ 失败的测试: ${results.failed}`);
  console.log(`📈 成功率: ${((results.passed / tests.length) * 100).toFixed(1)}%`);
  
  if (results.failed === 0) {
    console.log('\n🎉 所有测试通过! 项目可以部署到Vercel。');
    console.log('\n下一步操作:');
    console.log('1. 访问 GitHub: https://github.com/RicharZhaoyj/ai-link-cn');
    console.log('2. 连接 Vercel: https://vercel.com/new');
    console.log('3. 导入 ai-link-cn 仓库');
    console.log('4. 部署到 https://ai.link.cn');
  } else {
    console.log('\n⚠️ 有些测试失败，需要修复后才能部署。');
    console.log('\n常见问题:');
    console.log('1. 缺少文件: 检查是否所有文件都已提交');
    console.log('2. 配置错误: 检查JSON文件格式');
    console.log('3. 依赖问题: 运行 npm install');
  }
  
  console.log('\n' + '='*60);
  process.exit(results.failed === 0 ? 0 : 1);
}

// 运行测试
if (require.main === module) {
  runTests().catch(error => {
    console.error('测试运行失败:', error);
    process.exit(1);
  });
}

module.exports = { runTests };