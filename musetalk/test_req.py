# 測試呼叫funcion
from musetalk import lip_sync_request
import base64
from datetime import datetime


def test_lip_sync_request(video_path, audio_path, output_path="output-async.mp4", verbose=False, use_cache=True):
    with open(video_path, "rb") as f:
        vid_b64 = base64.b64encode(f.read()).decode()

    with open(audio_path, "rb") as f:
        aud_b64 = base64.b64encode(f.read()).decode()

    lip_sync_request(vid_b64, aud_b64, output_path=output_path, verbose=verbose, use_cache=use_cache)

video_path = "data/video/yongen.mp4"
video_path2 = "data/video/Vito_720p.mp4"
audio_path = "data/audio/yongen.wav"
audio_path2 = "data/audio/eng.wav"
audio_path3 = "data/audio/喜酒.mp3"
audio_path4 = "data/audio/output_vito_tts.mp3"
sing_path = "data/audio/FEniX有多愛_vito.mp3"

# for i in range(1, 13):
#     print(f"Testing {i*5}.mp3")
#     test_lip_sync_request(video_path2, f"data/audio/{i*5}.mp3", output_path="output-async.mp4", verbose=True, use_cache=False)

test_lip_sync_request(video_path2, sing_path, "FEniX有多愛_vito.mp4")