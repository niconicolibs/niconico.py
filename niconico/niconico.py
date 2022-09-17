# niconico.py - Client

from __future__ import annotations

from typing import Optional

from logging import getLogger
import re

import requests

from .video import Client as VideoClient
from .search import SearchClient
from .cookies import Cookies

from .exceptions import LoginFailureException


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
        self.searchclient = SearchClient(self)
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

    def login(self, mail: str, password: str) -> NicoNico:
        """メールアドレスとパスワードを用いてログインを行います。
        二段階認証が有効になっているアカウントではログインすることができません。
        クッキーの中身を直接置き換える方法で認証をしてください。

        Parameters
        ----------
        mail : str
            ログインする際のメールアドレスもしくは電話番号です。
        password : str
            ログインする際のパスワードです。

        Raises
        ------
        LoginFailureException"""
        session = requests.session()
        
        res = session.post(
            "https://secure.nicovideo.jp/secure/login?site=niconico",
            params={
                "mail": mail,
                "password": password
            })
        
        if res.headers.get("x-niconico-authflag") == ('1' or '3'):
            self.cookies = Cookies.from_string(session.cookies.get("user_session"))
            return self
        else:
            title_ptn = re.compile('<title>(.*?)</title>')
            title = title_ptn.search(res.text)
            if title:
                if "2段階認証" in title.group(1):
                    raise LoginFailureException("Two-step verification is not supported.")
        raise LoginFailureException("Login failed.")
