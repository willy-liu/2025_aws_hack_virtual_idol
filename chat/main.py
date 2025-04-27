from fastapi import FastAPI, HTTPException
from collections import deque
import uvicorn
from concurrent.futures import ThreadPoolExecutor
from .nova.interest_filter import interest_filter_rag
from .nova.generate_response import generate_response_rag
from .nova.generate_response import renew_security_prompt
from .nova.security import security_filter_rag
from .utils.chat_message import ChatMessage
from .utils.response_input import ResponseInput
from .longterm.rag import get_retriev
import time

app = FastAPI()

message_buffer = deque(maxlen=100)

# 創建線程池
thread_pool = ThreadPoolExecutor(max_workers=10)

@app.post("/chat")
async def receive_message(message: ChatMessage):
    try:
        message_buffer.append(message)
        return {
            "status": "success",
            "message_id": len(message_buffer),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/response")
def gen_response(input: ResponseInput):
    security_response = ""
    response = ""
    try:
        interest_table = interest_filter_rag(input.above, message_buffer)
        message_buffer.clear()
        print(interest_table)
        time.sleep(1)
        rag_context = get_retriev(interest_table)
        time.sleep(1)
        print(rag_context)
        while "OK" not in security_response:
            print(security_response)
            renew_security_prompt(security_response)
            ai_response = generate_response_rag(input, interest_table, rag_context)
            security_response = security_filter_rag(ai_response)
        response = ai_response
        message_buffer.clear()
        security_response = ""
        return  response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        workers=4  # 使用多個 worker 進程
    )
