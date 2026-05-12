// API根端点
export default function handler(req, res) {
  res.status(200).json({
    name: 'AI.link.cn API',
    version: '1.0.0',
    description: 'AI工具推荐平台API',
    endpoints: {
      '/api/tools': '获取AI工具列表',
      '/api/affiliate': '获取Affiliate链接',
      '/api/content': '内容生成接口'
    },
    documentation: 'https://github.com/RicharZhaoyj/ai-link-cn',
    status: 'active'
  });
}