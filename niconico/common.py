# niconico.py - Common

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Iterator, Union, Optional, Any

from bs4 import BeautifulSoup
from json import loads, dumps

from .base import DictFromAttribute, BaseClient
from .exceptions import ExtractFailed

from .objects.niconico import User as AbcUser

if TYPE_CHECKING:
    from .niconico import Response


__all__ = ("HEADERS", "User", "Client")
HEADERS = {
    "normal": {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Accept-Language': 'ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'X-Frontend-Id': '6',
        'X-Niconico-Language': 'ja-jp',
        'X-Frontend-Version': '0',
    }
}
"リクエストに使用されるヘッダーが入っている定数です。"


class User():
    """ニコニコのアカウントデータを含めるクラスです。
    普通はこのクラスをインスタンスは :meth:`niconico.common.Client.get_user` を使って作ります。"""

    user: AbcUser
    "ユーザーのデータです。"
    client: Client
    "情報取得用のクライアントのインスタンスです。"

    def __init__(self, client: Client, data: dict):
        self.client = client
        self.user = AbcUser(data, client)


class Client(BaseClient):
    """ニコニコサービス全体のクライアントです。
    普通 :class:`niconico.niconico.NicoNico` から使います。"""

    def get_user(self, id: int) -> User:
        """ニコニコのアカウント情報を取得します。

        Parameters
        ----------
        id : int
            アカウントのIDです。

        Raises
        ------
        ExtractFailed"""
        
        # 動画情報を取得する。
        data = BeautifulSoup(
            self.niconico.request("GET", f"https://www.nicovideo.jp/user/{id}", headers=HEADERS["normal"]).text, "html.parser"
        ).find(
            "div", {"id": "js-initial-userpage-data"}
        ).get("data-initial-data")

        if data:
            user = User(self, loads(data)["userDetails"]["userDetails"]["user"])
            return user
        else:
            raise ExtractFailed("ニコニコから情報を取得するのに失敗しました。")