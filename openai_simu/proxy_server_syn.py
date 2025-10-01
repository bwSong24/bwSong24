import os
import json
import requests
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

def proxy_stream(url: str, headers: Dict[str, str], json_data: Dict[str, Any]):
    print("url:", url)
    print("headers:", headers)
    print("json_data:", json_data)
    
    response = requests.post(url, headers=headers, json=json_data, stream=True)
    print("after call post")
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    for line in response.iter_lines():
        if line:
            #print ('test yield')
            yield f"{line.decode('utf-8')}\n\n"
    

@app.post("/v1/chat/completions")
def chat_completions(request: ChatCompletionRequest, authorization: Optional[str] = Header(None)):
    print(f"Received request for model: {request.model}")
    print(f"Authorization Header: {authorization}")
    print(f"Stream: {request.stream}")
    print("Messages:")
    for msg in request.messages:
        print(f"  - Role: {msg.role}, Content: {msg.content}")

    if not authorization:
        print ("API key is empty.")
        # raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }
    
    json_data = request.model_dump(exclude_none=True)
    url = f"{OPENAI_API_BASE}/chat/completions"
    
    if request.stream:
        print ('proxy_stream use')
        return StreamingResponse(proxy_stream(url, headers, json_data), media_type="text/event-stream")
    else:
        response = requests.post(url, headers=headers, json=json_data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)