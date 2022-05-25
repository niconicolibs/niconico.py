
import path_magic
from niconico import NicoNico, Cookies


client = NicoNico()
video = client.video.get_video("https://www.nicovideo.jp/watch/sm20780163")
video._download_log = lambda x: print(f"[INFO] {x}\r", end="")
with video as video:
    video.download(f"{video.video.id}.mp4")
