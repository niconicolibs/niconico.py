# niconico.py - Client

from __future__ import annotations

from typing import Optional

from logging import getLogger

import requests

from .video import Client as VideoClient
from .cookies import Cookies


Response = requests.Response
logger = getLogger("niconico.py")


def adjust_cookies(cookies: Cookies) -> dict[str, str]:
    "Cookiesを辞書に変換します。"
    return {key: morsel.value for key, morsel in cookies.items()}


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

        # クッキーの調整をする。
        if "cookies" not in kwargs:
            save_default = False
            if self.cookies is not None:
                # kwargsにクッキーがないのならそのクッキーを設定する。
                kwargs["cookies"] = self.cookies
            elif kwargs.pop("require_cookies", False):
                # もしクッキーが必須の場合かつクッキーが指定されていないのならゲスト用のクッキーを作る。
                kwargs["cookies"] = Cookies.guest()
        # クッキーがCookiesクラスになっているなら辞書にする。
        if isinstance(kwargs.get("cookies", {}), Cookies):
            kwargs["cookies"] = adjust_cookies(kwargs["cookies"])

        # デバッグログを出力する。
        self.logger.debug("リクエスト: (%s) %s" % (method, url))
        for key, value in (
            ("cookies", "クッキー"), ("params", "パラメーター"),
            ("json", "JSON")
        ):
            if key in kwargs:
                self.logger.debug("使用予定の%s: %s" % (value, kwargs[key]))

        # リクエストをする。
        response = requests.request(method, url, *args, **kwargs)
        if save_default:
            self.cookies = Cookies(response.cookies.get_dict())
        response.raise_for_status()
        return response