# 🤝 贡献指南

感谢你考虑为 **AI.link.cn** 项目贡献代码！这份指南将帮助你开始贡献。

## 📋 贡献方式

### 1. 报告Bug
- 使用 [GitHub Issues](https://github.com/RicharZhaoyj/ai-link-cn/issues) 报告bug
- 提供详细的bug描述、重现步骤和环境信息

### 2. 请求新功能
- 通过 Issues 提出功能建议
- 描述功能解决的问题和预期效果

### 3. 提交代码
- Fork 项目仓库
- 创建功能分支
- 提交清晰的 commit 信息
- 创建 Pull Request

## 🚀 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/RicharZhaoyj/ai-link-cn.git
cd ai-link-cn
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行测试
```bash
# 运行基本测试
python -m pytest tests/

# 运行API测试
python tests/test_api.py
```

## 📝 代码规范

### 1. Python 代码风格
- 遵循 PEP 8 规范
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序

### 2. Commit 信息规范
使用约定式提交：
- `feat:` 新功能
- `fix:` bug修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

### 3. Pull Request 流程
1. Fork 主仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 🏗️ 项目结构

```
ai-link-cn/
├── api/                    # API接口
│   ├── auth.py            # 用户认证
│   ├── hello.py           # 欢迎API
│   └── premium/           # 高级API
├── docs/                  # 文档
├── scripts/               # 脚本
├── tests/                 # 测试
└── *.py                   # 主程序文件
```

## 🔧 开发指南

### API 开发
- 所有API端点应该在 `api/` 目录下
- 使用统一的错误处理
- 添加适当的文档字符串

### 测试要求
- 新功能必须包含测试
- 测试覆盖率达到80%以上
- 使用 pytest 作为测试框架

### 文档要求
- 所有公开函数都需要文档字符串
- 更新 README.md 中的相关部分
- 添加使用示例

## 🐛 调试帮助

### 常见问题
1. **导入错误**: 确保在项目根目录运行
2. **API错误**: 检查Vercel部署状态
3. **数据获取失败**: 检查网络连接和API密钥

### 调试工具
```python
# 启用调试模式
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 联系与支持

- **问题讨论**: [GitHub Discussions](https://github.com/RicharZhaoyj/ai-link-cn/discussions)
- **Bug报告**: [GitHub Issues](https://github.com/RicharZhaoyj/ai-link-cn/issues)
- **邮件联系**: ai@link.cn

## 🙏 感谢贡献

感谢所有为这个项目做出贡献的人！你的努力让这个项目变得更好。

---

**注意**: 提交Pull Request即表示你同意你的贡献将在MIT许可证下发布。