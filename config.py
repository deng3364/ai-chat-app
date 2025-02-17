import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# API 配置
ARK_API_KEY = os.environ.get("ARK_API_KEY", "e9f71adf-9df3-442e-bfb0-0db7a141d20c")
SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY", "b31e64c8d871583a73ea5c60d7f02b634bac6f95c4217db520b106d98672b97f")
SERPAPI_URL = "https://serpapi.com/search.json"

# OpenAI 配置
OPENAI_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
OPENAI_MODEL = "ep-20250217014504-gkqr7"

# 应用配置
DEBUG = os.environ.get("FLASK_ENV") != "production"
PORT = int(os.environ.get("PORT", 5000)) 