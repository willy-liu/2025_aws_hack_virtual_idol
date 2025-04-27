import boto3
import base64
import json
import time
from datetime import datetime

PROFILE = "aws_hack"
AWS_REGION = "us-west-2"
BUCKET_NAME = "aws-2025-hackthon"
MODEL_NAME = "musetalk"
EndpointName = "musetalk-async-endpoint"   # 這裡記得改成你實際的 endpoint 名稱

def lip_sync_request(vid_b64: str, aud_b64: str, output_path: str = "output-async.mp4", verbose=False, use_cache=True) -> str:
    start = time.time()
    session = boto3.Session(profile_name=PROFILE, region_name=AWS_REGION)
    s3      = session.client("s3")
    runtime = session.client("sagemaker-runtime")
    payload = json.dumps({
        "mode": "realtime",
        "batch_size": 4,
        "video": vid_b64,
        "audio": aud_b64,
        "use_cache": use_cache
    })
    INPUT_KEY = f"{MODEL_NAME}-inputs/{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    input_s3_uri   = f"s3://{BUCKET_NAME}/{INPUT_KEY}"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=INPUT_KEY,
        Body=payload,
        ContentType="application/json"
    )
    async_response = runtime.invoke_endpoint_async(
        EndpointName   = EndpointName,
        ContentType    = "application/json",
        InputLocation  = input_s3_uri,
        RequestTTLSeconds       = 21600,
        InvocationTimeoutSeconds= 3600
    )

    OUTPUT_KEY = f"{MODEL_NAME}-outputs/" + async_response["OutputLocation"].split("/")[-1]
    FAIL_OUTPUT_KEY = f"{MODEL_NAME}-outputs/" + async_response["FailureLocation"].split("/")[-1]

    success = False
    while True:
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=OUTPUT_KEY)
            success = True
            break
        except s3.exceptions.ClientError:
            pass
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=FAIL_OUTPUT_KEY)
            break
        except s3.exceptions.ClientError:
            pass
        time.sleep(1)

    if not success:
        return ""
    
    response = s3.get_object(Bucket=BUCKET_NAME, Key=OUTPUT_KEY)
    body = response["Body"].read()
    
    if verbose:
        print("time(s):", time.time()-start)

    with open(output_path, "wb") as f:
        f.write(body)
    
    return output_path
