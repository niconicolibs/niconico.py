"""Module for channel search client."""

from __future__ import annotations

from typing import Literal

import requests

from niconico.base.client import BaseClient
from niconico.objects.channel.search import ChannelSearchItem, ChSearchAPIResponse


class ChannelSearchClient(BaseClient):
    """Client for channel search."""

    def search_channels(
        self,
        query: str,
        *,
        search_type: Literal["keyword", "tag"] = "keyword",
        limit: int = 20,
        offset: int = 0,
        order: Literal["desc", "asc"] = "desc",
        sort: Literal["updateTime"] | None = None,
    ) -> list[ChannelSearchItem]:
        """Search channels by query.

        Args:
            query (str): Query to search.
            search_type (Literal["keyword", "tag"], optional): Search type. Defaults to "keyword".
            limit (int, optional): Limit. Defaults to 20.
            offset (int, optional): Offset. Defaults to 0.
            order (Literal["desc", "asc"], optional): Order. Defaults to "desc".
            sort (Literal["updateTime"], optional): Sort. Default is created time.

        Returns:
            list[ChannelSearchItem]: Channel search item list.
        """
        query_dict = {
            "query": query,
            "searchType": search_type,
            "limit": str(limit),
            "offset": str(offset),
            "order": order,
            "responseGroup": "detail",
        }
        if sort is not None:
            query_dict["sort"] = sort
        query_str = "&".join(f"{key}={value}" for key, value in query_dict.items())
        res = self.niconico.get(f"https://public-api.ch.nicovideo.jp/v1/open/search/channels?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = ChSearchAPIResponse(**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return []
