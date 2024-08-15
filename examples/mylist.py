"""Example of getting mylist items."""

from niconico import NicoNico

client = NicoNico()

mylist = client.video.get_mylist("61813702")

if mylist is None:
    print("Mylist not found.")
else:
    items = [x.video for x in mylist.items]
    for item in items:
        print(item.title)
