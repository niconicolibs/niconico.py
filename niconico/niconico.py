# niconico.py - Client

from typing import Optional

from logging import getLogger

import requests

from .video import Client as VideoClient
from .cookies import Cookies


Response = requests.Response
logger = getLogger("niconico.py")


class NicoNico:
    """ニコニコにアクセスするために使うクラスです。"""

    def __init__(self, cookies: Optional[Cookies] = None):
        self.video = VideoClient(self)
        self.cookies = cookies
        self.logger = logger

    def request(
        self, method: str, url: str, *args, **kwargs
    ) -> requests.Response:
        """``requests.request`` を使用して設定されているクッキーでリクエストを行います。
        引数は ``requests.request`` と同じです。"""
        kwargs["cookies"] = self.cookies
        response = requests.request(method, url, *args, **kwargs)
        response.raise_for_status()
        if self.cookies is None:
            self.cookies = Cookies.guest(response.cookies["nicosid"])
        return response
