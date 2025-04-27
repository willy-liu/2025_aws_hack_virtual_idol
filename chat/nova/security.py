from __future__ import annotations
import json
from pathlib import Path
from typing import List
from ..utils.chat_message import ChatMessage
from .nova import invoke_nova

PROMPT_FILE = Path(__file__).resolve().parents[1] / "prompt" / "image_safety.txt"
prompt_template = PROMPT_FILE.read_text(encoding="utf-8")

def build_prompt(ai_message: str) -> str:
    prompt = prompt_template.format(ai_message=ai_message)
    return prompt
    
def security_filter(ai_message: str) -> str:
    prompt = build_prompt(ai_message)
    return invoke_nova(prompt)

PROMPT_FILE_RAG = Path(__file__).resolve().parents[1] / "prompt" / "image_safety_rag.txt"
prompt_template_rag = PROMPT_FILE.read_text(encoding="utf-8")

def build_prompt_rag(ai_message: str) -> str:
    prompt = prompt_template_rag.format(ai_message=ai_message)
    return prompt

def security_filter_rag(ai_message: str) -> str:
    prompt = build_prompt_rag(ai_message)
    return invoke_nova(prompt)