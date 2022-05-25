
import path_magic
from niconico import NicoNico, Cookies


client = NicoNico(Cookies.from_file("cookies.txt"))
video = client.video.get_video("https://www.nicovideo.jp/watch/sm37658498")
print(f"好き：{video.video.viewer.like.isLiked}")
