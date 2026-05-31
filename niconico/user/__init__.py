"""This module provides a class that represents a user client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal
from urllib.parse import urlencode

import requests

from niconico.base.client import BaseClient
from niconico.decorators import login_required
from niconico.objects.nvapi import (
    CopyMylistItemsData,
    CreateMylistData,
    FeedData,
    FollowingMylistsData,
    FollowingTagsData,
    MylistData,
    NvAPIResponse,
    OwnMylistItemsData,
    OwnSeriesData,
    OwnUserData,
    OwnVideosData,
    RecommendData,
    RelationshipUsersData,
    ReorderMylistsData,
    SeriesData,
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
    from niconico.objects.video import Mylist, MylistSortKey, MylistSortOrder


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
    def follow_user(self, user_id: str) -> bool:
        """Follow a user.

        Args:
            user_id (str): The ID of the user to follow.

        Returns:
            bool: True if the user was successfully followed, False otherwise.
        """
        res = self.niconico.post(f"https://user-follow-api.nicovideo.jp/v1/user/followees/niconico-users/{user_id}.json")
        return res.status_code == requests.codes.ok

    @login_required()
    def unfollow_user(self, user_id: str) -> bool:
        """Unfollow a user.

        Args:
            user_id (str): The ID of the user to unfollow.

        Returns:
            bool: True if the user was successfully unfollowed, False otherwise.
        """
        res = self.niconico.delete(f"https://user-follow-api.nicovideo.jp/v1/user/followees/niconico-users/{user_id}.json")
        return res.status_code == requests.codes.ok

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
    def get_own_mylist(
        self,
        mylist_id: str,
        *,
        page_size: int = 20,
        page: int = 1,
        sort_key: MylistSortKey | None = None,
        sort_order: MylistSortOrder | None = None,
    ) -> Mylist | None:
        """Get a own mylist by its ID.

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
        add_optional_param(query, "sortKey", sort_key)
        add_optional_param(query, "sortOrder", sort_order)
        query_str = urlencode(query)
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mylist_id}?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[MylistData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.mylist
        return None

    @login_required()
    def get_own_mylist_items(
        self,
        mylist_id: str,
        *,
        page_size: int = 20,
        page: int = 1,
        sort_key: MylistSortKey | None = None,
        sort_order: MylistSortOrder | None = None,
    ) -> OwnMylistItemsData | None:
        """Get item-focused data for an own mylist by its ID.

        Args:
            mylist_id (str): The ID of the mylist.
            page_size (int): The number of videos to get per page.
            page (int): The page number.
            sort_key (MylistSortKey | None): The sort key.
            sort_order (MylistSortOrder | None): The sort order.

        Returns:
            OwnMylistItemsData | None: The mylist items data if found, None otherwise.
        """
        query: dict[str, str] = {}
        add_optional_param(query, "sortKey", sort_key)
        add_optional_param(query, "sortOrder", sort_order)
        query_str = urlencode(query)
        url = f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mylist_id}/items"
        if query_str:
            url = f"{url}?{query_str}"
        res = self.niconico.get(url)
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[OwnMylistItemsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        mylist = self.get_own_mylist(
            mylist_id,
            page_size=page_size,
            page=page,
            sort_key=sort_key,
            sort_order=sort_order,
        )
        if mylist is not None:
            return OwnMylistItemsData.model_validate(mylist.model_dump(by_alias=True))
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
    def add_mylist_item(self, mylist_id: str, item_id: str, *, description: str | None = None) -> bool:
        """Add a video to a mylist.

        Args:
            mylist_id (str): The ID of the mylist to add the video to.
            item_id (str): The ID of the video to add to the mylist.
            description (str | None): The note to add to the video.

        Returns:
            bool: True if the video was successfully added, False otherwise.
        """
        query = {"itemId": item_id}
        add_optional_param(query, "description", description)
        query_str = urlencode(query)
        res = self.niconico.post(f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mylist_id}/items?{query_str}")
        return res.status_code in (requests.codes.ok, requests.codes.created)

    @login_required()
    def remove_mylist_items(self, mylist_id: str, item_ids: list[str]) -> bool:
        """Remove multiple videos from a mylist.

        Args:
            mylist_id (str): The ID of the mylist to remove the videos from.
            item_ids (list[str]): The IDs of the videos to remove from the mylist.

        Returns:
            bool: True if the videos were successfully removed, False otherwise.
        """
        item_ids_str = ",".join(item_ids)
        res = self.niconico.delete(f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mylist_id}/items?itemIds={item_ids_str}")
        return res.status_code == requests.codes.ok

    @login_required()
    def create_mylist(
        self,
        name: str,
        description: str = "",
        *,
        is_public: bool = False,
        default_sort_key: MylistSortKey = "addedAt",
        default_sort_order: MylistSortOrder = "desc",
    ) -> CreateMylistData | None:
        """Create a new mylist.

        Args:
            name (str): The name of the mylist.
            description (str): The description of the mylist.
            is_public (bool): Whether the mylist is public.
            default_sort_key (MylistSortKey): The default sort key for the mylist.
            default_sort_order (MylistSortOrder): The default sort order for the mylist.

        Returns:
            CreateMylistData | None: The created mylist data if successful, None otherwise.
        """
        data = {
            "name": name,
            "description": description,
            "isPublic": "true" if is_public else "false",
            "defaultSortKey": default_sort_key,
            "defaultSortOrder": default_sort_order,
        }
        res = self.niconico.post("https://nvapi.nicovideo.jp/v1/users/me/mylists", data=data)
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[CreateMylistData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def update_mylist(
        self,
        mylist_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        is_public: bool | None = None,
        default_sort_key: MylistSortKey | None = None,
        default_sort_order: MylistSortOrder | None = None,
    ) -> Mylist | None:
        """Update own mylist metadata.

        Args:
            mylist_id (str): The ID of the mylist to update.
            name (str | None): The new mylist name.
            description (str | None): The new mylist description.
            is_public (bool | None): Whether the mylist is public.
            default_sort_key (MylistSortKey | None): The default sort key.
            default_sort_order (MylistSortOrder | None): The default sort order.

        Returns:
            Mylist | None: The updated mylist if successful, None otherwise.
        """
        data: dict[str, str] = {}
        add_optional_param(data, "name", name)
        add_optional_param(data, "description", description)
        if is_public is not None:
            data["isPublic"] = "true" if is_public else "false"
        add_optional_param(data, "defaultSortKey", default_sort_key)
        add_optional_param(data, "defaultSortOrder", default_sort_order)

        res = self.niconico.put(f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mylist_id}", data=data)
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[MylistData](**res.json())
            if res_cls.data is not None:
                return res_cls.data.mylist
        return None

    @login_required()
    def reorder_mylists(self, mylist_ids: list[str | int]) -> ReorderMylistsData | None:
        """Reorder all own mylists.

        Args:
            mylist_ids (list[str | int]): All own mylist IDs in the desired order.

        Returns:
            ReorderMylistsData | None: The reordered mylist IDs if successful, None otherwise.
        """
        data = {"order": ",".join(str(mylist_id) for mylist_id in mylist_ids)}
        res = self.niconico.put("https://nvapi.nicovideo.jp/v1/users/me/mylists/order", data=data)
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[ReorderMylistsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def delete_mylist(self, mylist_id: str) -> bool:
        """Delete an own mylist.

        Args:
            mylist_id (str): The ID of the mylist to delete.

        Returns:
            bool: True if the mylist was successfully deleted, False otherwise.
        """
        res = self.niconico.delete(f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mylist_id}")
        return res.status_code == requests.codes.ok

    @login_required()
    def copy_mylist_items(
        self,
        from_mylist_id: str,
        to_mylist_id: str,
        item_ids: list[str],
    ) -> CopyMylistItemsData | None:
        """Copy videos from an own mylist to another own mylist.

        Args:
            from_mylist_id (str): The source mylist ID.
            to_mylist_id (str): The destination mylist ID.
            item_ids (list[str]): The video IDs to copy.

        Returns:
            CopyMylistItemsData | None: The copied item result if successful, None otherwise.
        """
        query = {
            "from": from_mylist_id,
            "to": to_mylist_id,
            "itemIds": ",".join(item_ids),
        }
        query_str = urlencode(query, safe=",")
        res = self.niconico.post(f"https://nvapi.nicovideo.jp/v1/users/me/copy-mylist-items?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[CopyMylistItemsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_series_detail(self, series_id: str, *, page_size: int = 100, page: int = 1) -> SeriesData | None:
        """Get a own series by its ID.

        Args:
            series_id (str): The ID of the series.
            page_size (int): The number of videos to get per page.
            page (int): The page number.

        Returns:
            SeriesData | None: The series object if found, None otherwise.
        """
        query = {"pageSize": str(page_size), "page": str(page)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/series/{series_id}?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[SeriesData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_series(self, *, page_size: int = 100, page: int = 1) -> list[UserSeriesItem]:
        """Get the series list of the own user.

        Args:
            page_size (int): The number of series to get per page.
            page (int): The page number to get the series from.

        Returns:
            list[UserSeriesItem]: The list of series if found, an empty list otherwise.
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

    @login_required()
    def get_own_following_mylists(self, *, sample_item_count: int = 0) -> FollowingMylistsData | None:
        """Get the mylists that the own user is following.

        Args:
            sample_item_count (int): The number of items to get from each mylist.

        Returns:
            FollowingMylistsData | None: The following mylists data if found, None otherwise.
        """
        query = {"sampleItemCount": str(sample_item_count)}
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])
        res = self.niconico.get(f"https://nvapi.nicovideo.jp/v1/users/me/following/mylists?{query_str}")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[FollowingMylistsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_own_following_tags(self) -> FollowingTagsData | None:
        """Get the tags that the own user is following.

        Returns:
            FollowingTagsData | None: The following tags data if found, None otherwise.
        """
        res = self.niconico.get("https://nvapi.nicovideo.jp/v1/users/me/following/tags")
        if res.status_code == requests.codes.ok:
            res_cls = NvAPIResponse[FollowingTagsData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None

    @login_required()
    def get_following_activities(
        self,
        *,
        endpoint: Literal["publish", "video"] = "publish",
        context: Literal["header_timeline", "my_timeline"] = "header_timeline",
        cursor: str | None = None,
    ) -> FeedData | None:
        """Get activities from users you follow.

        Args:
            endpoint (Literal["publish", "video"]): The API endpoint to use.
                - "publish": All types of activities (video, illust, etc.)
                - "video": Video activities only
            context (str): The context for the feed. Currently not affecting results.
            cursor (str | None): The cursor for pagination. If None, gets the latest activities.

        Returns:
            FeedData | None: The feed data if successful, None otherwise.
        """
        base_url = "https://api.feed.nicovideo.jp/v1/activities/followings"
        url = f"{base_url}/{endpoint}"

        query: dict[str, str] = {"context": context}
        if cursor is not None:
            query["cursor"] = cursor
        query_str = "&".join([f"{key}={value}" for key, value in query.items()])

        res = self.niconico.get(f"{url}?{query_str}")
        if res.status_code == requests.codes.ok:
            return FeedData(**res.json())
        return None
