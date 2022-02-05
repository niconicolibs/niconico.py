# niconico.py
ニコニコスクレイピングライブラリです。  
これを使うことでニコニコ動画の動画のダウンロードができます。  

**Warning!**  
現在は開発中でリリースされているものもアルファ版です。  
使用者が予期できない変更をすることやバグがある可能性があります。

## Installation
pipを使用してインストールすることができます。  
`pip install niconico.py`

## Example
### ニコニコ動画
#### ダウンロード
```python
from niconico import NicoNico

client = NicoNico()

with client.video.get_video("https://www.nicovideo.jp/watch/sm20780163") as video:
    video.download(f"{video.video.id}.mp4")
```
#### マイリスト
```python
from niconico import NicoNico, Cookies

URL = "https://www.nicovideo.jp/user/31194074/mylist/57162586"

client = NicoNico()
for mylist in client.video.get_mylist(URL):
    print(f"取り出したマイリスト: %s (%s)" % (mylist.name, mylist.id))
```