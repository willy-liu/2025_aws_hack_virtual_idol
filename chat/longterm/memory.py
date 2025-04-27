import boto3
import uuid

s3_bucket = "aws-2025-hackthon"
s3_prefix = "chat-memory/"
region = "us-east-1"

knowledge_base_id = "4QGILNZVD6"
data_source_id = "PIGD11ZHCY"

AWS_ACCESS_KEY_ID = '[YOUR-ACCESS-KEY-ID]'
AWS_SECRET_ACCESS_KEY = '[YOUR-ACCESS-KEY-ID]'

s3 = boto3.client("s3", 
    region_name=region,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
bedrock_agent = boto3.client("bedrock-agent",
    region_name=region,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

def upload_chat_to_s3(user_id: str, chat_text: str):
    filename = f"{user_id}_{uuid.uuid4().hex}.txt"
    full_key = s3_prefix + filename

    with open(filename, "w", encoding="utf-8") as f:
        f.write(chat_text)

    s3.upload_file(filename, s3_bucket, full_key)

def start_ingestion():
    bedrock_agent.start_ingestion_job(
        knowledgeBaseId=knowledge_base_id,
        dataSourceId=data_source_id
    )

def chat_knowledge_update(file_name: str, chat_text: str):
    upload_chat_to_s3(file_name, chat_text)
    start_ingestion()


