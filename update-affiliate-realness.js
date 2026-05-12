#!/usr/bin/env node
/**
 * 更新Affiliate链接的真实性说明
 */

const fs = require('fs').promises;
const path = require('path');

async function updateFile(filePath) {
  try {
    let content = await fs.readFile(filePath, 'utf-8');
    
    // 替换ChatGPT链接和说明
    content = content.replace(
      /affiliateUrl: 'https:\/\/chat\.openai\.com\/\?ref=ailink',/,
      `affiliateUrl: 'https://chat.openai.com/',
        notes: '⚠️ OpenAI目前没有官方Affiliate项目。这只是官网链接，不产生佣金。'`
    );
    
    // 替换Midjourney链接和说明
    content = content.replace(
      /affiliateUrl: 'https:\/\/www\.midjourney\.com\/\?ref=ailink',/,
      `affiliateUrl: 'https://www.midjourney.com/',
        notes: '⚠️ Midjourney目前没有官方Affiliate项目。这只是官网链接，不产生佣金。考虑推广Canva AI等有Affiliate的替代工具。'`
    );
    
    // 更新Notion AI说明
    content = content.replace(
      /notes: '通过ShareASale平台'/,
      `notes: '⚠️ 需要通过ShareASale平台申请真实的Affiliate链接。这只是referral参数链接，申请批准后需要更新为真实的Affiliate链接。'`
    );
    
    // 更新Grammarly说明
    content = content.replace(
      /notes: '通过Impact平台'/,
      `notes: '✅ 有官方Affiliate项目。需要通过Impact.com申请：https://impact.com/publishers/grammarly-affiliate-program/ 申请批准后更新链接。'`
    );
    
    // 更新Jasper AI说明
    content = content.replace(
      /notes: '高转化率'/,
      `notes: '✅ 有官方Affiliate项目。申请地址：https://www.jasper.ai/affiliates 申请批准后更新链接。'`
    );
    
    // 添加实际可申请的Affiliate工具
    const newTools = `
      // 实际可申请的Affiliate工具（添加在默认链接后面）
      {
        id: 'canva',
        name: 'Canva AI',
        toolName: 'Canva',
        type: 'subscription',
        url: 'https://www.canva.com/',
        affiliateUrl: 'https://www.canva.com/?ref=YOUR_AFFILIATE_ID',
        platform: 'Canva',
        commission: '按销售计算',
        commissionType: 'one_time',
        status: 'pending',
        lastChecked: new Date().toISOString(),
        notes: '✅ 有官方Affiliate项目。申请地址：https://www.canva.com/affiliates/'
      },
      {
        id: 'convertkit',
        name: 'ConvertKit',
        toolName: 'ConvertKit',
        type: 'subscription',
        url: 'https://convertkit.com/',
        affiliateUrl: 'https://convertkit.com/?via=YOUR_AFFILIATE_ID',
        platform: 'ConvertKit',
        commission: '30%月费',
        commissionType: 'percentage_recurring',
        status: 'pending',
        lastChecked: new Date().toISOString(),
        notes: '✅ 有官方Affiliate项目。申请地址：https://convertkit.com/affiliates 容易批准'
      },
      {
        id: 'hostinger',
        name: 'Hostinger',
        toolName: 'Hostinger',
        type: 'one_time',
        url: 'https://www.hostinger.com/',
        affiliateUrl: 'https://www.hostinger.com/?ref=YOUR_AFFILIATE_ID',
        platform: 'Hostinger',
        commission: '60-100%首次购买',
        commissionType: 'percentage_one_time',
        status: 'pending',
        lastChecked: new Date().toISOString(),
        notes: '✅ 有官方Affiliate项目。申请地址：https://www.hostinger.com/affiliates 高佣金'
      }
    `;
    
    // 在最后一个链接后面添加新工具
    const insertPoint = content.lastIndexOf('}') + 1;
    content = content.slice(0, insertPoint) + ',' + newTools + content.slice(insertPoint);
    
    await fs.writeFile(filePath, content, 'utf-8');
    console.log(`✅ 已更新: ${filePath}`);
    
  } catch (error) {
    console.log(`❌ 更新失败 ${filePath}: ${error.message}`);
  }
}

async function main() {
  console.log('🔧 更新Affiliate链接真实性说明...\n');
  
  await updateFile('src/affiliate_tracker.js');
  
  console.log('\n✅ 更新完成！');
  console.log('\n📋 主要更新内容:');
  console.log('1. ✅ 标记了真实的Affiliate项目 (Canva, ConvertKit, Hostinger)');
  console.log('2. ⚠️ 标注了虚假的"Affiliate链接" (ChatGPT, Midjourney)');
  console.log('3. 🔗 提供了真实的申请链接');
  console.log('4. 💰 明确了佣金计算方式');
  
  console.log('\n🚀 立即行动:');
  console.log('1. 访问提供的真实Affiliate申请链接');
  console.log('2. 申请批准后更新affiliateUrl字段');
  console.log('3. 删除虚假的"Affiliate链接"说明');
  console.log('4. 开始推广真实的Affiliate项目');
  
  console.log('\n💡 提示: 虚假的Affiliate链接不仅不产生佣金，还可能违反平台规则。');
  console.log('专注于推广有真实Affiliate项目的工具，建立可持续的收入。');
}

if (require.main === module) {
  main().catch(console.error);
}