# response_manager.py

from pathlib import Path

class ResponseManager:
    def __init__(self):
        self.last_response_text = None  # 上一次 response 產生的文字
        self.task_video_mapping = {}    # task id -> 檔案路徑
        self.current_video_index = 0    # 目前正在播的 default split (0~4)

    def get_context(self):
        """
        根據當前影片決定上下文
        """
        
        try:
            above_path = Path(f"/home/ubuntu/Virtual-Idol/static/txt/default_{self.current_video_index + 1}.txt")
            print(f"[debug] 上下文檔案路徑：{above_path}")
            next_index = (self.current_video_index + 1) % 5
            print(f"[debug] 下一個影片索引：{next_index}")
            below_path = Path(f"/home/ubuntu/Virtual-Idol/static/txt/default_{next_index + 1}.txt")
            print(f"[debug] 下一個上下文檔案路徑：{below_path}")
            
            if self.last_response_text:
                with open(below_path, "r", encoding="utf-8") as f:
                    below_text = f.read()
                return self.last_response_text, below_text
            else:
                if above_path.exists() and below_path.exists():
                    with open(above_path, "r", encoding="utf-8") as f1, open(below_path, "r", encoding="utf-8") as f2:
                        return f1.read(), f2.read()
                else:
                    print("[warning] 上下文檔案不存在，使用空白字串！")
                    return "", ""
        except Exception as e:
            print(f"[error] get_context() 失敗：{e}")
            return "", ""

    def set_last_response(self, response_text):
        self.last_response_text = response_text

    def bind_task_to_video(self, task_id, video_path):
        self.task_video_mapping[task_id] = video_path

    def check_video_for_current_split(self):
        """
        回傳當前 split 是否有對應 response影片
        """
        for video_path in self.task_video_mapping.values():
            if Path(video_path).exists():
                return video_path
        return None

    def next_default(self):
        self.current_video_index = (self.current_video_index + 1) % 5
