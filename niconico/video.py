# niconico.py - Video

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn, Union, Any

from threading import Thread

from bs4 import BeautifulSoup
from json import loads

from .base import DictFromAttribute, BaseClient
from .exceptions import ExtractFailed
from .enums import VideoDownloadMode
from .niconico import Response

from .types.video import EasyComment, Tag, Video as VideoType


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
    }
}


class Video(DictFromAttribute):
    """ニコニコ動画のデータを含めるクラスです。
    動画をダウンロードすることができます。"""

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

    @property
    def is_heartbeat_running(self) -> bool:
        return self._heartbeat_running.is_set()

    def get_download_link(self):
        """ダウンロードリンクを取得します。
        そしてこれを実行するにはハードビートを動かしている必要があります。
        ですので、これを実行する際は :meth:`niconico.video.Video.connect` を実行してください。
        そしてダウンロードリンクの使用が終了したら :meth:`niconico.video.Video.close` を実行してください。

        Warnings
        --------
        ダウンロードリンクはハートビートが動いている状態のみ使用可能です。"""

    def connect(self):
        """ハートビートを動かして動画データを取得することが可能な状態にします。

        Notes
        -----
        ハートビートは定期的にニコニコ動画と通信を行うもので別スレッドで動かされます。
        動画使用後には :meth:`niconico.video.Video.close` を実行してスレッドを停止させてください。"""
        self.thread.start()
        self.client.log("info", "Started heartbeat")

    def close(self):
        "ハートビートを停止します。"
        self.client.log("info", "Closing heartbeat")
        self._heartbeat_running.clear()
        self.thread.join()

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
        ...

    def _make_session_data(self, mode: VideoDownloadMode):
        # セッション用のデータを作る。
        # TODO: このセッションデータの画質設定等を解析してできればもっと細かく設定できるようにする。
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
    "ニコニコ動画用のクライアントです。"

    def get_video(self, url: str, headers: dict[str, str] = HEADERS["normal"]) -> Union[Video, NoReturn]:
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
        if "nico.ms" in url:
            url = url.replace("nico.ms/", "www.nicovideo.jp/watch/")
        if "sp" in url:
            url = url.replace("sp", "www")

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

    def log(self, type_: str, content: str, *args, **kwargs):
        content += " (%s)" % self.__str__()
        return super().log(type_, content, *args, **kwargs)
