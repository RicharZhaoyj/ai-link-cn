#!/usr/bin/env node

/**
 * 简单的开发服务器
 * 用于本地测试和Vercel部署
 */

const http = require('http');
const fs = require('fs').promises;
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3000;

// MIME类型映射
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain',
  '.md': 'text/markdown'
};

// API处理器
const apiHandlers = {
  '/api': (req, res) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      name: 'AI.link.cn API',
      version: '1.0.0',
      description: 'AI工具推荐平台API',
      endpoints: ['/api', '/api/tools', '/api/affiliate'],
      status: 'active'
    }));
  },
  
  '/api/tools': (req, res) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      success: true,
      data: {
        writing: [
          { id: 'chatgpt', name: 'ChatGPT', description: 'OpenAI的对话式AI', category: '写作', affiliate: true },
          { id: 'jasper', name: 'Jasper AI', description: '专业的AI写作工具', category: '写作', affiliate: true },
          { id: 'grammarly', name: 'Grammarly', description: 'AI语法检查工具', category: '写作', affiliate: true }
        ],
        image: [
          { id: 'midjourney', name: 'Midjourney', description: 'AI图像生成', category: '图像', affiliate: true },
          { id: 'dalle', name: 'DALL-E 3', description: 'OpenAI图像生成', category: '图像', affiliate: false },
          { id: 'canva', name: 'Canva AI', description: '设计工具+AI', category: '图像', affiliate: true }
        ]
      },
      timestamp: new Date().toISOString()
    }));
  },
  
  '/api/affiliate': (req, res) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      success: true,
      data: [
        { id: 'chatgpt', name: 'ChatGPT', url: 'https://chat.openai.com/', affiliateUrl: 'https://chat.openai.com/?ref=ailink' },
        { id: 'midjourney', name: 'Midjourney', url: 'https://www.midjourney.com/', affiliateUrl: 'https://www.midjourney.com/?ref=ailink' },
        { id: 'grammarly', name: 'Grammarly', url: 'https://www.grammarly.com/', affiliateUrl: 'https://www.grammarly.com/?ref=ailink' }
      ],
      timestamp: new Date().toISOString()
    }));
  }
};

// 静态文件服务
async function serveStaticFile(req, res) {
  try {
    const parsedUrl = url.parse(req.url);
    let filePath = parsedUrl.pathname;
    
    // 默认首页
    if (filePath === '/') {
      filePath = '/index.html';
    }
    
    // 安全路径检查
    if (filePath.includes('..')) {
      res.writeHead(403);
      res.end('Forbidden');
      return;
    }
    
    const fullPath = path.join(__dirname, '..', filePath);
    
    // 检查文件是否存在
    try {
      await fs.access(fullPath);
    } catch {
      // 文件不存在，返回404
      res.writeHead(404);
      res.end('File not found');
      return;
    }
    
    // 读取文件
    const data = await fs.readFile(fullPath);
    
    // 获取MIME类型
    const ext = path.extname(fullPath);
    const mimeType = MIME_TYPES[ext] || 'application/octet-stream';
    
    // 设置响应头
    res.writeHead(200, {
      'Content-Type': mimeType,
      'Cache-Control': 'public, max-age=3600'
    });
    
    res.end(data);
    
  } catch (error) {
    console.error('Error serving file:', error);
    res.writeHead(500);
    res.end('Internal server error');
  }
}

// 请求处理器
async function requestHandler(req, res) {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  
  // 处理API请求
  if (req.url.startsWith('/api')) {
    const handler = apiHandlers[req.url] || apiHandlers['/api'];
    handler(req, res);
    return;
  }
  
  // 处理静态文件
  await serveStaticFile(req, res);
}

// 创建服务器
const server = http.createServer(requestHandler);

// 启动服务器
server.listen(PORT, () => {
  console.log(`
  ===========================================
  AI.link.cn 开发服务器已启动
  ===========================================
  
  本地访问: http://localhost:${PORT}
  网络访问: http://[你的IP]:${PORT}
  
  可用端点:
  - /              : 主页面
  - /api           : API信息
  - /api/tools     : AI工具列表
  - /api/affiliate : Affiliate链接
  
  项目状态:
  - ✅ GitHub仓库已更新
  - ✅ 风险转移完成 (投资分析 → AI工具推荐)
  - ✅ 部署配置就绪
  - 🚀 准备上线!
  
  ===========================================
  `);
});

// 优雅关闭
process.on('SIGINT', () => {
  console.log('\n正在关闭服务器...');
  server.close(() => {
    console.log('服务器已关闭');
    process.exit(0);
  });
});

process.on('SIGTERM', () => {
  console.log('\n收到终止信号，正在关闭服务器...');
  server.close(() => {
    console.log('服务器已关闭');
    process.exit(0);
  });
});