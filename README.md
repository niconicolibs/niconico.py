[![PyPI](https://img.shields.io/pypi/v/niconico.py)](https://pypi.org/project/niconico.py/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/niconico.py) ![PyPI - Downloads](https://img.shields.io/pypi/dm/niconico.py) ![PyPI - License](https://img.shields.io/pypi/l/niconico.py) [![Documentation Status](https://readthedocs.org/projects/niconico-py/badge/?version=latest)](https://niconico-py.readthedocs.io/ja/latest/?badge=latest)
# niconico.py
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
from niconico import NicoNico

URL = "https://www.nicovideo.jp/user/85641805/mylist/63403141"

client = NicoNico()
for mylist in client.video.get_mylist(URL):
    print(f"取り出したマイリスト: %s (%s)" % (mylist.name, mylist.id))
```

## コンソールからの使用
`niconico help`で使用方法を確認可能です。  
注意：コマンドの使用方法は後日変更される予定です。

## ToDo
* [x] 動画のダウンロード
* [x] マイリストの読み込み
* [ ] 検索
* [ ] ニコニコ大百科
* [ ] ニコニコ静画
* [ ] 非同期版 (できれば)
* [ ] etc

## Contributing
リポジトリ内の`contributing.md`をご覧ください。

## License
MITライセンスの下で使用が可能です。
