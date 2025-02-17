# AI 智能助手

基于火山引擎的智能对话助手，支持实时联网搜索，提供流畅的对话体验。

## 功能特点

- 🚀 基于火山引擎大语言模型
- 🌐 支持实时联网搜索
- 💬 流式对话响应
- 📱 响应式界面设计
- 🎨 类聊天软件的界面设计
- ⌛ 优雅的加载动画
- 🕒 消息时间戳显示
- 📝 Markdown 格式支持

## 在线体验

访问：[https://ai-chat-app-xxx.vercel.app](https://ai-chat-app-xxx.vercel.app)

## 本地开发

### 环境要求

- Python 3.8+
- Flask 3.0.0
- OpenAI 0.28.1
- Python-dotenv 1.0.0
- Flask-CORS 4.0.0
- Requests 2.31.0

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/deng3364/ai-chat-app.git
cd ai-chat-app
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
# 创建 .env 文件并添加以下配置
ARK_API_KEY=your_api_key
SERPAPI_API_KEY=your_api_key
```

5. 运行应用
```bash
python app.py
```

访问 http://localhost:5000 开始使用。

## 项目结构

```
ai-chat-app/
├── app.py              # Flask 应用主文件
├── config.py           # 配置文件
├── requirements.txt    # 项目依赖
├── templates/         # HTML 模板
│   └── index.html    # 主页面
├── .gitignore        # Git 忽略文件
├── LICENSE           # 开源协议
├── README.md         # 项目说明
└── vercel.json       # Vercel 配置
```

## 技术栈

- 后端：Flask + Python
- 前端：HTML + CSS + JavaScript + Tailwind CSS
- 部署：Vercel
- API：火山引擎 + SerpApi

## 开源协议

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 联系方式

作者：deng3364
- GitHub：[@deng3364](https://github.com/deng3364)

## 致谢

- [火山引擎](https://www.volcengine.com/)
- [SerpApi](https://serpapi.com/)
- [Vercel](https://vercel.com/)
- [Tailwind CSS](https://tailwindcss.com/)