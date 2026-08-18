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

## スナップショット検索 API で検索する

[スナップショット検索 API v2](https://site.nicovideo.jp/search-api-docs/snapshot) を利用した検索です。ログイン不要で、再生数などの条件で絞り込めます。

```python
from niconico import NicoNico

client = NicoNico()
result = client.video.search.search_videos_by_snapshot(
    "初音ミク",
    ["title", "tags"],
    sort_key="viewCounter",
    fields=["contentId", "title", "viewCounter"],
    filters={"viewCounter": {"gte": "10000"}},
    limit=5,
)

if result is not None:
    print(result.meta.total_count)
    for item in result.data:
        print(item.content_id, item.view_counter, item.title)
```

`fields` で指定したフィールドだけが応答に含まれるため、`SnapshotVideoItem` の各属性は指定しない限り `None` になります。`_context` に相当する `context` 引数には、利用するサービス名やアプリ名を指定してください。

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
