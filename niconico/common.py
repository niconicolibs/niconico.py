# niconico.py - Common

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Iterator, Union, Optional, Any

from threading import Thread, Event
from time import time, sleep

from bs4 import BeautifulSoup
from json import loads

from .base import DictFromAttribute, BaseClient
from .exceptions import ExtractFailed
from .enums import VideoDownloadMode
from .utils import parse_link

from .objects.niconico import User as AbcUser

if TYPE_CHECKING:
    from .niconico import Response


__all__ = ("User", "Client")


class User(AbcUser):
    """ニコニコのアカウントデータを含めるクラスです。
    普通はこのクラスをインスタンスは :meth:`niconico.common.Client.get_user` を使って作ります。"""


class Client(BaseClient):
    """ニコニコサービス全体のクライアントです。
    普通 :class:`niconico.niconico.NicoNico` から使います。"""

    def get_user(self, id: int) -> User:
        """ニコニコのアカウント情報を取得します。

        Parameters
        ----------
        id : int
            アカウントのIDです。"""
        
        