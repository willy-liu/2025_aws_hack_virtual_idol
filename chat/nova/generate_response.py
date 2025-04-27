from __future__ import annotations
from pathlib import Path
from typing import List
from ..utils.chat_message import ChatMessage
from ..utils.response_input import ResponseInput
from .nova import invoke_nova
import json

PROMPT_FILE = Path(__file__).resolve().parents[1] / "prompt" / "Vito_response.txt"
prompt_template = PROMPT_FILE.read_text(encoding="utf-8")

def build_prompt(input: ResponseInput, messages: List[str]) -> str:
    prompt = prompt_template.format(messages=messages, above=input.above, below=input.below, security_response="")
    return prompt

def message_process(raw_response: str) -> List[ChatMessage]:
    cleaned = raw_response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()
    if cleaned.endswith("```"):
        cleaned = cleaned.removesuffix("```").strip()
    interest_message = json.loads(cleaned)
    interest_message = interest_message.get("messages", [])
    interest_message = [msg["content"] for msg in interest_message]
    return interest_message

def renew_security_prompt(security_response: str):
    global prompt_template
    format_security_response = "{security_response}" + security_response
    new_prompt = (
        prompt_template
        .replace("{security_response}", format_security_response)
        .replace("{above}", "{above}")
        .replace("{messages}", "{messages}")
        .replace("{below}", "{below}")
    )
    # PROMPT_FILE.write_text(new_prompt, encoding="utf-8")
    prompt_template = new_prompt
    
def generate_response(input: ResponseInput, messages: str) -> str:
    interest_message = message_process(messages)
    prompt = build_prompt(input, interest_message)
    return invoke_nova(prompt)

PROMPT_FILE_RAG = Path(__file__).resolve().parents[1] / "prompt" / "Vito_response_rag.txt"
prompt_template_rag = PROMPT_FILE_RAG.read_text(encoding="utf-8")

def build_prompt_rag(input: ResponseInput, messages: List[str], rag_context: str) -> str:
    prompt = prompt_template_rag.format(messages=messages, above=input.above, below=input.below, security_response="", rag=rag_context)
    return prompt

def generate_response_rag(input: ResponseInput, messages: str, rag_context: str) -> str:
    interest_message = message_process(messages)
    prompt = build_prompt_rag(input, interest_message, rag_context)
    return invoke_nova(prompt)