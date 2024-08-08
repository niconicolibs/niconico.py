"""This module provides a class that represents a video client."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from niconico.base.client import BaseClient
from niconico.objects.nvapi import MylistData, NvAPIResponse, SeriesData, TagsData, VideosData

if TYPE_CHECKING:
    from niconico.objects.video import EssentialVideo, Mylist, Tag


class VideoClient(BaseClient):
    """A class that represents a video client."""

    def get_video(self, video_id: str) -> EssentialVideo | None:
        """Get a video by its ID.

        Args:
            video_id (str): The ID of the video.

        Returns:
            EssentialVideo | None: The video object if found, None otherwise.
        """
        res = self.niconico.get("https://nvapi.nicovideo.jp/v1/videos?watchIds=" + video_id)
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[VideosData](**res.json())
            if res_cls.data is not None and len(res_cls.data.items) >= 1:
                return res_cls.data.items[0].video
        return None

    def get_video_tags(self, video_id: str) -> list[Tag] | None:
        """Get the tags of a video by its ID.

        Args:
            video_id (str): The ID of the video.

        Returns:
            list[Tag] | None: The tags of the video if found, None otherwise.
        """
        res = self.niconico.get("https://nvapi.nicovideo.jp/v1/videos/" + video_id + "/tags")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[TagsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.tags
        return None

    def get_mylist(self, mylist_id: str) -> Mylist | None:
        """Get a mylist by its ID.

        Args:
            mylist_id (str): The ID of the mylist.

        Returns:
            Mylist | None: The mylist object if found, None otherwise.
        """
        res = self.niconico.get("https://nvapi.nicovideo.jp/v2/mylists/" + mylist_id)
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[MylistData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.mylist
        return None

    def get_series(self, series_id: str) -> SeriesData | None:
        """Get a series by its ID.

        Args:
            series_id (str): The ID of the series.

        Returns:
            SeriesData | None: The series object if found, None otherwise.
        """
        res = self.niconico.get("https://nvapi.nicovideo.jp/v1/series/" + series_id)
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[SeriesData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None
