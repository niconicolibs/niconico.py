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

## ショート動画を検索する

`selectContentType` に対応した検索・ファセット・ユーザー投稿動画の各メソッドで、ショート動画（ID が `ss` で始まる動画）を絞り込めます。`"short"` でショートのみ、`"long"` で通常動画のみ、`"all"` で両方が対象になります。省略時は通常動画のみです。

```python
from niconico import NicoNico

client = NicoNico()
result = client.video.search.search_videos_by_keyword(
    "音楽",
    page_size=10,
    select_content_type="short",
)

if result is not None:
    for video in result.items:
        print(video.id_, video.content_type, video.title)
```

個々の動画がショートかどうかは `content_type`（`"short"` / `"long"`）で判別できます。視聴ページの取得やダウンロードは通常動画と同じメソッドがそのまま使えます。

```python
watch_data = client.video.watch.get_watch_data("ss46649515")
print(watch_data.video.content_type)  # short
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

## ショート動画のフィードを取得する

ショート動画プレイヤーが再生する縦型フィードを取得します。ログインは不要で、返る動画はすべてショート動画です。

```python
from niconico import NicoNico

client = NicoNico()
feed = client.video.get_shorts_feed()

if feed is not None:
    print(feed.total_count)
    for item in feed.items:
        print(item.watch_id, item.content.title)
```

特定のショート動画を起点にしたフィードや、件数の指定もできます。

```python
feed = client.video.get_shorts_feed("ss46649515", page_size=5)
```

## 定番ランキングを取得する

ジャンル別ランキング（`get_ranking`）とは別系統の、視聴ページに表示される定番ランキングです。まず利用可能なキーを取得します。

```python
from niconico import NicoNico

client = NicoNico()

for key in client.video.ranking.get_teiban_ranking_featured_keys():
    print(key.featured_key, key.label)

ranking = client.video.ranking.get_teiban_ranking("e9uj2uks", "24h", page_size=25)

if ranking is not None:
    print(ranking.label, ranking.max_item_count)
    for video in ranking.items:
        print(video.id_, video.title)
```

`page_size` は 25 または 100 のみ指定できます。

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
