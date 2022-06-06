
import path_magic
from niconico import NicoNico, Cookies


client = NicoNico()
video = client.video.get_video("https://www.nicovideo.jp/watch/sm20780163")
comments = video.get_comments("main", 100)

for comment in comments.chats:
    print(f"Comment: {comment.content}")