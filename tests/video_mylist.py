
import path_magic
from niconico import NicoNico, Cookies


URL = "https://www.nicovideo.jp/user/31194074/mylist/57162586"


client = NicoNico()
for mylist in client.video.get_mylist(URL):
    print(f"Extracted mylist: %s (%s)" % (mylist.name, mylist.id))
    for item in mylist.items:
        print(f"\tVideo: %s (%s)" % (item.video.title, item.video.url))
