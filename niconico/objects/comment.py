# niconico.py - Comment

from typing import TYPE_CHECKING, TypedDict, Literal, Optional, List, Any
from niconico.base import DictFromAttribute


__all__ = (
    "Comments", "MovieComment"
)


class MovieChat(DictFromAttribute):
    "コメントデータです。"

    thread: str
    "スレッドのIDです。"
    no: int
    "コメント番号です。"
    vpos: int
    "コメントが投稿された場所です。"
    date: int
    "コメントが投稿された日時です。"
    nicoru: Optional[int] = 0,
    "ニコられた数です。"
    premium: Optional[int] = 0,
    "プレミアムかどうかです。"
    anonymity: int
    "匿名アカウントかどうかです。"
    date_usec: Optional[int] = 0,
    "コメントが投稿された日時のミリ秒数です。"
    score: Optional[int] = 0,
    "コメントのNG共有スコアの値です。"
    user_id: str
    "コメント投稿者のユーザーIDです。"
    mail: str
    "指定されたコマンドです。"
    content: str
    "コメント内容です。"


class Comments():
    "動画のコメントデータです。"

    thread: str
    "スレッドのIDです。"
    fork: int
    "コメントの種類です。"
    count: int
    "投稿されたコメント数です。"
    last_res: Optional[int] = 0
    "取得したものの最新のコメント番号です。"
    num_res: int
    "全サーバー合計のコメント数です。"
    ticket: str
    "コメント投稿をする際のチケットです。"
    items: List[MovieChat]
    "コメントデータのリストです。"

    def __init__(self, data: dict):
        self.__data__ = data
        super().__init__(self.__data__, self)