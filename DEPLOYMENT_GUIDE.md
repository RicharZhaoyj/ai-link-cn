# 🚀 AI.link.cn Vercel部署指南

本文档提供将AI.link.cn部署到Vercel的完整指南。

## ✅ 当前状态确认

**GitHub仓库已100%更新**：
- ✅ 新项目文件已提交
- ✅ Vercel配置已修复
- ✅ 所有测试通过
- ✅ 可以立即部署

## 🔗 GitHub仓库

**URL**: https://github.com/RicharZhaoyj/ai-link-cn

**最新提交**: `修复Vercel部署配置: 简化项目结构，创建静态网站和API端点`

## 📋 部署步骤

### 步骤1: 访问Vercel

1. 打开 https://vercel.com/new
2. 使用GitHub账号登录
3. 点击"Import Git Repository"

### 步骤2: 导入仓库

1. 在搜索框中输入 `RicharZhaoyj/ai-link-cn`
2. 选择 `ai-link-cn` 仓库
3. 点击"Import"

### 步骤3: 配置项目

Vercel会自动检测配置，但需要确认：

1. **项目名称**: `ai-link-cn` (自动填写)
2. **框架预设**: Vercel会自动检测为"Other" (静态网站)
3. **根目录**: `/` (默认)
4. **构建命令**: 留空 (使用默认)
5. **输出目录**: `.` (当前目录)

**重要**: 确保以下环境变量已设置（Vercel会自动从vercel.json读取）：
- `NODE_ENV=production`
- `SITE_NAME=AI.link.cn`
- `SITE_URL=https://ai.link.cn`

### 步骤4: 配置自定义域名

1. 在Vercel项目设置中，点击"Domains"
2. 添加 `ai.link.cn`
3. 按照提示配置DNS记录

**DNS配置**:
```
记录类型: CNAME
名称: @ 或 ai.link.cn
值: cname.vercel-dns.com
TTL: 自动
```

### 步骤5: 部署

1. 点击"Deploy"
2. 等待构建完成 (约1-2分钟)
3. 访问部署的网站

## 🌐 网站结构

### 主要页面
- `/` - 主页 (index.html)
- `/api` - API信息
- `/api/tools` - AI工具列表API
- `/api/affiliate` - Affiliate链接API

### 静态资源
- `index.html` - 完整的AI工具平台前端
- `config/` - 配置文件
- `src/` - JavaScript源代码
- `docs/` - 文档
- `scripts/` - 实用脚本

## 🛠️ 本地开发

### 启动开发服务器
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
# 或
node scripts/dev-server.js
```

### 访问本地网站
- **URL**: http://localhost:3000
- **API端点**: http://localhost:3000/api

### 测试功能
```bash
# 运行部署测试
node test-deployment.js

# 生成示例内容
node src/content_generator.js review "ChatGPT" "https://chat.openai.com/" "writing"

# 查看Affiliate链接
node src/affiliate_tracker.js list
```

## 📊 部署验证

### 验证网站正常运行
1. 访问 https://ai.link.cn
2. 确认看到AI工具平台首页
3. 测试API端点: https://ai.link.cn/api

### 验证GitHub集成
1. 新的提交会自动触发Vercel部署
2. 查看部署日志: Vercel Dashboard → Deployments

### 验证自定义域名
1. `ai.link.cn` 应该指向Vercel部署
2. HTTPS应该自动启用

## 🔧 故障排除

### 常见问题1: 构建失败
**症状**: Vercel构建失败，显示错误

**解决方案**:
1. 检查 `package.json` 是否有效JSON
2. 确认所有必要文件存在
3. 查看Vercel构建日志

### 常见问题2: 自定义域名不工作
**症状**: `ai.link.cn` 无法访问

**解决方案**:
1. 检查DNS配置是否正确
2. 确认域名已指向Vercel
3. 在Vercel中重新配置域名

### 常见问题3: API端点404
**症状**: `/api` 返回404

**解决方案**:
1. 检查 `vercel.json` 中的路由配置
2. 确认 `api/` 目录存在
3. 检查服务器日志

### 常见问题4: 样式或JS不加载
**症状**: 页面无样式或交互失效

**解决方案**:
1. 检查控制台错误
2. 确认CDN链接有效
3. 检查文件路径是否正确

## 📈 监控和维护

### 监控工具
1. **Vercel Analytics**: 查看网站流量和性能
2. **Google Analytics**: 集成用户行为分析
3. **Uptime Robot**: 监控网站可用性

### 定期维护
1. **每周**: 更新AI工具信息
2. **每月**: 分析Affiliate收入
3. **每季度**: 优化SEO策略

### 备份策略
1. **GitHub**: 代码和内容版本控制
2. **Vercel**: 部署版本回滚
3. **本地备份**: 重要数据本地备份

## 💰 收入启动

### 第1周: 基础设置
1. ✅ 部署网站到Vercel
2. 申请Grammarly Affiliate (最容易)
3. 创建5篇基础内容

### 第1个月: 建立流量
1. 申请3-5个主要AI工具Affiliate
2. 创建20篇高质量内容
3. 开始SEO优化

### 第3个月: 收入增长
1. 月访问量目标: 5,000
2. Affiliate收入目标: $500/月
3. 建立邮件列表

## 🚨 紧急恢复

### 如果部署失败
```bash
# 回滚到上一个版本
# 在Vercel Dashboard中:
# 1. 进入Deployments
# 2. 找到成功的部署
# 3. 点击"Promote to Production"
```

### 如果网站被黑
1. 立即在Vercel中暂停部署
2. 从GitHub恢复干净版本
3. 重新部署

### 如果域名问题
1. 临时使用Vercel提供的域名
2. 修复DNS配置
3. 重新连接自定义域名

## 📞 支持资源

### Vercel支持
- 文档: https://vercel.com/docs
- 社区: https://vercel.com/community
- 支持: support@vercel.com

### GitHub支持
- 文档: https://docs.github.com
- 社区: https://github.com/community

### 项目文档
- `README.md` - 项目概述
- `docs/affiliate_guide.md` - Affiliate申请指南
- `REPLACE_GUIDE.md` - 替换过程记录

## 🎉 部署完成检查清单

- [ ] Vercel项目创建成功
- [ ] GitHub仓库正确导入
- [ ] 自定义域名配置完成
- [ ] 网站可以正常访问 (https://ai.link.cn)
- [ ] API端点正常工作 (/api)
- [ ] HTTPS自动启用
- [ ] 自动部署配置完成
- [ ] 监控工具设置完成

---

**部署完成时间**: 2025年5月12日  
**项目状态**: ✅ 准备就绪，可以立即部署  
**预估上线时间**: 5-10分钟  

**下一步**: 访问 https://vercel.com/new 开始部署！