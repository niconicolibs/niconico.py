"""Example of downloading a video."""

import logging

from niconico import NicoNico

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

client = NicoNico()

watch_data = client.video.watch.get_watch_data("sm9")

outputs = client.video.watch.get_outputs(watch_data)
output_label = next(iter(outputs))

downloaded_path = client.video.watch.download_video(watch_data, output_label, "%(title)s.%(ext)s")

print(downloaded_path)
