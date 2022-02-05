
import path_magic
from niconico import NicoNico, Cookies


client = NicoNico()
video = client.video.get_video("https://www.nicovideo.jp/watch/sm20780163")
if video.owner is None:
    print("None")
else:
    print(f"Video Author: {video.owner.__data__}")