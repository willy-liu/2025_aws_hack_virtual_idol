from tts.vito_tts import vito_tts_request
from musetalk.musetalk import lip_sync_request
import base64

def query_llm(input: str) -> str:
    
    if input == '1':
        # 讀取指定的txt檔案
        with open('static/txt/1.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    
    elif input == '2':
        # 讀取指定的txt檔案
        with open('static/txt/2.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    
    elif input == '3':
        # 讀取指定的txt檔案
        with open('static/txt/3.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    
    elif input == '4':
        # 讀取指定的txt檔案
        with open('static/txt/4.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    
    elif input == '5':
        # 讀取指定的txt檔案
        with open('static/txt/5.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return content

def process_content(content: str):
    """
    處理讀到的內容，可以根據你的需求修改這個function。
    """
    print("🔵 處理中的內容：")
    print(content)

def main():
    """
    主流程：接收輸入，讀取檔案，處理內容。
    """
    user_input = input("請輸入想讀取的段落名稱（例如：第一段）：").strip()
    print(f"🔵 使用者輸入：{user_input}")
    
    content = query_llm(user_input)
    print(f"🔵 讀取的內容：{content}")
    
    response_audio = vito_tts_request(content)
    print(f"🔵 生成的音訊檔案完成")
    
    # 3) Generate Video
    default_video_path = '/home/ubuntu/Virtual-Idol/musetalk/data/video/Vito_720p.mp4'

    print(f"🔵 讀取的影片路徑：{default_video_path}")
    # Encoder 成 base64
    with open(default_video_path, "rb") as f:
        vid_b64 = base64.b64encode(f.read()).decode('utf-8')
        
    print(f"🔵 生成影片中")
    path = lip_sync_request(vid_b64, response_audio, output_path=f"generate/default_{user_input}.mp4")
    
    print(f"影片已生成，路徑：{path}")

if __name__ == "__main__":
    main()
