# 動画

## 動画情報を取得する

```python
from niconico import NicoNico

client = NicoNico()
video = client.video.get_video("sm9")

if video is not None:
    print(video.title)
```

## 視聴ページ情報を取得する

```python
from niconico import NicoNico

client = NicoNico()
watch_data = client.video.watch.get_watch_data("sm9")

print(watch_data.video.title)
```

## コメントを取得する

```python
from niconico import NicoNico

client = NicoNico()
watch_data = client.video.watch.get_watch_data("sm9")
comments = client.video.watch.get_comments(watch_data)

if comments is not None:
    for thread in comments.threads:
        print(thread.id)
```

## 動画をダウンロードする

```python
from niconico import NicoNico

client = NicoNico()
watch_data = client.video.watch.get_watch_data("sm9")
outputs = client.video.watch.get_outputs(watch_data)

label = next(iter(outputs))
client.video.watch.download_video(watch_data, label)
```

動画ダウンロードには FFmpeg が必要です。
