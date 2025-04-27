from __future__ import annotations
import json
from pathlib import Path
from typing import List
from ..utils.chat_message import ChatMessage
from .nova import invoke_nova

PROMPT_FILE = Path(__file__).resolve().parents[1] / "prompt" / "Vito_interest.txt"
prompt_template = PROMPT_FILE.read_text(encoding="utf-8")

def build_prompt(above: str, messages: List[ChatMessage]) -> str:
    print(f"[debug] build_prompt() called with above: {above}, messages: {messages}")
    """將 ChatMessage 轉為 JSON 格式並套用至 prompt 模板"""
    message_contents = [m.content for m in messages]
    
    formatted_messages = json.dumps(message_contents, ensure_ascii=False)
    
    prompt = prompt_template.format(messages=formatted_messages, above=above)

    return prompt
    
def interest_filter(above: str, messages: List[ChatMessage]) -> str:
    

    prompt = build_prompt(above, messages)

    return invoke_nova(prompt)

PROMPT_FILE_RAG = Path(__file__).resolve().parents[1] / "prompt" / "Vito_interest_rag.txt"
prompt_template_rag = PROMPT_FILE_RAG.read_text(encoding="utf-8")

def build_prompt_rag(above: str, messages: List[ChatMessage]) -> str:
    message_contents = [m.content for m in messages]
    formatted_messages = json.dumps(message_contents, ensure_ascii=False)
    prompt = prompt_template_rag.format(messages=formatted_messages, above=above)
    return prompt
    
def interest_filter_rag(above: str, messages: List[ChatMessage]) -> str:
    prompt = build_prompt_rag(above, messages)
    return invoke_nova(prompt)