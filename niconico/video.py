# niconico.py - Video

from __future__ import annotations

from typing import TYPE_CHECKING, Union, Any

from threading import Thread, Event
from time import time, sleep

from bs4 import BeautifulSoup
from json import loads

from .base import DictFromAttribute, BaseClient
from .exceptions import ExtractFailed
from .enums import VideoDownloadMode

from .types.video import EasyComment, Tag, Video as VideoType

if TYPE_CHECKING:
    from .niconico import Response


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
        動画の辞書形式のデータです。"""

    if TYPE_CHECKING:
        easyComment: EasyComment
        tag: Tag
        video: VideoType

    def __init__(self, client: Client, url: str, data: dict):
        self.client, self.url, self.data = client, url, data
        self.thread = Thread(target=self._heartbeat)
        self._heartbeat_running = Event()
        super().__init__(self.data)

    def __str__(self) -> str:
        return f"<Video Title={self.data['video']['title']} Heartbeat={self.is_heartbeat_running}>"

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
        return self._heartbeat_running.is_set()

    def connect(self):
        """ハートビートを動かして動画データを取得することが可能な状態にします。

        Notes
        -----
        ハートビートは定期的にニコニコ動画と通信を行うもので別スレッドで動かされます。
        動画使用後には :meth:`niconico.video.Video.close` を実行してハートビートを停止させてください。
        また、`with`構文を使用すればこの関数と :meth:`niconico.video.Video.close` を省略することができます。"""
        self.thread.start()
        self._heartbeat_running.wait()
        self.client.log("info", "Started heartbeat")

    def close(self):
        "ハートビートを停止します。"
        self.client.log("info", "Closing heartbeat")
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

    def get_download_link(self) -> str:
        """動画のダウンロードリンクを取得します。

        Notes
        -----
        これを実行する際は :meth:`niconico.video.Video.connect` でハートビートを動かす必要があります。
        また、これで取得するダウンロードリンクはハートビートが動いている状態でなければ使うことができません。

        Raises
        ------
        AssertionError : ハートビートが動いていない際に発生します。"""
        self._assert_heartbeat()
        self._download_link = self.session["content_uri"]
        return self._download_link

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
            self.niconico.request(
                "head", self._download_link, headers=headers, params=(params := (
                    (
                        "ht2_nicovideo",
                        self.result_data["content_auth"]["content_auth_info"]["value"]
                    ),
                ))
            ).headers.get("content-length")
        )

        self.log("info", "Downloading...")
        r = self.client.niconico.request(
            "GET", self.get_download_link(), headers=headers, params=params, stream=True
        )

        now_size = 0
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=load_chunk_size):
                if chunk:
                    now_size += len(chunk)
                    f.write(chunk)
                    self.log("debug", f"Downloaded: {int(now_size/size*100)}% ({now_size}/{size})")

        self.log("info", "Done")

    def _make_url(self, session_id: str) -> str:
        # Heartbeat用のURLを作る。
        return f"{BASES['heartbeat']}/{session_id}?_format=json&_method=PUT"

    def _heartbeat(self):
        # ハートビート
        self.log("info", "Send the initial heartbeat data to get session id")
        # セッションIDを取得する。
        self.session = self.client.niconico.request(
            "POST", f"{BASES['heartbeat']}?_format=json",
            headers=HEADERS["heartbeat"], json=self._make_session_data(
                VideoDownloadMode.http_output_download_parameters
            )
        ).json()["data"]["session"]
        self.log("info", "Session ID: %s" % self.session["id"])
        self._heartbeat_running.set()
        # 事前にしておかなければならないリクエストをしておく。
        self.client.niconico.request(
            "OPTIONS", self._make_url(self.session["id"]),
            headers=HEADERS["heartbeat_first"]
        )
        # ここからは定期的に「生きているよ」のメッセージを送ります。
        after = self._get_interval(before)
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
            self.log("info", "Sent heartbeat")
            self.log("debug", f"Data: {self.session}")
            after = self._get_interval(now, data)

    def _get_interval(self, now: float, data: dict) -> float:
        return now + data["session"]["keep_method"]["heartbeat"]["lifetime"] / 1000 - 3

    def _make_session_data(self, mode: VideoDownloadMode):
        # セッション用のデータを作る。
        # TODO: このセッションデータの画質設定等を解析してできればもっと細かく設定できるようにする。
        print(self.data)
        movie = self.data["media"]["delivery"]
        session = movie["session"]
        data: dict[Any, Any] = {}

        data["content_type"] = "movie"
        data["content_src_id_sets"] = [{"content_src_ids": []}]
        lv, la = len(session["videos"]), len(session["audios"])
        for _ in range(lv if lv >= la else la):
            src_id_to_mux = {
                "src_id_to_mux": {
                    "video_src_ids": session["videos"].copy(),
                    "audio_src_ids": session["audios"].copy()
                }
            }
            data["content_src_id_sets"][0]["content_src_ids"].append(src_id_to_mux)
            for k in ("videos", "audios"):
                if len(session[k]) != 1:
                    session[k].pop(0)
        del src_id_to_mux
        data["timing_constraint"] = "unlimited"
        data["keep_method"] = {
            "heartbeat": {
                "lifetime": session["heartbeatLifetime"]
            }
        }
        data["recipe_id"] = session["recipeId"]
        data["priority"] = session["priority"]
        assert mode is VideoDownloadMode, "動画取得方法の指定方法が違います。"
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
        del session, movie

        return {"session": data}


class Client(BaseClient):
    """ニコニコ動画用のクライアントです。
    普通 :class:`niconico.niconico.NicoNico` から使います。"""

    def get_video(self, url: str, headers: dict[str, str] = HEADERS["normal"]) -> Video:
        """ニコニコ動画から指定された動画を取得します。

        Parameters
        ----------
        headers : Headers, default VIDEO
            リクエストをする際に使用するヘッダーです。

        Returns
        -------
        data : dict
            動画のデータです。

        Raises
        ------
        ExtractFailed"""
        # 短縮やスマホ用のURLであれば元に戻す。
        if "nico.ms" in url:
            url = url.replace("nico.ms/", "www.nicovideo.jp/watch/")
        if "sp" in url:
            url = url.replace("sp", "www")

        # 動画情報を取得する。
        data = BeautifulSoup(
            self.niconico.request(
                "get", url, headers=headers, cookies=self.niconico.cookies
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