import asyncio
import time
import json
from fastapi import FastAPI, Request, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: bool = False

async def stream_generator(request: ChatCompletionRequest):
    model_name = request.model
    user_messages = [msg for msg in request.messages if msg.role == "user"]
    user_messages_len = len(user_messages)
    print ("user_messages:", user_messages)
    print ("user_messages_len:", user_messages_len)

    for i in range(5):
        # Simulate receiving user message
        # user_message = next((msg.content for msg in request.messages if msg.role == "user"), "")
        user_message = user_messages[i%user_messages_len].content
        print ("user_message:", user_message)
       
        
        # Create a response chunk
        chunk = {
            "id": f"chatcmpl-123-{i}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model_name,
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "content": f"Hello! You said: '{user_message}'. This is chunk {i} from model {model_name}."
                    },
                    "finish_reason": None
                }
            ]
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(0.5)
    
    # Send the done signal
    yield "data: [DONE]\n\n"


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, authorization: Optional[str] = Header(None)):
    print(f"Received request for model: {request.model}")
    print(f"Authorization Header: {authorization}")
    print(f"Stream: {request.stream}")
    print("Messages:")
    for msg in request.messages:
        print(f"  - Role: {msg.role}, Content: {msg.content}")

    if request.stream:
        return StreamingResponse(stream_generator(request), media_type="text/event-stream")
    else:
        # Non-streaming response can be implemented here if needed
        return {"error": "Non-streaming response not implemented yet."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)