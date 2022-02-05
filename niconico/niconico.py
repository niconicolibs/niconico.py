# niconico.py - Client

from __future__ import annotations

from typing import Optional

from logging import getLogger

import requests

from .video import Client as VideoClient
from .cookies import Cookies


__all__ = ("adjust_cookies", "NicoNico", "logger")
Response = requests.Response
logger = getLogger("niconico.py")
"``logging`` の ``Logger`` です。"


def adjust_cookies(cookies: Cookies) -> dict[str, str]:
    """Cookiesを辞書に変換します。

    Parameters
    ----------
    cookies : Cookies
        辞書に変換するクッキーです。"""
    return {key: morsel.value for key, morsel in cookies.items()}


class NicoNico:
    """ニコニコにアクセスするために使うクラスです。

    Parameters
    ----------
    cookies : Cookies, optional
        リクエストの際に使用するクッキーです。"""

    video: VideoClient
    "ニコニコ動画用のクライアントクラスのインスタンスです。"
    cookies: Optional[Cookies]
    "リクエスト時に使用するクッキーです。"

    def __init__(self, cookies: Optional[Cookies] = None):
        self.video = VideoClient(self)
        self.cookies = cookies
        self.logger = logger

    def request(self, method: str, url: str, *args, **kwargs) -> requests.Response:
        """``requests.request`` を使用して設定されているクッキーでリクエストを行います。
        引数は ``requests.request`` と同じです。

        Notes
        -----
        引数 ``cookies`` に :class:`niconico.cookies.Cookies` を渡した場合は自動で辞書に変換されます。"""
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