# niconico.py - Enums

from enum import Enum


__all__ = ("VideoDownloadMode",)


class VideoDownloadMode(Enum):
    "ニコニコ動画のダウンロードのモードの列挙型です。"

    http_output_download_parameters = 1
    "mp4動画ファイル形式で読み込む。"
    hls_parameters = 2
    "hlsで読み込む。"