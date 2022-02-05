# Introduction
niconico.pyはニコニコにあるコンテンツを取得するためのライブラリです。  
これを使うことでニコニコ動画の動画のダウンロードができます。  
また、自分のアカウントを使用して動画情報の取得も可能です。

**Warning!**  
現在は開発されたばかりで使用者が予期できない変更やバグがある可能性があります。

## Installation
pipを使用してインストールすることができます。  
`pip install niconico.py`

## Example
### ニコニコ動画
#### ダウンロード
```python
from niconico import NicoNico

client = NicoNico()

with client.video.get_video("https://www.nicovideo.jp/watch/sm37658498") as video:
    video.download(f"{video.video.id}.mp4")
```
#### マイリスト
```python
from niconico import NicoNico, Cookies

URL = "https://www.nicovideo.jp/user/85641805/mylist/63403141"

client = NicoNico()
for mylist in client.video.get_mylist(URL):
    print(f"取り出したマイリスト: %s (%s)" % (mylist.name, mylist.id))
```

## コンソールからの使用
`niconico help`で使用方法を確認可能です。  
注意：コマンドの使用方法は後日変更される予定です。

## Documentation
ドキュメンテーションのテーマに[pydata-sphinx-theme](https://github.com/pydata/pydata-sphinx-theme/blob/master/LICENSE)を使用しています。

## Contributing
リポジトリ内の`contributing.md`をご覧ください。

## License
MITライセンスの下で使用が可能です。