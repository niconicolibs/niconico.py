# niconico.py - Video

from typing import TYPE_CHECKING, NoReturn, Union

from threading import Thread

from bs4 import BeautifulSoup

from .base import DictFromAttribute, BaseClient
from .exceptions import ExtractFailed
from .headers import Headers, VIDEO
from ._json import loads, dumps
from .utils import request

from .types.video import EasyComment, Tag, Video as VideoType


class Video(DictFromAttribute):

    if TYPE_CHECKING:
        easyComment: EasyComment
        tag: Tag
        video: VideoType

    def __init__(self, client: "Client", url: str, data: dict):
        self.client, self.url, self.data = client, url, data
        super().__init__(self.data)

    def get_download_link(self):
        ...

    def _heartbeat(self):
        ...


class Client(BaseClient):
    def get_video(self, url: str, headers: Headers = VIDEO) -> Union[Video, NoReturn]:
        """Get video data from Nico Nico Video.

        Parameters
        ----------
        headers : Headers, default VIDEO
            Headers to be used when making a request.

        Returns
        -------
        data : dict
            Video data

        Raises
        ------
        ExtractFailed"""
        if "nico.ms" in url:
            url = url.replace("nico.ms/", "www.nicovideo.jp/watch/")
        if "sp" in url:
            url = url.replace("sp", "www")

        data = BeautifulSoup(
            self.client.request(
                "get", url, headers=headers, cookies=self.cookies
            ).text, "html.parser"
        ).find(
            "div", {"id": "js-initial-watch-data"}
        ).get("data-api-data")
        video = Video(self, url, data)

        if data:
            video.data = loads(data)
            return video
        else:
            raise ExtractFailed("ニコニコ動画から情報を取得するのに失敗しました。")