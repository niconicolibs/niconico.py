"""This module provides a class that represents a video ranking client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import requests

from niconico.base.client import BaseClient
from niconico.objects.video.nvapi import GenresData, NvAPIResponse, PopularTagsData, RankingData

if TYPE_CHECKING:
    from niconico.objects.video.ranking import Genre


class VideoRankingClient(BaseClient):
    """A class that represents a video ranking client."""

    def get_genres(self) -> list[Genre]:
        """Get genres.

        Returns:
            list[Genre]: A list of available genres.
        """
        res = self.niconico.get("https://nvapi.nicovideo.jp/v2/genres")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[GenresData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.genres
        return []

    def get_popular_tags(self, genre_key: str) -> list[str]:
        """Get popular tags of a genre.

        Args:
            genre_key (str): The key of the genre.

        Returns:
            list[str]: A list of popular tags of the genre.
        """
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/genres/{genre_key}/popular-tags")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[PopularTagsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.tags
        return []

    def get_ranking(
        self,
        genre_key: str,
        term: Literal["hour", "24h", "week", "month", "total"],
        *,
        page_size: Literal[25, 100] = 100,
        page: int = 1,
        tag: str | None = None,
        sensitive_contents: Literal["mask", "filter"] | None = None,
    ) -> RankingData | None:
        """Get a ranking.

        Args:
            genre_key (str): The key of the genre.
            term (Literal["hour", "24h", "week", "month", "total"]): The term of the ranking.
            page_size (int, optional): The size of the page. Defaults to 10.
            page (int, optional): The page number. Defaults to 1.
            tag (str, optional): The tag. Defaults to None.
            sensitive_contents (Literal["mask", "filter"], optional): The sensitive contents. Defaults to None.

        Returns:
            RankingData | None: The ranking data.
        """
        query = {
            "term": term,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if tag is not None:
            query["tag"] = tag
        if sensitive_contents is not None:
            query["sensitiveContents"] = sensitive_contents
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/ranking/genre/{genre_key}?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RankingData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_hot_topics(
        self,
        term: Literal["hour", "24h", "week", "month", "total"],
        *,
        page_size: Literal[25, 100] = 100,
        page: int = 1,
        sensitive_contents: Literal["mask", "filter"] | None = None,
    ) -> RankingData | None:
        """Get hot topics.

        Args:
            term (Literal["hour", "24h", "week", "month", "total"]): The term of the hot topics.
            page_size (int, optional): The size of the page. Defaults to 10.
            page (int, optional): The page number. Defaults to 1.
            sensitive_contents (Literal["mask", "filter"], optional): The sensitive contents. Defaults to None.

        Returns:
            list[str]: A list of hot topics.
        """
        query = {
            "term": term,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if sensitive_contents is not None:
            query["sensitiveContents"] = sensitive_contents
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/ranking/hot-topic?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RankingData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None
