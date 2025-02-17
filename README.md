# AI 智能助手

一个基于火山引擎和 SerpAPI 的智能对话系统，支持实时联网搜索和上下文对话。

## 功能特点

- 🤖 基于火山引擎的智能对话
- 🔍 支持实时联网搜索
- 💬 支持上下文对话记忆
- ⚡ 流式响应，实时显示
- 🌐 跨平台支持
- 🎨 简洁美观的用户界面

## 在线体验

[在线演示地址]（部署后添加链接）

## 本地运行

1. 克隆项目
bash
git clone https://github.com/你的用户名/ai-chat-app.git
cd ai-chat-app

2. 安装依赖
bash
pip install -r requirements.txt

3. 配置环境变量
bash
export SERPAPI_API_KEY="你的 SerpApi 密钥"
export ARK_API_KEY="你的火山引擎 API 密钥"
PORT=5000

4. 运行应用
bash
python app.py

访问 `http://localhost:5000` 即可使用。

## 技术栈

- 后端：Flask
- AI：火山引擎 API
- 搜索：SerpAPI
- 前端：HTML + CSS + JavaScript
- 部署：Vercel

## 使用说明

1. 直接对话：输入问题即可获得 AI 回答
2. 联网搜索：开启搜索开关，AI 将结合最新网络信息回答
3. 清除对话：点击清除按钮可重新开始对话

## 注意事项

- 需要配置相应的 API 密钥才能使用
- 联网搜索功能需要 SerpAPI 支持
- 建议在生产环境中使用 HTTPS

## 开发计划

- [ ] 添加更多搜索引擎支持
- [ ] 优化对话历史管理
- [ ] 添加用户认证功能
- [ ] 支持更多对话模型

## 贡献指南

欢迎提交 Issues 和 Pull Requests 来帮助改进项目。

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎联系：[你的邮箱或其他联系方式]