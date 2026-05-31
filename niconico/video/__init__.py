"""This module provides a class that represents a video client."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from niconico.base.client import BaseClient
from niconico.decorators import login_required
from niconico.objects.nvapi import HistoryData, MylistData, NvAPIResponse, SeriesData, TagsData, VideosData
from niconico.video.ranking import VideoRankingClient
from niconico.video.search import VideoSearchClient
from niconico.video.watch import VideoWatchClient

if TYPE_CHECKING:
    from niconico.niconico import NicoNico
    from niconico.objects.video import EssentialVideo, Mylist, MylistSortKey, MylistSortOrder, Tag


class VideoClient(BaseClient):
    """A class that represents a video client."""

    ranking: VideoRankingClient
    search: VideoSearchClient
    watch: VideoWatchClient

    def __init__(self, niconico: NicoNico) -> None:
        """Initialize the client."""
        super().__init__(niconico)
        self.ranking = VideoRankingClient(niconico)
        self.search = VideoSearchClient(niconico)
        self.watch = VideoWatchClient(niconico)

    def get_video(self, video_id: str) -> EssentialVideo | None:
        """Get a video by its ID.

        Args:
            video_id (str): The ID of the video.

        Returns:
            EssentialVideo | None: The video object if found, None otherwise.
        """
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/videos?watchIds={video_id}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[VideosData](**res.json())
            if res_cls.data is not None and len(res_cls.data.items) >= 1:
                return res_cls.data.items[0].video
        return None

    def get_video_tags(self, video_id: str, edit_key: str) -> list[Tag] | None:
        """Get the tags of a video by its ID.

        Args:
            video_id (str): The ID of the video.
            edit_key (str): The edit key for tag operations (required for v2 API).
                            Can be obtained from WatchData.tag.edit.edit_key or WatchData.tag.viewer.edit_key.

        Returns:
            list[Tag] | None: The tags of the video if found, None otherwise.
        """
        headers = {}
        if edit_key is not None:
            headers["X-Tag-Edit-Key"] = edit_key

        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/videos/{video_id}/tags", headers=headers)
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[TagsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.tags
        return None

    def get_mylist(
        self,
        mylist_id: str,
        *,
        page_size: int = 20,
        page: int = 1,
        sort_key: MylistSortKey | None = None,
        sort_order: MylistSortOrder | None = None,
    ) -> Mylist | None:
        """Get a mylist by its ID.

        Args:
            mylist_id (str): The ID of the mylist.
            page_size (int): The number of videos to get per page.
            page (int): The page number.
            sort_key (MylistSortKey | None): The sort key.
            sort_order (MylistSortOrder | None): The sort order.

        Returns:
            Mylist | None: The mylist object if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        if sort_key is not None:
            query["sortKey"] = sort_key
        if sort_order is not None:
            query["sortOrder"] = sort_order
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/mylists/{mylist_id}?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[MylistData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.mylist
        return None

    def get_series(self, series_id: str, *, page_size: int = 100, page: int = 1) -> SeriesData | None:
        """Get a series by its ID.

        Args:
            series_id (str): The ID of the series.
            page_size (int): The number of videos to get per page.
            page (int): The page number.

        Returns:
            SeriesData | None: The series object if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/series/{series_id}?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[SeriesData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_history(self, *, page_size: int = 100, page: int = 1) -> HistoryData | None:
        """Get the history of the authenticated user.

        Args:
            page_size (int): The number of videos to get per page.
            page (int): The page number.

        Returns:
            HistoryData | None: The history data if successful, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/watch/history?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[HistoryData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None
