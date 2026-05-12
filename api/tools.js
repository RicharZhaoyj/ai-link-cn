// AI工具API端点
export default function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  // 从配置文件读取工具数据
  const tools = {
    writing: [
      { id: 'chatgpt', name: 'ChatGPT', description: 'OpenAI的对话式AI', category: '写作', affiliate: true },
      { id: 'jasper', name: 'Jasper AI', description: '专业的AI写作工具', category: '写作', affiliate: true },
      { id: 'grammarly', name: 'Grammarly', description: 'AI语法检查工具', category: '写作', affiliate: true }
    ],
    image: [
      { id: 'midjourney', name: 'Midjourney', description: 'AI图像生成', category: '图像', affiliate: true },
      { id: 'dalle', name: 'DALL-E 3', description: 'OpenAI图像生成', category: '图像', affiliate: false },
      { id: 'canva', name: 'Canva AI', description: '设计工具+AI', category: '图像', affiliate: true }
    ],
    code: [
      { id: 'copilot', name: 'GitHub Copilot', description: 'AI代码补全', category: '编程', affiliate: false },
      { id: 'codewhisperer', name: 'Amazon CodeWhisperer', description: 'AWS编程工具', category: '编程', affiliate: false },
      { id: 'tabnine', name: 'Tabnine', description: 'AI代码补全', category: '编程', affiliate: true }
    ]
  };
  
  res.status(200).json({
    success: true,
    data: tools,
    count: Object.values(tools).flat().length,
    timestamp: new Date().toISOString()
  });
}