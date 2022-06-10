# niconico.py - Common

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Iterator, Union, Optional, Any

from bs4 import BeautifulSoup
from json import loads

from .base import DictFromAttribute, BaseClient
from .exceptions import ExtractFailed

from .objects.video import MyList as AbcMyList, VideoSortKey, AbcVideo
from .objects.niconico import User as AbcUser, AbcUser as AbcAbcUser

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

    def get_followers(self, num: Optional[int] = 1000, page: Optional[int] = 1) -> Iterator[AbcUser]:
        """ユーザーのフォロワーを取得します。

        Parameters
        ----------
        num : int, default 100
            取得する上限値です。
        page : int, default 1
            合計数を上限値で割ったときの何ページ目を表示するかです。

        Raises
        ------
        ExtractFailed"""
        
        r = self.client.niconico.request(
            "GET", f"https://nvapi.nicovideo.jp/v1/users/{id}/followed-by/users?pageSize={num}&page={page}", headers=HEADERS["normal"]
        ).json()

        for user in r["data"]["items"]:
            yield AbcAbcUser(user, self)
    
    def get_followees(self, num: Optional[int] = 1000, page: Optional[int] = 1) -> Iterator[AbcUser]:
        """ユーザーがフォローしているユーザーを取得します。

        Parameters
        ----------
        num : int, default 100
            取得する上限値です。
        page : int, default 1
            合計数を上限値で割ったときの何ページ目を表示するかです。

        Raises
        ------
        ExtractFailed"""
        
        r = self.client.niconico.request(
            "GET", f"https://nvapi.nicovideo.jp/v1/users/{id}/following/users?pageSize={num}&page={page}", headers=HEADERS["normal"]
        ).json()

        for user in r["data"]["items"]:
            yield AbcAbcUser(user, self)
    
    def get_mylists(self) -> Iterator[AbcMyList]:
        """ユーザーのマイリストを取得します。

        Raises
        ------
        ExtractFailed"""
        
        r = self.client.niconico.request(
            "GET", f"https://nvapi.nicovideo.jp/v1/users/{id}/mylists", headers=HEADERS["normal"]
        ).json()

        for mr in r["data"]["mylists"]:
            yield AbcMyList(mr, self)
    
    def get_movies(
            self, num: Optional[int] = 100, page: Optional[int] = 1,
            sortKey: Optional[str] = VideoSortKey.registeredAt,
            sortOrder: Optional[str] = "desc") -> Iterator[AbcVideo]:
        """ユーザーのマイリストを取得します。

        Parameters
        ----------
        num : int, default 100
            取得する上限値です。
        page : int, default 1
            合計数を上限値で割ったときの何ページ目を表示するかです。
        sortKey : str, default VideoSortKey.registeredAt
            動画のソート方法です。VideoSortKey列挙型でも指定できます。
        sortOrder : str, default desc
            ソートが降順(desc)か昇順(asc)かを指定します。

        Raises
        ------
        ExtractFailed"""
        
        r = self.client.niconico.request(
            "GET", f"https://nvapi.nicovideo.jp/v1/users/{id}/videos"\
                f"?pageSize={num}&page={page}&sortKey={sortKey}&sortOrder={sortOrder}",
            headers=HEADERS["normal"]
        ).json()

        for v in r["data"]["items"]:
            yield AbcVideo(v, self)
    
    def is_following(self, id: int) -> bool:
        """指定したユーザーをフォローしているかを返します。

        Parameters
        ----------
        id : int
            ユーザーIDです。"""
        
        r = self.client.niconico.request(
            "GET",
            f"https://user-follow-api.nicovideo.jp/v1/user/followees/niconico-users/{id}.json",
            headers=HEADERS["normal"]
        ).json()

        return r["data"]["following"]


class Client(BaseClient):
    """ニコニコサービス全体のクライアントです。
    普通 :class:`niconico.niconico.NicoNico` から使います。"""

    def get_user(self, id: str) -> User:
        """ニコニコのアカウント情報を取得します。

        Parameters
        ----------
        id : str
            アカウントのIDです。

        Raises
        ------
        ExtractFailed"""
        
        r = self.niconico.request(
            "GET", f"https://nvapi.nicovideo.jp/v1/users/{id}", headers=HEADERS["normal"]
        ).json()
        return User(self, r["data"]["user"])
    
    def get_own(self) -> User:
        """ログインしているアカウント情報を取得します。

        Raises
        ------
        ExtractFailed"""

        return self.get_user("me")
        

#TODO
"""
user.is_followee(id)
"""