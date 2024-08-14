"""Module for user search client."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from niconico.base.client import BaseClient
from niconico.objects.nvapi import NvAPIResponse, UserSearchData

if TYPE_CHECKING:
    from niconico.objects.user.search import UserSearchSortKey


class UserSearchClient(BaseClient):
    """Client for user search."""

    def search_users(
        self,
        keyword: str,
        *,
        sort_key: UserSearchSortKey = "_personalized",
        page_size: int = 100,
        page: int = 1,
    ) -> UserSearchData | None:
        """Search users by keyword.

        Args:
            keyword (str): Keyword to search.
            sort_key (UserSearchSortKey, optional): Sort key. Defaults to "_personalized".
            page_size (int, optional): Page size. Defaults to 100.
            page (int, optional): Page. Defaults to 1.

        Returns:
            UserSearchData | None: User search data.
        """
        query = {
            "keyword": keyword,
            "sortKey": sort_key,
            "pageSize": page_size,
            "page": page,
        }
        query_str = "&".join(f"{key}={value}" for key, value in query.items())
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/search/user?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserSearchData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None
