// 静态文件服务器配置
// 用于在Vercel上正确处理静态文件

const fs = require('fs');
const path = require('path');

// 检查文件是否存在
function fileExists(filePath) {
  try {
    return fs.existsSync(filePath) && fs.statSync(filePath).isFile();
  } catch {
    return false;
  }
}

// 处理页面请求
function handlePageRequest(req, res) {
  const url = req.url;
  
  // 映射常用页面
  const pageMap = {
    '/': 'index.html',
    '/tools': 'pages/tools/index.html',
    '/affiliate-guide': 'pages/affiliate-guide.html',
    '/navigation': 'pages/navigation.html',
    '/chatgpt': 'pages/tools/chatgpt.html',
    '/midjourney': 'pages/tools/midjourney.html',
    '/grammarly': 'pages/tools/grammarly.html',
    '/notion-ai': 'pages/tools/notion_ai.html',
    '/canva': 'pages/tools/canva.html',
    '/jasper': 'pages/tools/jasper.html'
  };
  
  // 如果是映射的路径
  if (pageMap[url]) {
    const filePath = path.join(__dirname, pageMap[url]);
    if (fileExists(filePath)) {
      const content = fs.readFileSync(filePath, 'utf-8');
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(content);
      return true;
    }
  }
  
  // 尝试直接访问文件
  const cleanUrl = url.replace(/\.\./g, ''); // 防止目录遍历攻击
  
  // 检查是否有对应的文件
  const possiblePaths = [
    cleanUrl,
    cleanUrl + '.html',
    cleanUrl + '/index.html',
    '/pages' + cleanUrl,
    '/pages' + cleanUrl + '.html',
    '/pages' + cleanUrl + '/index.html'
  ];
  
  for (const possiblePath of possiblePaths) {
    const fullPath = path.join(__dirname, possiblePath);
    if (fileExists(fullPath)) {
      const ext = path.extname(fullPath).toLowerCase();
      const contentType = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml'
      }[ext] || 'text/plain';
      
      const content = fs.readFileSync(fullPath);
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
      return true;
    }
  }
  
  return false;
}

// 为Vercel函数导出处理程序
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { handlePageRequest, fileExists };
}

console.log('✅ 静态文件服务器配置已加载');