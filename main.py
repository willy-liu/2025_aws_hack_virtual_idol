# main.py

import json, uuid, os, asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Response
from pathlib import Path
import redis.asyncio as aioredis

from function import chat, response, message_buffer
from response_manager import ResponseManager

app = FastAPI()

# Redis async 連線
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis = aioredis.from_url(redis_url, decode_responses=True)

# 插入影片資料夾路徑
GENERATED_VIDEO_DIR = Path("generate")

# 創建 ResponseManager
response_manager = ResponseManager()

@app.get("/")
async def home():
    return FileResponse("templates/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/generate", StaticFiles(directory="generate"), name="generate")
app.mount("/musetalk", StaticFiles(directory="musetalk"), name="musetalk")


@app.websocket("/ws")
async def chat_ws(ws: WebSocket):
    await ws.accept()
    sid = str(uuid.uuid4())
    print(f"[ws] open sid={sid}")

    redis_task = asyncio.create_task(redis_forwarder(ws, sid))
    response_task = asyncio.create_task(scheduled_response(sid))

    try:
        while True:
            text = await ws.receive_text()
            chat(text)  # 收到文字放進 buffer
            await ws.send_json({"type": "ack", "msg": "Received"})
    except WebSocketDisconnect:
        redis_task.cancel()
        response_task.cancel()
        print(f"[ws] close sid={sid}")


async def redis_forwarder(ws: WebSocket, sid: str):
    pubsub = redis.pubsub()
    await pubsub.subscribe(sid)
    print(f"[forwarder] subscribed sid={sid}", flush=True)

    try:
        async for msg in pubsub.listen():
            if msg["type"] == "message":
                print("[forwarder] got", msg["data"], flush=True)
                await ws.send_json(json.loads(msg["data"]))
    except Exception as e:
        print("[forwarder] ERROR", e, flush=True)
    finally:
        await pubsub.unsubscribe(sid)
        await pubsub.close()


async def scheduled_response(sid: str):
    """
    每10秒呼叫 response，把結果用 Redis 推送出去
    """
    while True:
        await asyncio.sleep(10)

        print(f"[debug] message_buffer: {message_buffer}", flush=True)
        
        if message_buffer:
            print("FALSE")
            
            
            from worker import heavy_job  # 延後載入避免循環

            above_text, below_text = response_manager.get_context()

            
            print(f"[debug] 上文：{above_text}", flush=True)
            print(f"[debug] 下文：{below_text}", flush=True)
            
            combined_text = response(above_text, below_text)  # 呼叫新的 response()
            print(f"[debug] 產生的 response：{combined_text}", flush=True)
            
            if combined_text:
                res = heavy_job.delay(combined_text, sid)  # 丟給 Celery
                video_path = f"generate/response_{sid}.mp4"
                print(f"[scheduled_response] SID={sid} 發出新 Task! task_id={res.id} -> 目標影片路徑: {video_path}")

                # 綁定 task id 與生成影片的路徑
                response_manager.bind_task_to_video(res.id, video_path)

                # 更新最新 response
                response_manager.set_last_response(combined_text)


@app.head("/generate/{filename}")
async def check_video_exists(filename: str):
    file_path = GENERATED_VIDEO_DIR / filename
    if file_path.exists():
        return Response(status_code=200)
    return Response(status_code=404)
