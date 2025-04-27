import boto3
import json

knowledge_base_id = "4QGILNZVD6"
data_source_id = "PIGD11ZHCY"
MODEL_ID = "us.amazon.nova-lite-v1:0"
REGION = "us-west-2"
AWS_ACCESS_KEY_ID = '[YOUR-ACCESS-KEY-ID]'
AWS_SECRET_ACCESS_KEY = '[YOUR-ACCESS-KEY-ID]'

client = boto3.client("bedrock-agent-runtime",
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

def retrieve_from_kb(user_query: str, top_k: int = 1):
    retrieve = ""
    response = client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={
            "text": user_query
        },
        retrievalConfiguration={
            "vectorSearchConfiguration": {
                "numberOfResults": top_k
            }
        }
    )

    retrieved_chunks = response["retrievalResults"]
    for i, chunk in enumerate(retrieved_chunks):
        retrieve += chunk["content"]["text"]
    return retrieve

def get_retriev(raw_response: str) -> str:
    cleaned = raw_response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()
    if cleaned.endswith("```"):
        cleaned = cleaned.removesuffix("```").strip()
    interest_message = json.loads(cleaned)
    interest_message = interest_message.get("messages", [])
    rag_context = ""
    for msg in interest_message :
        if msg["rag"] != 0:
            rag_context += retrieve_from_kb(msg["content"])
    return rag_context