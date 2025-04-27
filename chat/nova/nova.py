from __future__ import annotations
import json
import boto3

MODEL_ID = "us.amazon.nova-lite-v1:0"
REGION = "us-west-2"
AWS_ACCESS_KEY_ID = '[YOUR-ACCESS-KEY-ID]'
AWS_SECRET_ACCESS_KEY = '[YOUR-ACCESS-KEY-ID]'

def invoke_nova(prompt: str) -> str:
    client = boto3.client(
        "bedrock-runtime", 
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    payload = {
        "inferenceConfig": {
            "max_new_tokens": 1000
        },
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
    }
    try:
        response = client.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )
        response_body = json.loads(response["body"].read())
        return response_body["output"]["message"]["content"][0]["text"]

    except Exception as e:
        raise RuntimeError(f"Failed to invoke Nova model: {e}")