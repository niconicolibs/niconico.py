![niconico](https://img.shields.io/badge/niconico-(%E5%B8%B0%E3%81%A3%E3%81%A6%E3%81%8D%E3%81%9F)-auto?logo=niconico&logoColor=%23e6e6e6&color=%23252525)

[![PyPI](https://img.shields.io/pypi/v/niconico.py?logo=pypi)](https://pypi.org/project/niconico.py/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/niconico.py?logo=pypi)
![PyPI - Downloads](https://img.shields.io/pypi/dm/niconico.py?logo=pypi)
![PyPI - License](https://img.shields.io/pypi/l/niconico.py?logo=pypi)
![Website](https://img.shields.io/website?label=docs&logo=github&url=https%3A%2F%2Fniconicolibs.github.io%2Fniconico.py)

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

## Example
### nicovideo
#### Download video
```python
from niconico import NicoNico

client = NicoNico()

watch_data = client.video.watch.get_watch_data("sm9")
outputs = client.video.watch.get_outputs(watch_data)
client.video.watch.download_video(watch_data, "720p", ".")
```

## License
[MIT License](LICENSE)
