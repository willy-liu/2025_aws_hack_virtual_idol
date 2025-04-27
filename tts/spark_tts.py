import os, time, subprocess, base64, json
import boto3

# 要使用的 AWS CLI/profile 名稱
PROFILE = "aws_hack"

# AWS 區域、ECR 與 SageMaker 設定
AWS_REGION    = "us-west-2"
MODEL_NAME    = "spark-tts"
EndpointName = f"{MODEL_NAME}-endpoint"


# 呼叫 Endpoint 並下載回傳影片 (範例)
def spark_tts_request(text: str, prompt_text: str, prompt_b64: str) -> bytes:
    """呼叫 API，回傳原始 response bytes（預期是 base64 mp3音檔"""
    start = time.time()
    session = boto3.Session(region_name=AWS_REGION, profile_name=PROFILE)
    runtime = session.client("sagemaker-runtime")
    payload = json.dumps({
        "text": text,
        "prompt_text": prompt_text,
        "prompt_speech": prompt_b64
    })
    resp = runtime.invoke_endpoint(
        EndpointName=EndpointName,
        ContentType="application/json",
        Body=payload)
    
    body = resp["Body"].read()  # 讀取檔案內容(應該是mp4的binary)
    elapsed = time.time() - start
    print(f"Request took {elapsed:.2f}s")


    return json.loads(body.decode())["audio"]
