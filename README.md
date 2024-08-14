![niconico](https://img.shields.io/badge/niconico-(%E5%B8%B0%E3%81%A3%E3%81%A6%E3%81%8D%E3%81%9F)-auto?logo=niconico&logoColor=%23e6e6e6&color=%23252525)

[![PyPI](https://img.shields.io/pypi/v/niconico.py?logo=pypi)](https://pypi.org/project/niconico.py/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/niconico.py?logo=pypi)
![PyPI - Downloads](https://img.shields.io/pypi/dm/niconico.py?logo=pypi)
![PyPI - License](https://img.shields.io/pypi/l/niconico.py?logo=pypi)

[![Test](https://github.com/niconicolibs/niconico.py/actions/workflows/release.yml/badge.svg)](https://github.com/niconicolibs/niconico.py/actions/workflows/release.yml)
[![Test](https://github.com/niconicolibs/niconico.py/actions/workflows/pypi.yml/badge.svg)](https://github.com/niconicolibs/niconico.py/actions/workflows/pypi.yml)

# niconico.py
niconico.py is a Python library for retrieving Niconico video content and information, and is compatible with the latest version of Niconico.
It allows you to download videos, retrieve information, get comments, and more.

## Installation
You can install it using pip:
```bash
pip install niconico.py
```

## Usage
### video
#### download video
```python
from niconico import NicoNico

client = NicoNico()

watch_data = client.video.watch.get_watch_data("sm9")
outputs = client.video.watch.get_outputs(watch_data)
client.video.watch.download_video(watch_data, "720p", ".")
```

#### get mylist items
```python
from niconico import NicoNico

client = NicoNico()

mylist = client.video.get_mylist("61813702")
items = list(map(lambda x: x.video, mylist.items))
```

## Command
### help
```bash
niconico -h
```
### download video
```bash
niconico download -h
```

## License
[MIT License](LICENSE)
