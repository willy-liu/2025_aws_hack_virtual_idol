from celery import Celery
import base64, time, uuid, os, redis, json
from function import query_llm, generate_audio_file, test_send_request
import redis.asyncio as aioredis   # ← 同樣換 async 版
from musetalk.musetalk import lip_sync_request
from tts.vito_tts import vito_tts_request
import time
# vito_tts_request(text = "")

celery = Celery("worker", broker="redis://localhost:6379/0")
# redis_pub = redis.Redis(host="redis", decode_responses=True)
redis_pub = redis.Redis(host="localhost", port=6379, decode_responses=True)
# redis_pub = aioredis.from_url("redis://localhost:6379/0", decode_responses=True)


@celery.task
def heavy_job(text, sid):
    print(f"[heavy_job] SID={sid} 正在處理 task 任務...")

    # 2) Generate Audio
    # response_audio = generate_audio_file(response_LLM)
    response_audio = vito_tts_request(text)
    print(f"[heavy_job] SID={sid} 音檔生成成功")

    # 3) Generate Video
    default_video_path = '/home/ubuntu/Virtual-Idol/musetalk/data/video/Vito_720p.mp4'

    with open(default_video_path, "rb") as f:
        vid_b64 = base64.b64encode(f.read()).decode('utf-8')

    response_video = lip_sync_request(vid_b64, response_audio,  output_path=f"generate/response_{sid}.mp4", verbose=False, use_cache=True)

    # 產生影片
    public_url = response_video
    print(f"[heavy_job] SID={sid} 影片生成完成，影片路徑：{public_url}")

    # Publish 成功訊息給 sid
    redis_pub.publish(
        sid,
        json.dumps({"type": "switch", "url": public_url, "ts": int(time.time())})
    )
    
    print(f"[heavy_job] SID={sid} 成功推送影片訊息到 redis，完成！")

    return public_url
