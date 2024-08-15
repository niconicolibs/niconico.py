"""Example of downloading a video."""

from niconico import NicoNico

client = NicoNico()

watch_data = client.video.watch.get_watch_data("sm9")

outputs = client.video.watch.get_outputs(watch_data)
output_label = next(iter(outputs))

downloaded_path = client.video.watch.download_video(watch_data, output_label, ".")

print(downloaded_path)
