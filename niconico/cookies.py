# niconico.py - Cookies

from typing import Optional

from http.cookies import SimpleCookie

from datetime import datetime, timedelta
from time import time


__all__ = ("Cookies",)
FORMAT = "%a, %d-%b-%Y %X"


class Cookies(SimpleCookie):
    @classmethod
    def from_file(cls, path: str):
        """Netscapeのクッキーファイルフォーマットに準拠したテキストファイルからクッキーが格納されたクラスを作成します。  
        なので、ChromeやEdgeで使用可能な `Get cookies.txt <https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid>`_ のような拡張機能を使って作ったクッキーのテキストファイルを読み込むことができます。
        もし自分のアカウントでニコニコ動画のコンテンツを取得したい場合はこれを使用しましょう。

        Parameters
        ----------
        path : str
            クッキーのファイルのパスです。

        Raises
        ------
        FileNotFoundError"""
        with open(path, "r") as f:
            raw = f.read()
        cookies = cls()
        for item in map(
            lambda x: x.split(), filter(
                lambda x: x and x[0] != "#", raw.splitlines()
            )
        ):
            cookies[item[5]] = item[6]
            for index, key in enumerate(
                ("domain", None, "path", "secure", "expires")
            ):
                if key:
                    cookies[item[5]][key] = (
                        datetime.fromtimestamp(float(item[index])).strftime(FORMAT)
                        if key == "expires" else item[index]
                    )
        return cookies

    @classmethod
    def guest(cls, nicosid: Optional[str] = None):
        """ニコニコのゲストアカウントのクッキーを生成します。  

        Notes
        -----
        これはニコニコ動画にアクセスして作成するクッキーではなく、開発者がクッキーを見て予想して作った再現物です。"""
        cookies = cls()
        cookies["nicosid"] = nicosid or str(time())
        for key, value in (
            ("domain", ".nicovideo.jp"), ("path", "/"),
            ("expires", (datetime.now() + timedelta(days=365)).strftime(FORMAT))
        ):
            cookies["nicosid"][key] = value
        return cookies