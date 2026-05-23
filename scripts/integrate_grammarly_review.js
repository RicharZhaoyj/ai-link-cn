#!/usr/bin/env node
/**
 * Grammarly评测集成脚本
 * 将评测内容集成到网站页面
 */

const fs = require('fs').promises;
const path = require('path');

async function integrateGrammarlyReview() {
  console.log('🚀 开始Grammarly评测集成工作');
  console.log('='.repeat(60));
  
  try {
    // 1. 读取评测内容
    const reviewPath = path.join(__dirname, '..', 'content', 'tools', 'grammarly_ai_review_20260519.md');
    const reviewContent = await fs.readFile(reviewPath, 'utf-8');
    
    console.log(`📄 读取评测文件: ${reviewPath}`);
    console.log(`📊 评测内容大小: ${reviewContent.length} 字符`);
    
    // 2. 解析评测内容
    const sections = parseReviewContent(reviewContent);
    console.log(`📋 解析出 ${sections.length} 个主要章节`);
    
    // 3. 读取现有HTML模板
    const htmlPath = path.join(__dirname, '..', 'pages', 'tools', 'grammarly.html');
    let htmlContent = await fs.readFile(htmlPath, 'utf-8');
    console.log(`📄 读取HTML模板: ${htmlPath}`);
    
    // 4. 集成评测内容
    const updatedHtml = integrateIntoHtml(htmlContent, sections);
    
    // 5. 保存更新后的页面
    await fs.writeFile(htmlPath, updatedHtml, 'utf-8');
    console.log(`💾 已更新Grammarly页面: ${htmlPath}`);
    
    // 6. 创建备份
    const backupPath = htmlPath + '.backup.' + Date.now();
    await fs.writeFile(backupPath, htmlContent, 'utf-8');
    console.log(`📦 创建备份: ${backupPath}`);
    
    console.log('\n✅ Grammarly评测集成完成！');
    console.log('💡 建议下一步:');
    console.log('1. 检查页面显示效果');
    console.log('2. 更新工具列表页面的链接');
    console.log('3. 提交到GitHub并部署到Vercel');
    
    return {
      success: true,
      sections: sections.length,
      backup: backupPath
    };
    
  } catch (error) {
    console.error('❌ 集成失败:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 解析评测内容
 */
function parseReviewContent(content) {
  const sections = [];
  const lines = content.split('\n');
  
  let currentSection = null;
  
  for (const line of lines) {
    // 检测标题
    if (line.startsWith('# ')) {
      if (currentSection) sections.push(currentSection);
      currentSection = {
        title: line.replace('# ', '').trim(),
        content: '',
        level: 1
      };
    } else if (line.startsWith('## ')) {
      if (currentSection) sections.push(currentSection);
      currentSection = {
        title: line.replace('## ', '').trim(),
        content: '',
        level: 2
      };
    } else if (line.startsWith('### ')) {
      if (currentSection) sections.push(currentSection);
      currentSection = {
        title: line.replace('### ', '').trim(),
        content: '',
        level: 3
      };
    } else if (currentSection) {
      // 添加内容到当前章节
      if (line.trim() || currentSection.content) {
        currentSection.content += line + '\n';
      }
    }
  }
  
  // 添加最后一个章节
  if (currentSection) {
    sections.push(currentSection);
  }
  
  return sections;
}

/**
 * 集成到HTML
 */
function integrateIntoHtml(htmlContent, sections) {
  // 找到插入点（在现有内容之后）
  const bodyEndIndex = htmlContent.indexOf('</body>');
  if (bodyEndIndex === -1) {
    throw new Error('找不到</body>标签');
  }
  
  // 构建评测内容HTML
  let reviewHtml = '\n\n<!-- ==================== -->\n';
  reviewHtml += '<!-- Grammarly AI评测内容 -->\n';
  reviewHtml += '<!-- ==================== -->\n\n';
  
  reviewHtml += '<main class="container">\n';
  reviewHtml += '  <article>\n';
  
  for (const section of sections) {
    if (section.title && section.content.trim()) {
      // 根据标题级别生成HTML
      const tagName = `h${section.level}`;
      reviewHtml += `    <${tagName}>${section.title}</${tagName}>\n`;
      
      // 处理内容
      const processedContent = processContent(section.content);
      reviewHtml += `    <div class="section-content">\n${processedContent}\n    </div>\n\n`;
    }
  }
  
  reviewHtml += '  </article>\n';
  reviewHtml += '</main>\n\n';
  
  // 插入到</body>之前
  const updatedHtml = htmlContent.slice(0, bodyEndIndex) + reviewHtml + htmlContent.slice(bodyEndIndex);
  
  return updatedHtml;
}

/**
 * 处理内容格式
 */
function processContent(content) {
  let processed = content;
  
  // 处理列表
  processed = processed.replace(/^- (.*)/gm, '      <li>$1</li>');
  
  // 处理加粗文本
  processed = processed.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  
  // 处理链接
  processed = processed.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  
  // 处理代码块
  processed = processed.replace(/`(.*?)`/g, '<code>$1</code>');
  
  // 将列表项包装在<ul>中
  const lines = processed.split('\n');
  let inList = false;
  let resultLines = [];
  
  for (let line of lines) {
    if (line.includes('<li>')) {
      if (!inList) {
        resultLines.push('      <ul>');
        inList = true;
      }
      resultLines.push(line);
    } else {
      if (inList) {
        resultLines.push('      </ul>');
        inList = false;
      }
      resultLines.push(line);
    }
  }
  
  if (inList) {
    resultLines.push('      </ul>');
  }
  
  return resultLines.join('\n');
}

// 命令行接口
if (require.main === module) {
  integrateGrammarlyReview().then(result => {
    if (result.success) {
      console.log('\n🎉 Grammarly评测集成成功！');
      process.exit(0);
    } else {
      console.error('\n❌ 集成失败');
      process.exit(1);
    }
  });
}

module.exports = integrateGrammarlyReview;