![niconico](https://img.shields.io/badge/niconico-(to%20i)-auto?logo=niconico&logoColor=%23e6e6e6&color=%23252525)

[![PyPI](https://img.shields.io/pypi/v/niconico.py?logo=pypi)](https://pypi.org/project/niconico.py/)
![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue?logo=python&logoColor=white)
![PyPI - Downloads](https://img.shields.io/pypi/dm/niconico.py?logo=pypi)
![PyPI - License](https://img.shields.io/pypi/l/niconico.py?logo=pypi)

[![Release](https://github.com/niconicolibs/niconico.py/actions/workflows/release.yml/badge.svg)](https://github.com/niconicolibs/niconico.py/actions/workflows/release.yml)
[![PyPI Publish](https://github.com/niconicolibs/niconico.py/actions/workflows/pypi.yml/badge.svg)](https://github.com/niconicolibs/niconico.py/actions/workflows/pypi.yml)

[日本語](README.md) | [English](README.en.md)

# <img src="https://avatars.githubusercontent.com/u/113749892" height="30" /> niconico.py

niconico.py は、ニコニコ動画のコンテンツや情報を取得するための Python ライブラリです。
動画のダウンロード、動画情報の取得、コメント取得などを扱えます。

## Requirements

Python 3.11 以降が必要です。

動画ダウンロード機能を利用する場合は、[FFmpeg](https://www.ffmpeg.org/) をインストールしてパスを通してください。

## Installation

```bash
pip install niconico.py
```

## Usage

```python
from niconico import NicoNico

client = NicoNico()
```

### Examples

サンプルコードは [examples](https://github.com/niconicolibs/niconico.py/tree/main/examples) にあります。

## CLI

CLI の使い方は次のコマンドで確認できます。

```bash
niconico -h
```

## Contributing

コントリビューションは歓迎します。Issue や PR では、目的と変更内容が分かるように記載してください。

## License

[MIT License](LICENSE)
