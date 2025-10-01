import requests
import json

def stream_chat(message):
    # url = "http://localhost:3000/v1/chat/completions"
    url = "http://10.100.34.42:5941/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer test-key"
    }
    data = {
        # "model": "gpt-4.1",
        "model": "qwen3-8b",
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": True,
        "enable_thinking": True
    }

    # 发送请求并获取流式响应
    with requests.post(url, headers=headers, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                # 移除 'data: ' 前缀
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    line = line[6:]
                if line == '[DONE]':
                    break
                try:
                    # 解析 JSON 响应
                    chunk = json.loads(line)
                    # 提取并打印内容
                    if 'choices' in chunk and len(chunk['choices']) > 0:
                        content = chunk['choices'][0]['delta'].get('content', '')
                        if content:
                            print(content, end='', flush=True)
                except json.JSONDecodeError:
                    continue
        print('\n')

if __name__ == "__main__":
    while True:
        user_input = input("\n请输入您的问题（输入 'quit' 退出）: ")
        if user_input.lower() == 'quit':
            break
        stream_chat(user_input)