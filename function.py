# function.py

import os
import json
import base64
from pathlib import Path
from collections import deque
from chat.nova.interest_filter import interest_filter
from chat.nova.generate_response import generate_response, renew_security_prompt
from chat.nova.security import security_filter
from typing import List          # <— 新增
from chat.utils.chat_message import ChatMessage  
from chat.utils.response_input import ResponseInput

# 全域聊天訊息 buffer
message_buffer = deque(maxlen=50)

# 定義產生影片的資料夾
GENERATED_VIDEO_DIR = Path("generate")


def chat(message: str):
    message_buffer.append(message)

def response(above_text: str, below_text: str) -> str:
    print(f"[debug] Respnse function called with above_text: {above_text}, below_text: {below_text}")

    if not message_buffer:
        return ""

    try:
        # ① 先把 deque 中的純字串轉成 ChatMessage 物件
        chat_messages: List[ChatMessage] = [
            ChatMessage(user_id="user", content=msg) for msg in message_buffer
        ]

        # ② 交給 interest_filter
        interest_table = interest_filter(above_text, chat_messages)
        print("[debug] Finished interest_filter")

        # 以下原本流程…
        security_response = ""
        while "OK" not in security_response:
            renew_security_prompt(security_response)
            print(f"[debug] renew_security_prompt:{security_response}")
            input = ResponseInput(above=above_text, below=below_text)
            ai_response = generate_response(input, interest_table)
            # print(f"[debug] Finished generate_response:{ai_response}")
            security_response = security_filter(ai_response)
            # print(f"[debug] Finished security_filter:{security_response}")
        print(f"[debug] Finished security_filter")
        response = ai_response
        message_buffer.clear()
        security_response = ""
        # print(f"[debug] Final response: {response}")
        return response

    except Exception as e:
        raise Exception(f"Response generation failed: {e}")



def query_llm(input_text: str) -> str:
    """
    模擬文字轉文字 LLM API
    """
    mapping = {
        '第一段': 'static/txt/1.txt',
        '第二段': 'static/txt/2.txt',
        '第三段': 'static/txt/3.txt',
        '第四段': 'static/txt/4.txt',
        '第五段': 'static/txt/5.txt'
    }
    path = mapping.get(input_text)
    if path and os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "找不到指定段落內容。"


def generate_audio_file(text: str) -> str:
    """
    模擬文字轉語音 API
    """
    if text == '你好, 我是小明':
        return 'static/audio/1.mp3'
    elif text == '早安，幫媽媽採朵花':
        return 'static/audio/2.mp3'
    else:
        return 'static/audio/3.mp3'

def test_send_request(vid_b64: str, aud_b64: str) -> str:
    print(f"[debug] test_send_request")
    pass