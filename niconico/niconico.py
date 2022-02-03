# niconico.py - Client

from __future__ import annotations

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

    def request(self, method: str, url: str, *args, **kwargs) -> requests.Response:
        """``requests.request`` を使用して設定されているクッキーでリクエストを行います。
        引数は ``requests.request`` と同じです。"""
        save_default = True
        if "cookies" not in kwargs and self.cookies is not None:
            save_default = False
            kwargs["cookies"] = {
                key: morsel.value for key, morsel in self.cookies.items()
            }
        response = requests.request(method, url, *args, **kwargs)
        if save_default:
            self.cookies = Cookies(response.cookies.get_dict())
        response.raise_for_status()
        return response