from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import os
from openai import OpenAI
import time
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API配置
ARK_API_KEY = os.environ.get("ARK_API_KEY", "e9f71adf-9df3-442e-bfb0-0db7a141d20c")
SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY", "b31e64c8d871583a73ea5c60d7f02b634bac6f95c4217db520b106d98672b97f")
SERPAPI_URL = "https://serpapi.com/search.json"

# 初始化OpenAI客户端
client = OpenAI(
    api_key = ARK_API_KEY,
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
    timeout=60.0
)

def search_web(query, num=5):
    """使用 SerpApi 获取 Google 搜索结果"""
    if not SERPAPI_API_KEY:
        return []
        
    params = {
        'api_key': SERPAPI_API_KEY,
        'q': query,
        'num': 10,  # 请求更多结果
        'hl': 'zh-CN',
        'gl': 'cn',
        'google_domain': 'google.com',
        'engine': 'google',
        'safe': 'active',  # 安全搜索
        'start': 0  # 从第一个结果开始
    }
    
    try:
        response = requests.get(SERPAPI_URL, params=params)
        response.raise_for_status()
        search_results = response.json()
        
        results = []
        if 'organic_results' in search_results:
            # 只取前num个最相关的结果
            for item in search_results['organic_results'][:num]:
                # 优化snippet的长度，确保内容充分
                snippet = item.get('snippet', '')
                if len(snippet) < 50 and item.get('description'):  # 如果摘要太短，使用description
                    snippet = item.get('description')
                
                results.append({
                    'title': item.get('title', ''),
                    'snippet': snippet,
                    'url': item.get('link', '')
                })
        return results
    except Exception as e:
        print(f"搜索错误: {e}")
        return []

def format_search_results(search_results):
    """格式化搜索结果为结构化提示"""
    if not search_results:
        return ""
        
    context = (
        "我已获取到以下相关信息，请基于这些信息和你的知识，给出准确、全面的回答。"
        "在回答时，请将搜索到的信息与你的知识自然地结合，并在适当时引用信息来源：\n\n"
    )
    
    for i, result in enumerate(search_results, 1):
        context += f"来源{i}：【{result['title']}】\n"
        context += f"内容：{result['snippet']}\n"
        context += f"链接：{result['url']}\n\n"
    
    return context

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['GET'])
def ask():
    question = request.args.get('question', '')
    history = request.args.get('history', '')
    use_search = request.args.get('search', 'false') == 'true'
    
    # 基础系统提示
    messages = [
        {"role": "system", "content": (
            "你是豆包，是由字节跳动开发的 AI 人工智能助手。"
            + (
                "我已为你提供了一些搜索结果作为参考。请基于这些信息和你的知识给出全面的回答。"
                "在回答时，应自然地引用信息来源，确保回答流畅连贯。"
                if use_search and SERPAPI_API_KEY else
                "请基于你的知识直接回答用户的问题。回答应该准确、专业且富有见地。"
            )
        )}
    ]
    
    # 处理历史对话
    if history:
        try:
            history_pairs = history.split('|')
            for pair in history_pairs:
                if ':' in pair:
                    role, content = pair.split(':', 1)
                    messages.append({"role": role, "content": content})
        except Exception as e:
            print(f"解析历史记录错误: {e}")
    
    # 如果启用搜索，获取并添加搜索结果
    search_context = ""
    if use_search and SERPAPI_API_KEY:
        search_results = search_web(question)
        search_context = format_search_results(search_results)
        if search_context:
            messages.append({"role": "system", "content": search_context})
    
    # 构建用户问题的完整提示
    user_prompt = question
    if search_context:
        user_prompt = f"{question}\n\n请基于上述搜索结果和你的知识回答这个问题。"
    
    messages.append({"role": "user", "content": user_prompt})
    
    def generate():
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                stream = client.chat.completions.create(
                    model="ep-20250217014504-gkqr7",
                    messages=messages,
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield f"data: {chunk.choices[0].delta.content}\n\n"
                
                yield "event: done\ndata: \n\n"
                return
                    
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    error_msg = "连接失败，请稍后重试"
                    if not SERPAPI_API_KEY:
                        error_msg = "SerpApi未配置，但AI助手仍会尽力回答您的问题"
                    yield f"data: Error: {error_msg} ({str(e)})\n\n"
                    yield "event: done\ndata: \n\n"
                    return
                time.sleep(1)
    
    return Response(
        stream_with_context(generate()), 
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

if __name__ == '__main__':
    # 本地运行时使用
    app.run(debug=True)
else:
    # Vercel 部署时使用
    app = app 