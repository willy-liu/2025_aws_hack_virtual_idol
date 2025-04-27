from vito_tts import vito_tts_request
import time
start = time.time()
text = """
    聊天室有人問：「Vito，你怎麼開始唱歌的？」
    哇這問題好欸！  

    其實我小時候家裡常常放卡帶、CD，我就一直聽一直唱，  
    到最後就愛上唱歌了，覺得音樂是一種超強的能量！  
    我希望40歲的我，還能站在舞台上大唱特唱啊～

    我不管啦！我就是要唱到老唱到世界末日哈哈哈！

    有人說：「你最喜歡哪種歌？」  
    欸～～我最喜歡那種可以帶動氣氛的歌！大家一起嗨起來的那種～  
    但偶爾我也會唱一些超走心的歌啦，看心情看月亮
"""
# mp3_byte = vito_tts_request(text=text)
mp3_byte = vito_tts_request(text="聊天室有人問：「Vito，你怎麼開始唱歌的？」")

with open ("example/output_vito_tts.mp3", "wb") as f:
    f.write(mp3_byte)

print(f"花費時間:{time.time()-start}")