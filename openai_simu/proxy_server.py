import os
import json
import httpx
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

app = FastAPI()

# 配置 OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
# OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_API_BASE = "http://10.206.1.181:3000/v1"

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: bool = False
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    max_tokens: Optional[int] = None
    enable_thinking: bool = False

async def proxy_stream(url: str, headers: Dict[str, str], json_data: Dict[str, Any]):
    print ("url:", url)
    print ("headers:", headers)
    print ("json_data:", json_data)
    async with httpx.AsyncClient() as client:
        print ("befor call post")
        async with client.stream('POST', url, headers=headers, json=json_data, timeout=None) as response:
            print ("after call post")
            if response.status_code != 200:
                error_detail = await response.aread()
                raise HTTPException(status_code=response.status_code, detail=error_detail)
            
            async for line in response.aiter_lines():
                if line:
                    yield f"{line}\n\n"

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, authorization: Optional[str] = Header(None)):
    # 验证 Authorization 头
    if not authorization:
        print ("API key is empty.")
        #raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    # 准备转发到 OpenAI 的请求
    headers = {
        "Authorization": authorization,  # 使用客户端提供的 token
        "Content-Type": "application/json"
    }
    
    # 构建请求体
    json_data = request.model_dump(exclude_none=True)
    
    # 构建目标 URL
    url = f"{OPENAI_API_BASE}/chat/completions"
    
    if request.stream:
        # 处理流式响应
        return StreamingResponse(
            proxy_stream(url, headers, json_data),
            media_type="text/event-stream"
        )
    else:
        # 处理非流式响应
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=json_data)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)