# niconico.py - Enums

from enum import Enum


class VideoDownloadMode(Enum):
    """ニコニコ動画のダウンロードのモードの列挙型です。

    Attributes
    ----------
    http_output_download_parameters
    hls_parameters"""

    http_output_download_parameters = 1
    hls_parameters = 2