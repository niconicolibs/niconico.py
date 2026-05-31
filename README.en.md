![niconico](https://img.shields.io/badge/niconico-(to%20i)-auto?logo=niconico&logoColor=%23e6e6e6&color=%23252525)

[![PyPI](https://img.shields.io/pypi/v/niconico.py?logo=pypi)](https://pypi.org/project/niconico.py/)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-252525?logo=githubpages&logoColor=white)](https://niconicolibs.github.io/niconico.py/)
![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue?logo=python&logoColor=white)
![PyPI - Downloads](https://img.shields.io/pypi/dm/niconico.py?logo=pypi)
![PyPI - License](https://img.shields.io/pypi/l/niconico.py?logo=pypi)

[![Release](https://github.com/niconicolibs/niconico.py/actions/workflows/release.yml/badge.svg)](https://github.com/niconicolibs/niconico.py/actions/workflows/release.yml)
[![PyPI Publish](https://github.com/niconicolibs/niconico.py/actions/workflows/pypi.yml/badge.svg)](https://github.com/niconicolibs/niconico.py/actions/workflows/pypi.yml)

[日本語](README.md) | [English](README.en.md)

# <img src="https://avatars.githubusercontent.com/u/113749892" height="30" /> niconico.py

niconico.py is a Python library for retrieving Niconico video content and information.
It supports video downloads, metadata retrieval, comment retrieval, and more.

## Requirement

Python 3.11 or later is required.

To use the video download function, install [FFmpeg](https://www.ffmpeg.org/) and make it available on your PATH.

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

Example code is available in [examples](https://github.com/niconicolibs/niconico.py/tree/main/examples).

## Command

Use the following command to see CLI usage.

```bash
niconico -h
```

## Contributing

Contributions are welcome. Please describe the purpose and scope clearly in issues and pull requests.

## License

[MIT License](LICENSE)
