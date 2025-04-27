from datetime import datetime
import base64
import os
from spark_tts import spark_tts_request

# 測試呼叫funcion

# 輸入的文字 (text)
TEXT = "這是繁體中文的測試文本。"

# 風格提示文字 (prompt_text)
PROMPT_TEXT = (
    "吃燕窝就选燕之屋，本节目由26年专注高品质燕窝的燕之屋冠名播出。"
    "豆奶牛奶换着喝，營養更均衡，本节目由豆本豆豆奶特約播出。"
)

# 風格提示音檔 (prompt_speech)，請放一個 .wav 檔
PROMPT_WAV_PATH = "example/prompt_audio.wav"

# 輸出檔名
OUTPUT_MP3 = "example/output_tts.mp3"


def load_wav_base64(path: str) -> str:
    """讀入 WAV 檔並回傳 base64 字串。"""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"WAV 檔不存在：{path}")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    

def save_mp3(base64_str: str, out_path: str):
    """將 base64 字串存成 MP3 檔。"""
    mp3_bytes = base64.b64decode(base64_str)
    with open(out_path, "wb") as f:
        f.write(mp3_bytes)
    print(f"Saved MP3 to {out_path}")

print("Loading prompt WAV...")
prompt_b64 = load_wav_base64(PROMPT_WAV_PATH)

print("Sending TTS request...")
audio_b64 = spark_tts_request(TEXT, PROMPT_TEXT, prompt_b64)

if audio_b64:
    # print("Saving MP3...")
    save_mp3(audio_b64, OUTPUT_MP3)
else:
    print("沒有收到 audio 欄位，請檢查 API 回傳。")
    