"""This module provides the video search client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import requests

from niconico.base.client import BaseClient
from niconico.objects.nvapi import FacetData, ListSearchData, NvAPIResponse, VideoSearchData

if TYPE_CHECKING:
    from niconico.objects.video.search import (
        FacetItem,
        ListSearchSortKey,
        ListType,
        VideoSearchSortKey,
        VideoSearchSortOrder,
    )


class VideoSearchClient(BaseClient):
    """A class that represents a video search client."""

    def search_videos_by_keyword(
        self,
        keyword: str,
        *,
        sort_key: VideoSearchSortKey = "hot",
        sort_order: VideoSearchSortOrder = "none",
        page_size: int = 25,
        page: int = 1,
        sensitive_content: Literal["mask", "filter"] | None = None,
        channel_video_listing_status: Literal["included"] | None = None,
        allow_future_contents: bool | None = None,
        search_by_user: bool | None = None,
        min_registered_at: str | None = None,
        max_registered_at: str | None = None,
        max_duration: int | None = None,
    ) -> VideoSearchData | None:
        """Search videos by a keyword.

        Args:
            keyword (str): The keyword to search.
            sort_key (VideoSearchSortKey): The sort key.
            sort_order (VideoSearchSortOrder): The sort order.
            page_size (int): The page size.
            page (int): The page.
            sensitive_content (Literal["mask", "filter"] | None): The sensitive content.
            channel_video_listing_status (Literal["included"] | None): The channel video listing status.
            allow_future_contents (bool | None): The allow future contents.
            search_by_user (bool | None): The search by user.
            min_registered_at (str | None): The minimum registered at.
            max_registered_at (str | None): The maximum registered at.
            max_duration (int | None): The maximum duration.

        Returns:
            VideoSearchData | None: The search result.
        """
        query = {
            "keyword": keyword,
            "sortKey": sort_key,
            "sortOrder": sort_order,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if sensitive_content is not None:
            query["sensitiveContent"] = sensitive_content
        if channel_video_listing_status is not None:
            query["channelVideoListingStatus"] = channel_video_listing_status
        if allow_future_contents is not None:
            query["allowFutureContents"] = "true" if allow_future_contents else "false"
        if search_by_user is not None:
            query["searchByUser"] = "true" if search_by_user else "false"
        if min_registered_at is not None:
            query["minRegisteredAt"] = min_registered_at
        if max_registered_at is not None:
            query["maxRegisteredAt"] = max_registered_at
        if max_duration is not None:
            query["maxDuration"] = str(max_duration)
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/search/video?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[VideoSearchData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def search_videos_by_tag(
        self,
        tag: str,
        *,
        sort_key: VideoSearchSortKey = "hot",
        sort_order: VideoSearchSortOrder = "none",
        page_size: int = 25,
        page: int = 1,
        sensitive_content: Literal["mask", "filter"] | None = None,
        channel_video_listing_status: Literal["included"] | None = None,
        allow_future_contents: bool | None = None,
        search_by_user: bool | None = None,
        min_registered_at: str | None = None,
        max_registered_at: str | None = None,
        max_duration: int | None = None,
    ) -> VideoSearchData | None:
        """Search videos by a tag.

        Args:
            tag (str): The tag to search.
            sort_key (VideoSearchSortKey): The sort key.
            sort_order (VideoSearchSortOrder): The sort order.
            page_size (int): The page size.
            page (int): The page.
            sensitive_content (Literal["mask", "filter"] | None): The sensitive content.
            channel_video_listing_status (Literal["included"] | None): The channel video listing status.
            allow_future_contents (bool | None): The allow future contents.
            search_by_user (bool | None): The search by user.
            min_registered_at (str | None): The minimum registered at.
            max_registered_at (str | None): The maximum registered at.
            max_duration (int | None): The maximum duration.

        Returns:
            VideoSearchData | None: The search result.
        """
        query = {
            "tag": tag,
            "sortKey": sort_key,
            "sortOrder": sort_order,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if sensitive_content is not None:
            query["sensitiveContent"] = sensitive_content
        if channel_video_listing_status is not None:
            query["channelVideoListingStatus"] = channel_video_listing_status
        if allow_future_contents is not None:
            query["allowFutureContents"] = "true" if allow_future_contents else "false"
        if search_by_user is not None:
            query["searchByUser"] = "true" if search_by_user else "false"
        if min_registered_at is not None:
            query["minRegisteredAt"] = min_registered_at
        if max_registered_at is not None:
            query["maxRegisteredAt"] = max_registered_at
        if max_duration is not None:
            query["maxDuration"] = str(max_duration)
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/search/video?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[VideoSearchData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_facet_by_keyword(
        self,
        keyword: str,
        *,
        sort_key: VideoSearchSortKey = "hot",
        sort_order: VideoSearchSortOrder = "none",
        sensitive_content: Literal["mask", "filter"] | None = None,
        channel_video_listing_status: Literal["included"] | None = None,
        allow_future_contents: bool | None = None,
        search_by_user: bool | None = None,
        min_registered_at: str | None = None,
        max_registered_at: str | None = None,
        max_duration: int | None = None,
    ) -> list[FacetItem]:
        """Get the number of videos for each genre of videos searched with specified conditions.

        Args:
            keyword (str): The keyword to search.
            sort_key (VideoSearchSortKey): The sort key.
            sort_order (VideoSearchSortOrder): The sort order.
            sensitive_content (Literal["mask", "filter"] | None): The sensitive content.
            channel_video_listing_status (Literal["included"] | None): The channel video listing status.
            allow_future_contents (bool | None): The allow future contents.
            search_by_user (bool | None): The search by user.
            min_registered_at (str | None): The minimum registered at.
            max_registered_at (str | None): The maximum registered at.
            max_duration (int | None): The maximum duration.

        Returns:
            list[FacetItem]: The facet items.
        """
        query = {
            "keyword": keyword,
            "sortKey": sort_key,
            "sortOrder": sort_order,
        }
        if sensitive_content is not None:
            query["sensitiveContent"] = sensitive_content
        if channel_video_listing_status is not None:
            query["channelVideoListingStatus"] = channel_video_listing_status
        if allow_future_contents is not None:
            query["allowFutureContents"] = "true" if allow_future_contents else "false"
        if search_by_user is not None:
            query["searchByUser"] = "true" if search_by_user else "false"
        if min_registered_at is not None:
            query["minRegisteredAt"] = min_registered_at
        if max_registered_at is not None:
            query["maxRegisteredAt"] = max_registered_at
        if max_duration is not None:
            query["maxDuration"] = str(max_duration)
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/search/facet?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[FacetData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.items
        return []

    def search_facet_by_tag(
        self,
        tag: str,
        *,
        sort_key: VideoSearchSortKey = "hot",
        sort_order: VideoSearchSortOrder = "none",
        sensitive_content: Literal["mask", "filter"] | None = None,
        channel_video_listing_status: Literal["included"] | None = None,
        allow_future_contents: bool | None = None,
        search_by_user: bool | None = None,
        min_registered_at: str | None = None,
        max_registered_at: str | None = None,
        max_duration: int | None = None,
    ) -> list[FacetItem]:
        """Search videos by a tag.

        Args:
            tag (str): The tag to search.
            sort_key (VideoSearchSortKey): The sort key.
            sort_order (VideoSearchSortOrder): The sort order.
            sensitive_content (Literal["mask", "filter"] | None): The sensitive content.
            channel_video_listing_status (Literal["included"] | None): The channel video listing status.
            allow_future_contents (bool | None): The allow future contents.
            search_by_user (bool | None): The search by user.
            min_registered_at (str | None): The minimum registered at.
            max_registered_at (str | None): The maximum registered at.
            max_duration (int | None): The maximum duration.

        Returns:
            list[FacetItem]: The facet items.
        """
        query = {
            "tag": tag,
            "sortKey": sort_key,
            "sortOrder": sort_order,
        }
        if sensitive_content is not None:
            query["sensitiveContent"] = sensitive_content
        if channel_video_listing_status is not None:
            query["channelVideoListingStatus"] = channel_video_listing_status
        if allow_future_contents is not None:
            query["allowFutureContents"] = "true" if allow_future_contents else "false"
        if search_by_user is not None:
            query["searchByUser"] = "true" if search_by_user else "false"
        if min_registered_at is not None:
            query["minRegisteredAt"] = min_registered_at
        if max_registered_at is not None:
            query["maxRegisteredAt"] = max_registered_at
        if max_duration is not None:
            query["maxDuration"] = str(max_duration)
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/search/facet?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[FacetData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.items
        return []

    def search_lists(
        self,
        keyword: str,
        sort_key: ListSearchSortKey = "_hotTotalScore",
        types: list[ListType] | None = None,
        page_size: int = 100,
        page: int = 1,
    ) -> ListSearchData | None:
        """Search lists.

        Args:
            keyword (str): The keyword to search.
            sort_key (ListSearchSortKey): The sort key.
            types (list[ListType]): The types. If None, all types are included.
            page_size (int): The page size.
            page (int): The page.

        Returns:
            ListSearchData | None: The search result.
        """
        query = {
            "keyword": keyword,
            "sortKey": sort_key,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if types is not None and len(types) == 1:
            query["types"] = types[0]
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/search/list?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[ListSearchData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None
