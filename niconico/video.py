# niconico.py - Video

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

from .objects.video import EasyComment, Tag, VideoOwner, Video as AbcVideo, MyList as AbcMyList

if TYPE_CHECKING:
    from .niconico import Response


__all__ = ("HEADERS", "Video", "Client")
BASES = {
    "heartbeat": "https://api.dmc.nico/api/sessions"
}
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
    },
    "mylist": {
        'Accept': '*/*',
        'Accept-Language': 'ja',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'nvapi.nicovideo.jp',
        'Origin': 'https://www.nicovideo.jp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://www.nicovideo.jp/',
        'X-Frontend-Id': '6',
        'X-Niconico-Language': 'ja-jp',
        'X-Frontend-Version': '0',
    },
    "heartbeat": {
        "Host": "api.dmc.nico",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Microsoft Edge";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        "Accept": "application/json",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
        "sec-ch-ua-platform": "Windows",
        "Origin": "https://www.nicovideo.jp",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.nicovideo.jp/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7"
    },
    "heartbeat_first": {
        "Host": "api.dmc.nico",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
        "Origin": "https://www.nicovideo.jp",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.nicovideo.jp/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7"
    }
}
"リクエストに使用されるヘッダーが入っている定数です。"


class Video(DictFromAttribute):
    """ニコニコ動画のデータを含めるクラスです。
    動画をダウンロードすることができます。
    普通はこのクラスをインスタンスは :meth:`niconico.video.Client.get_video` を使って作ります。

    Parameters
    ----------
    client : Client
        動画クライアントクラスのインスタンスです。
    url : str
        取得する動画のURLです。
    data : dict
        動画の辞書形式のデータです。  
        属性からこのデータにアクセスすることができます。"""

    easyComment: EasyComment
    "簡易コメントデータです。"
    tag: Tag
    "動画についているタグです。"
    video: AbcVideo
    "動画のデータです。"
    owner: Optional[VideoOwner]
    "動画の投稿者です。"
    thread: Optional[Thread] = None
    "ハートビートを動かすスレッドです。"
    url: str
    "動画のURLです。"
    client: Client
    "動画取得用のクライアントのインスタンスです。"

    def __init__(self, client: Client, url: str, data: dict):
        self.client, self.url, self.__data__ = client, url, data
        self._heartbeat_running = Event()
        self._download_log: Optional[Callable[[Any], None]] = None
        super().__init__(self.__data__, self)

    def __str__(self) -> str:
        return f"<Video Title={self.__data__['video']['title']} Heartbeat={self.is_heartbeat_running}>"

    def log(self, type_: str, content: str, *args, **kwargs):
        """:meth:`niconico.base.BaseClient.log` を使用してログ出力をします。
        出力するログに動画クラスを文字列化したものを含めます。
        開発者のための関数です。

        Parameters
        ----------
        type_ : str
            ``info`` 等
        content : str
        *args
        **kwargs"""
        content += " (%s)" % self.__str__()
        return self.client.log(type_, content, *args, **kwargs)

    @property
    def is_heartbeat_running(self) -> bool:
        "ハートビートが動いているかです。"
        return self._heartbeat_running.is_set()

    def connect(self):
        """ハートビートを動かして動画データを取得することが可能な状態にします。

        Notes
        -----
        ハートビートは定期的にニコニコ動画と通信を行うもので別スレッドで動かされます。
        動画使用後には :meth:`niconico.video.Video.close` を実行してハートビートを停止させてください。
        また、 ``with`` 構文を使用すればこの関数と :meth:`niconico.video.Video.close` を省略することができます。"""
        self.thread = Thread(target=self._heartbeat)
        self.thread.start()
        self._heartbeat_running.wait()
        self.client.log("info", "ハートビートを開始しました。")

    def close(self):
        "ハートビートを停止します。"
        self.client.log("info", "ハートビートを停止させました。")
        self._heartbeat_running.clear()
        self.thread.join()

    def __enter__(self):
        if not self.is_heartbeat_running:
            self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.is_heartbeat_running:
            self.close()

    def _assert_heartbeat(self):
        assert self.is_heartbeat_running, "ハートベートが動いていません。"

    @property
    def download_link(self) -> str:
        """動画のダウンロードリンクを取得します。

        Notes
        -----
        これを実行する際は :meth:`niconico.video.Video.connect` でハートビートを動かす必要があります。
        また、これで取得するダウンロードリンクはハートビートが動いている状態でなければ使うことができません。

        Raises
        ------
        AssertionError : ハートビートが動いていない際に発生します。"""
        self._assert_heartbeat()
        return self.session["content_uri"]

    def download(self, path: str, load_chunk_size: int = 1024) -> None:
        """動画をダウンロードします。

        Parameters
        ----------
        path : str
            動画ファイルの保存先です。
        load_chunk_size : int, default 1024
            一度にダウンロードする量です。

        Notes
        -----
        これを実行する際には :meth:`niconico.video.Video.connect` でハートビートを動かす必要があります。

        Raises
        ------
        AssertionError : ハートビートが動いていない際に発生します。"""
        self._assert_heartbeat()
        headers = HEADERS["normal"].copy()
        headers["Content-Type"] = "video/mp4"

        # ファイルサイズを取得する。
        size = int(
            self.client.niconico.request(
                "head", self.download_link, headers=headers, params=(params := (
                    (
                        "ht2_nicovideo",
                        self.session["content_auth"]["content_auth_info"]["value"]
                    ),
                ))
            ).headers["content-length"]
        )

        self.log("info", "ダウンロード中...")
        r = self.client.niconico.request(
            "GET", self.download_link, headers=headers, params=params, stream=True
        )

        now_size = 0
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=load_chunk_size):
                if chunk:
                    now_size += len(chunk)
                    f.write(chunk)
                    if self._download_log is not None:
                        self._download_log(
                            f"ダウンロード済み: {int(now_size/size*100)}% ({now_size}/{size})"
                        )

        self.log("info", "完了")

    def _make_url(self, session_id: str) -> str:
        # Heartbeat用のURLを作る。
        return f"{BASES['heartbeat']}/{session_id}?_format=json&_method=PUT"

    def _heartbeat(self):
        # ハートビート
        self.log("info", "セッションIDを取得中...")
        # セッションIDを取得する。
        self.session = self.client.niconico.request(
            "POST", f"{BASES['heartbeat']}?_format=json",
            headers=HEADERS["heartbeat"], json=self._make_session_data(
                VideoDownloadMode.http_output_download_parameters
            )
        ).json()["data"]["session"]
        self.log("info", "セッションID: %s" % self.session["id"])
        self._heartbeat_running.set()
        # 事前にしておかなければならないリクエストをしておく。
        self.client.niconico.request(
            "OPTIONS", self._make_url(self.session["id"]),
            headers=HEADERS["heartbeat_first"]
        )
        # ここからは定期的に「生きているよ」のメッセージを送ります。
        after = self._get_interval(time(), {"session": self.session})
        while self._heartbeat_running.is_set():
            now = time()
            if now < after:
                sleep(0.05)
                continue
            data = {"session": self.session}
            # 「生きているよ」リクエストをする。
            self.session = self.client.niconico.request(
                "POST", self._make_url(self.session["id"]),
                json=data, headers=HEADERS["heartbeat"]
            ).json()["data"]["session"]
            self.log("info", "ハートビートを送信しました。")
            self.log("debug", f"レスポンス: {self.session}")
            after = self._get_interval(now, data)

    def _get_interval(self, now: float, data: dict) -> float:
        # ハートビートのインターバルを取得します。
        return now + data["session"]["keep_method"]["heartbeat"]["lifetime"] / 1000 - 3

    def _make_session_data(self, mode: VideoDownloadMode):
        # セッション用のデータを作る。
        # TODO: このセッションデータの画質設定等を解析してできればもっと細かく設定できるようにする。
        session = self.__data__["media"]["delivery"]["movie"]["session"].copy()
        data: dict[Any, Any] = {}

        data["content_type"] = "movie"
        data["content_src_id_sets"] = [{"content_src_ids": []}]
        data["content_src_id_sets"][0]["content_src_ids"].append({
            "src_id_to_mux": {
                "video_src_ids": session["videos"],
                "audio_src_ids": session["audios"]
            }
        })
        data["timing_constraint"] = "unlimited"
        data["keep_method"] = {
            "heartbeat": {
                "lifetime": session["heartbeatLifetime"]
            }
        }
        data["recipe_id"] = session["recipeId"]
        data["priority"] = session["priority"]
        parameters = {
            VideoDownloadMode.http_output_download_parameters.name: {
                "use_well_known_port": "yes" if session["urls"][0]["isWellKnownPort"] else "no",
                "use_ssl": "yes" if session["urls"][0]["isSsl"] else "no",
                "transfer_preset": ""
            }
        }
        data["protocol"] = {
            "name": "http",
            "parameters": {
                "http_parameters": {
                    "parameters": parameters
                }
            }
        }
        data["content_uri"] = ""
        data["session_operation_auth"] = {
            "session_operation_auth_by_signature": {
                "token": session["token"],
                "signature": session["signature"]
            }
        }
        data["content_id"] = session["contentId"]
        data["content_auth"] = {
            "auth_type": session["authTypes"]["http"],
            "content_key_timeout": session["contentKeyTimeout"],
            "service_id": "nicovideo",
            "service_user_id": str(session["serviceUserId"])
        }
        data["client_info"] = {
            "player_id": session["playerId"]
        }
        del session

        return {"session": data}


class Client(BaseClient):
    """ニコニコ動画用のクライアントです。
    普通 :class:`niconico.niconico.NicoNico` から使います。"""

    def get_video(self, url: str) -> Video:
        """ニコニコ動画から指定された動画を取得します。

        Parameters
        ----------
        url : str
            動画のURLです。。

        Raises
        ------
        ExtractFailed"""
        # 短縮やスマホ用のURLであれば元に戻す。
        if "nico.ms" in url:
            url = url.replace("nico.ms/", "www.nicovideo.jp/watch/")
        url = parse_link(url)

        # 動画情報を取得する。
        data = BeautifulSoup(
            self.niconico.request("GET", url, headers=HEADERS["normal"]).text, "html.parser"
        ).find(
            "div", {"id": "js-initial-watch-data"}
        ).get("data-api-data")
        video = Video(self, url, data)

        if data:
            video.__data__ = loads(data)
            return video
        else:
            raise ExtractFailed("ニコニコ動画から情報を取得するのに失敗しました。")

    def get_mylist(self, url: str) -> Iterator[AbcMyList]:
        """マイリストのデータを取得します。

        Parameters
        ----------
        url : str
            マイリストのURLです。

        Notes
        -----
        ニコニコ動画のマイリストは複数ページにわたる場合があります。  
        なので100ページずつ取得していきます。  
        よって返される各マイリストには百ページ分動画の情報が入っています。"""
        url = parse_link(url)
        mylist = False
        for code in url.split("/"):
            if code == "mylist":
                mylist = True
            elif mylist:
                self.log("info", "取得中...")
                before, page = None, 0
                while before is None or before.hasNext:
                    page += 1
                    data = self.niconico.request(
                        "GET", f"https://nvapi.nicovideo.jp/v2/mylists/{code}",
                        headers=HEADERS["mylist"], params=(("pageSize", 100), ("page", page))
                    ).json()
                    self.log("info", "マイリストの%sページ目のデータを取得しました。" % page)
                    yield (before := AbcMyList(data["data"]["mylist"], self))
                break
        else:
            raise ValueError("URLが適切ではありません。")