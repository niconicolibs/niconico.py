"""This module provides the video search client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal
from urllib.parse import urlencode

import requests

from niconico.base.client import BaseClient
from niconico.objects.nvapi import FacetData, ListSearchData, NvAPIResponse, VideoSearchData
from niconico.objects.video.search import SnapshotSearchData

if TYPE_CHECKING:
    from niconico.objects.video.search import (
        FacetItem,
        ListSearchSortKey,
        ListType,
        SnapshotResponseField,
        SnapshotSortKey,
        SnapshotSortOrder,
        SnapshotTargetField,
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
        sort_order: VideoSearchSortOrder = "desc",
        types: list[ListType] | None = None,
        page_size: int = 100,
        page: int = 1,
    ) -> ListSearchData | None:
        """Search lists.

        Args:
            keyword (str): The keyword to search.
            sort_key (ListSearchSortKey): The sort key.
            sort_order (VideoSearchSortOrder): The sort order.
            types (list[ListType]): The types. If None, all types are included.
            page_size (int): The page size.
            page (int): The page.

        Returns:
            ListSearchData | None: The search result.
        """
        query = {
            "keyword": keyword,
            "sortKey": sort_key,
            "sortOrder": sort_order,
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

    def search_videos_by_snapshot(
        self,
        keyword: str,
        targets: list[SnapshotTargetField] | None = None,
        *,
        sort_key: SnapshotSortKey = "viewCounter",
        sort_order: SnapshotSortOrder = "desc",
        fields: list[SnapshotResponseField] | None = None,
        filters: dict[str, dict[str, str] | list[str]] | None = None,
        json_filter: str | None = None,
        offset: int = 0,
        limit: int = 10,
        context: str = "niconico.py",
    ) -> SnapshotSearchData | None:
        """Search videos with the snapshot search API.

        Unlike the other search methods this endpoint is a public API that does not
        require a login. See https://site.nicovideo.jp/search-api-docs/snapshot for
        the full parameter reference.

        Args:
            keyword (str): The keyword to search.
            targets (list[SnapshotTargetField] | None): The fields to search against.
                Defaults to ``["title", "description", "tags"]``.
            sort_key (SnapshotSortKey): The sort key.
            sort_order (SnapshotSortOrder): The sort order.
            fields (list[SnapshotResponseField] | None): The fields to include in the response.
                If None, only ``contentId`` and ``title`` are requested.
            filters (dict[str, dict[str, str] | list[str]] | None): The simple filters, keyed by
                field name. A list is an exact match filter, a dict is a range filter such as
                ``{"gte": "2024-01-01T00:00:00+09:00"}``.
            json_filter (str | None): A JSON encoded filter, used instead of ``filters``.
            offset (int): The offset of the first item to return.
            limit (int): The maximum number of items to return.
            context (str): The name of the service or application sending the request.

        Returns:
            SnapshotSearchData | None: The search result.
        """
        query: list[tuple[str, str]] = [
            ("q", keyword),
            ("targets", ",".join(targets if targets is not None else ["title", "description", "tags"])),
            ("fields", ",".join(fields if fields is not None else ["contentId", "title"])),
            ("_sort", f"{'-' if sort_order == 'desc' else '+'}{sort_key}"),
            ("_offset", str(offset)),
            ("_limit", str(limit)),
            ("_context", context),
        ]
        if json_filter is not None:
            query.append(("jsonFilter", json_filter))
        elif filters is not None:
            for field, condition in filters.items():
                if isinstance(condition, dict):
                    query.extend((f"filters[{field}][{operator}]", value) for operator, value in condition.items())
                else:
                    query.extend((f"filters[{field}][{index}]", value) for index, value in enumerate(condition))
        query_str = urlencode(query)
        res = self.niconico.get(
            f"https://snapshot.search.nicovideo.jp/api/v2/snapshot/video/contents/search?{query_str}",
        )
        if res.status_code == requests.codes.ok:
            return SnapshotSearchData(**res.json())
        return None
