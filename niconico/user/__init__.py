"""This module provides a class that represents a user client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import requests

from niconico.base.client import BaseClient
from niconico.decorators import login_required
from niconico.objects.nvapi import (
    NvAPIResponse,
    OwnSeriesData,
    OwnUserData,
    OwnVideosData,
    RecommendData,
    RelationshipUsersData,
    UserData,
    UserMylistsData,
    UserSeriesData,
    UserVideosData,
)
from niconico.user.search import UserSearchClient
from niconico.utils import add_optional_param

if TYPE_CHECKING:
    from niconico.niconico import NicoNico
    from niconico.objects.user import (
        NicoUser,
        OwnNicoUser,
        RecipeId,
        UserMylistItem,
        UserSeriesItem,
        UserVideosSortKey,
        UserVideosSortOrder,
    )


class UserClient(BaseClient):
    """A class that represents a user client."""

    search: UserSearchClient

    def __init__(self, niconico: NicoNico) -> None:
        """Initialize the client."""
        super().__init__(niconico)
        self.search = UserSearchClient(niconico)

    def get_user(self, user_id: str) -> NicoUser | None:
        """Get a user by its ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            NicoUser | None: The user object if found, None otherwise.
        """
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.user
        return None

    def get_user_followers(self, user_id: str, *, page_size: int = 25, page: int = 1) -> RelationshipUsersData | None:
        """Get the followers of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            page_size (int): The number of followers to get per page.
            page (int): The page number to get the followers from.

        Returns:
            RelationshipUsersData | None: The list of followers if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}/followed-by/users?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RelationshipUsersData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_user_followings(self, user_id: str, *, page_size: int = 25, page: int = 1) -> RelationshipUsersData | None:
        """Get the followings of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            page_size (int): The number of followings to get per page.
            page (int): The page number to get the followings from.

        Returns:
            RelationshipUsersData | None: The list of followings if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}/following/users?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RelationshipUsersData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_user_videos(
        self,
        user_id: str,
        *,
        sort_key: UserVideosSortKey = "registeredAt",
        sort_order: UserVideosSortOrder = "asc",
        page_size: int = 30,
        page: int = 1,
        sensitive_contents: Literal["mask", "filter"] | None = None,
    ) -> UserVideosData | None:
        """Get the videos of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            sort_key (UserVideosSortKey): The key to sort the videos by.
            sort_order (UserVideosSortOrder): The order to sort the videos by.
            page_size (int): The number of videos to get per page.
            page (int): The page number to get the videos from.
            sensitive_contents (Literal["mask", "filter"] | None): The sensitive contents to get.

        Returns:
            UserVideosData | None: The list of videos if found, None otherwise.
        """
        query = {
            "sortKey": sort_key,
            "sortOrder": sort_order,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if sensitive_contents is not None:
            query["sensitiveContents"] = sensitive_contents
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v3/users/{user_id}/videos?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserVideosData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    def get_user_mylists(self, user_id: str, *, sample_item_count: int = 0) -> list[UserMylistItem]:
        """Get the mylists of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            sample_item_count (int): The number of items to get from each mylist.

        Returns:
            list[UserMylistItem]: The list of mylists if found, an empty list otherwise.
        """
        query = {"sampleItemCount": str(sample_item_count)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}/mylists?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserMylistsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.mylists
        return []

    def get_user_series(self, user_id: str, *, page_size: int = 100, page: int = 1) -> list[UserSeriesItem]:
        """Get the series of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            page_size (int): The number of series to get per page.
            page (int): The page number to get the series from.

        Returns:
            list[UserSeriesData] | None: The list of series if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/{user_id}/series?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserSeriesData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.items
        return []

    @login_required()
    def get_own(self) -> OwnNicoUser | None:
        """Get the own user.

        Returns:
            OwnNicoUser | None: The own user object if found, None otherwise.
        """
        res = self.niconico.get("https://nvapi.nicovideo.jp/v1/users/me")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[OwnUserData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.user
        return None

    @login_required()
    def get_own_followers(self, *, page_size: int = 25, page: int = 1) -> RelationshipUsersData | None:
        """Get the followers of the own user.

        Args:
            page_size (int): The number of followers to get per page.
            page (int): The page number to get the followers from.

        Returns:
            RelationshipUsersData | None: The list of followers if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/followed-by/users?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RelationshipUsersData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_followings(self, *, page_size: int = 25, page: int = 1) -> RelationshipUsersData | None:
        """Get the followings of the own user.

        Args:
            page_size (int): The number of followings to get per page.
            page (int): The page number to get the followings from.

        Returns:
            RelationshipUsersData | None: The list of followings if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/following/users?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RelationshipUsersData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_videos(
        self,
        *,
        sort_key: UserVideosSortKey = "registeredAt",
        sort_order: UserVideosSortOrder = "asc",
        page_size: int = 30,
        page: int = 1,
        sensitive_contents: Literal["mask", "filter"] | None = None,
    ) -> OwnVideosData | None:
        """Get the own videos.

        Args:
            sort_key (UserVideosSortKey): The key to sort the videos by.
            sort_order (UserVideosSortOrder): The order to sort the videos by.
            page_size (int): The number of videos to get per page.
            page (int): The page number to get the videos from.
            sensitive_contents (Literal["mask", "filter"] | None): The sensitive contents to get.

        Returns:
            OwnVideosData | None: The list of own videos if found, None otherwise.
        """
        query = {
            "sortKey": sort_key,
            "sortOrder": sort_order,
            "pageSize": str(page_size),
            "page": str(page),
        }
        if sensitive_contents is not None:
            query["sensitiveContents"] = sensitive_contents
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v2/users/me/videos?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[OwnVideosData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_mylists(self, *, sample_item_count: int = 0) -> list[UserMylistItem]:
        """Get the own mylists.

        Args:
            sample_item_count (int): The number of items to get from each mylist.

        Returns:
            list[UserMylistItem]: The list of own mylists if found, an empty list otherwise.
        """
        query = {"sampleItemCount": str(sample_item_count)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/mylists?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[UserMylistsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.mylists
        return []

    @login_required()
    def get_own_series(self, *, page_size: int = 100, page: int = 1) -> list[UserSeriesItem]:
        """Get the series of a user by its ID.

        Args:
            user_id (str): The ID of the user.
            page_size (int): The number of series to get per page.
            page (int): The page number to get the series from.

        Returns:
            list[UserSeriesData] | None: The list of series if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/series?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[OwnSeriesData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.items
        return []

    @login_required()
    def get_recommendations(
        self,
        recipe_id: RecipeId,
        *,
        video_id: str | None = None,
        site: str = "nicovideo",
        limit: int | None = None,
        with_reason: bool | None = None,
        sensitive_contents: Literal["mask", "filter"] | None = None,
        recipe_version: int | None = None,
    ) -> RecommendData | None:
        """Get recommendations based on a specific video or general recommendations.

        Args:
            recipe_id (str): The ID of the recommendation recipe. Available options:
                - "video_watch_recommendation": Watch-based recommendations (requires video_id)
                - "video_recommendation_recommend": General video recommendations
                - "video_top_recommend": Top recommended videos
            video_id (str | None): The ID of the video to base the recommendations on.
            site (str): The site to get recommendations from. Defaults to "nicovideo".
            limit (int | None): The maximum number of recommendations to return.
            with_reason (bool | None): Whether to include reasons for recommendations.
            sensitive_contents (Literal["mask", "filter"] | None):  The sensitive contents to get.
            recipe_version (int | None): The version of the recommendation recipe.

        Returns:
            RecommendData | None: The recommendation data if found, None otherwise.
        """
        query: dict[str, str] = {"recipeId": recipe_id, "site": site}

        # Set defaults and add video_id if provided
        if video_id is not None:
            query["videoId"] = video_id
            limit = limit or 25

        # Build query parameters
        add_optional_param(query, "recipeVersion", recipe_version)
        add_optional_param(query, "limit", limit)
        add_optional_param(query, "with_reason", "true" if with_reason else None)
        add_optional_param(query, "sensitiveContents", sensitive_contents)

        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/recommend?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[RecommendData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

