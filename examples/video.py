"""Example of getting video information."""

from niconico import NicoNico

client = NicoNico()

video = client.video.get_video("sm9")

if video is None:
    print("Video not found.")
else:
    print(video.title)
    print(video.short_description)
