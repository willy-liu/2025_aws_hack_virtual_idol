import requests
import base64

def vito_tts_request(
    text: str,
    model_id: int = 6,
    speaker_name: str = "puyang",
    speed_factor: float = 1.0,
    mode: str = "stream",
    token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhd3NfaGFja2F0aG9uIiwiZXhwaXJlcyI6MTc0NTc0ODAwMH0.9qpg1xraE_d_Hua2brAmCfRlQSce6p2kdipgq8j1iqo",
    env: str = "prod"  # "uat" or "prod"
) -> bytes:
    """
    根據輸入文字生成 mp3 語音並以 bytes 形式返回。
    """
    assert model_id in [1,2,4,5,6]
    assert speaker_name in ["long", "max", "chiachi", "junting", "puyang"]
    assert env in ["uat", "prod"], "env must be 'uat' or 'prod'"
    assert mode in ["stream", "file"], "mode must be 'stream' or 'file'"
    
    base_url = {
        "uat": "https://uat-persona-sound.data.gamania.com",
        "prod": "https://persona-sound.data.gamania.com"
    }[env]

    url = f"{base_url}/api/v1/public/voice"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    params = {
        "text": text,
        "model_id": model_id,
        "speaker_name": speaker_name,
        "speed_factor": speed_factor,
        "mode": mode
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        audio_bytes = response.content
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        return audio_b64
    else:
        raise Exception(f"Voice API Error: {response.status_code}, {response.text}")
