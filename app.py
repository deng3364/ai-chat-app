from flask import Flask, render_template, request, jsonify, Response
import openai
import time
import requests
from flask_cors import CORS
from config import *

app = Flask(__name__)
CORS(app)

# 配置 OpenAI
openai.api_key = ARK_API_KEY
openai.api_base = OPENAI_API_BASE

class AIChat:
    @staticmethod
    def search_web(query, num=5):
        """使用 SerpApi 获取搜索结果"""
        if not SERPAPI_API_KEY:
            return []
            
        params = {
            'api_key': SERPAPI_API_KEY,
            'q': query,
            'num': 10,
            'hl': 'zh-CN',
            'gl': 'cn',
            'google_domain': 'google.com',
            'engine': 'google',
            'safe': 'active',
            'start': 0
        }
        
        try:
            response = requests.get(SERPAPI_URL, params=params)
            response.raise_for_status()
            results = []
            for item in response.json().get('organic_results', [])[:num]:
                snippet = item.get('snippet', '') or item.get('description', '')
                results.append({
                    'title': item.get('title', ''),
                    'snippet': snippet,
                    'url': item.get('link', '')
                })
            return results
        except Exception as e:
            print(f"搜索错误: {e}")
            return []

    @staticmethod
    def format_search_results(search_results):
        """格式化搜索结果"""
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

    @staticmethod
    def create_chat_response(messages):
        """创建聊天响应"""
        def generate():
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries:
                try:
                    response = openai.ChatCompletion.create(
                        model=OPENAI_MODEL,
                        messages=messages,
                        stream=True
                    )
                    
                    for chunk in response:
                        if chunk.choices[0].delta.get('content'):
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
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['GET'])
def ask():
    question = request.args.get('question', '')
    history = request.args.get('history', '')
    use_search = request.args.get('search', 'false') == 'true'
    
    # 构建消息
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
            for pair in history.split('|'):
                if ':' in pair:
                    role, content = pair.split(':', 1)
                    messages.append({"role": role, "content": content})
        except Exception as e:
            print(f"解析历史记录错误: {e}")
    
    # 处理搜索结果
    if use_search and SERPAPI_API_KEY:
        search_results = AIChat.search_web(question)
        search_context = AIChat.format_search_results(search_results)
        if search_context:
            messages.append({"role": "system", "content": search_context})
    
    # 添加用户问题
    messages.append({"role": "user", "content": question})
    
    return AIChat.create_chat_response(messages)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

# 应用入口
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
else:
    app = app 