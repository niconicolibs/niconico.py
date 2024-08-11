"""This module provides a client for watching videos on Niconico."""

from __future__ import annotations

import re
import secrets
import string
import subprocess
import time
from pathlib import Path

import requests

from niconico.base.client import BaseClient
from niconico.decorators import login_required
from niconico.exceptions import DownloadError, NicoAPIError, WatchAPIError
from niconico.objects.video.nvapi import AccessRightsData, NvAPIResponse
from niconico.objects.video.watch import (
    NvCommentAPIData,
    NvCommentAPIResponse,
    StoryboardResponse,
    WatchAPIData,
    WatchAPIErrorData,
    WatchAPIResponse,
    WatchData,
)


class VideoWatchClient(BaseClient):
    """A client for watching videos on Niconico."""

    def get_watch_data(self, video_id: str) -> WatchData:
        """Get the watch data of a video.

        Args:
            video_id: The ID of the video.

        Returns:
            WatchData | WatchResponseError: The watch data of the video if successful, WatchResponseError
        """
        res = self.niconico.get(f"https://www.nicovideo.jp/watch/{video_id}?responseType=json")
        if res.status_code == requests.codes.ok:
            res_cls_data = WatchAPIResponse[WatchAPIData](**res.json())
            return res_cls_data.data.response
        res_cls_error = WatchAPIResponse[WatchAPIErrorData](**res.json())
        raise WatchAPIError(response=res_cls_error.data.response)

    def generate_action_track_id(self) -> str:
        """Generate a random action track ID.

        Returns:
            str: The generated action track ID.
        """
        fh_chars = string.ascii_letters + string.digits
        fh = "".join(secrets.choice(fh_chars) for _ in range(10))
        lh = int(time.time() * 1000)
        return f"{fh}_{lh}"

    def get_outputs(self, watch_data: WatchData) -> dict[str, list[str]]:
        """Get the outputs of a video.

        Args:
            watch_data: The watch data of the video.

        Returns:
            dict[str, list[str]]: The outputs of the video.
        """
        outputs: dict[str, list[str]] = {}
        top_audio_id = None
        top_audio_quality = -1
        for audio in watch_data.media.domand.audios:
            if audio.is_available and audio.quality_level > top_audio_quality:
                top_audio_id = audio.id_
                top_audio_quality = audio.quality_level
        if top_audio_id is None:
            return outputs
        for video in watch_data.media.domand.videos:
            if video.is_available:
                outputs[video.label] = [video.id_, top_audio_id]
        return outputs

    def get_hls_content_url(self, watch_data: WatchData, outputs: list[list[str]]) -> str | None:
        """Get the HLS content URL of a video.

        Args:
            watch_data: The watch data of the video.
            outputs: The outputs. e.g.: [video_id, audio_id][]

        Returns:
            str | None: The HLS content URL of the video if successful, None otherwise.
        """
        video_id = watch_data.client.watch_id
        action_track_id = watch_data.client.watch_track_id
        access_right_key = watch_data.media.domand.access_right_key
        res = self.niconico.post(
            f"https://nvapi.nicovideo.jp/v1/watch/{video_id}/access-rights/hls?actionTrackId={action_track_id}",
            json={"outputs": outputs},
            headers={"X-Access-Right-Key": access_right_key},
        )
        if res.status_code == requests.codes.created:
            res_cls = NvAPIResponse[AccessRightsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.content_url
        return None

    @login_required(premium=True)
    def get_storyboard_url(self, watch_data: WatchData) -> str | None:
        """Get the storyboards URL of a video.

        Args:
            watch_data: The watch data of the video.

        Returns:
            str | None: The storyboards URL of the video if successful, None otherwise.
        """
        if not watch_data.media.domand.is_storyboard_available:
            return None
        video_id = watch_data.client.watch_id
        action_track_id = watch_data.client.watch_track_id
        access_right_key = watch_data.media.domand.access_right_key
        res = self.niconico.post(
            f"https://nvapi.nicovideo.jp/v1/watch/{video_id}/access-rights/storyboard?actionTrackId={action_track_id}",
            headers={"X-Access-Right-Key": access_right_key},
        )
        if res.status_code == requests.codes.created:
            res_cls = NvAPIResponse[AccessRightsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.content_url
        return None

    @login_required(premium=True)
    def download_storyboards(self, watch_data: WatchData, path: str) -> None:
        """Download the storyboards of a video.

        Args:
            watch_data: The watch data of the video.
            path: The folder path to save the storyboards.
        """
        storyboard_url = self.get_storyboard_url(watch_data)
        if storyboard_url is None:
            raise NicoAPIError(message="Failed to get the storyboards URL.")
        res = self.niconico.get(storyboard_url)
        if res.status_code == requests.codes.ok:
            res_cls = StoryboardResponse(**res.json())
            if not Path(path).is_dir():
                Path(path).mkdir(parents=True)
            if Path(f"{path}/storyboard.json").exists():
                raise DownloadError(message="The storyboard.json file already exists.")
            with Path(f"{path}/storyboard.json").open(mode="w") as f:
                f.write(res.text)
            for image in res_cls.images:
                image_res = self.niconico.get(re.sub(r"(?<=/)[^/]+(?=\?)", image.url, storyboard_url))
                if image_res.status_code == requests.codes.ok:
                    if Path(f"{path}/{image.url}.jpg").exists():
                        raise DownloadError(message=f"The storyboard image already exists: {image.url}")
                    with Path(f"{path}/{image.url}.jpg").open(mode="wb") as f:
                        f.write(image_res.content)
                else:
                    raise DownloadError(message=f"Failed to download the storyboard image: {image.url}")
        else:
            raise DownloadError(message="Failed to download the storyboards.")

    def download_video(self, watch_data: WatchData, output_label: str, path: str) -> str:
        """Download a video.

        Args:
            watch_data: The watch data of the video.
            output_label: The output label of the video.
            path: The folder path to save the video.

        Returns:
            str: The path of the downloaded video.
        """
        outputs = self.get_outputs(watch_data)
        if output_label not in outputs:
            raise DownloadError(message="The output label is not available.")
        hls_content_url = self.get_hls_content_url(watch_data, [outputs[output_label]])
        if hls_content_url is None:
            raise NicoAPIError(message="Failed to get the HLS content URL.")
        name = f"{watch_data.video.id_}_{watch_data.video.title}.mp4"
        if not Path(path).is_dir():
            Path(path).mkdir(parents=True)
        if (Path(path) / name).exists():
            raise DownloadError(message="The video file already exists.")
        cookies = {
            "domand_bid": self.niconico.session.cookies.get("domand_bid"),
        }
        commands = " ".join(
            [
                "ffmpeg",
                "-headers",
                f"'cookie: {';'.join(f'{k}={v}' for k, v in cookies.items())}'",
                "-protocol_whitelist",
                "file,http,https,tcp,tls,crypto",
                "-i",
                f"'{hls_content_url}'",
                "-c",
                "copy",
                f"'{(Path(path) / name).as_posix()}'",
            ],
        )
        try:
            with subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True) as p:  # noqa: S602
                p.wait()
        except subprocess.CalledProcessError as e:
            raise DownloadError(message="Failed to download the video.") from e
        return (Path(path) / name).as_posix()

    def get_comments(self, watch_data: WatchData, *, when: int | None = None) -> NvCommentAPIData | None:
        """Get the comments of a video.

        Args:
            watch_data: The watch data of the video.
            when: The time to get the comments.

        Returns:
            list[Any]: The comments of the video.
        """
        payload = {
            "threadKey": watch_data.comment.nv_comment.thread_key,
            "params": watch_data.comment.nv_comment.params.model_dump_json(by_alias=True),
            "additionals": {},
        }
        if when is not None:
            if self.niconico.premium:
                payload["additionals"] = {"when": when}
            else:
                raise NicoAPIError(message="You must be a premium member to get the comments at a specific time.")
        res = self.niconico.post(watch_data.comment.nv_comment.server + "/v1/threads", json=payload)
        if res.status_code == requests.codes.ok:
            res_cls = NvCommentAPIResponse(**res.json())
            if res_cls.meta.status == requests.codes.ok:
                return res_cls.data
        return None
