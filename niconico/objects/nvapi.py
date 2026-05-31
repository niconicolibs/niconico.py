"""A module that contains classes that represent responses from the NvAPI."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from niconico.objects.user import (
    NicoUser,
    OwnNicoUser,
    OwnVideoItem,
    OwnVideosLimitation,
    RelationshipUser,
    RelationshipUsersSummary,
    UserMylistItem,
    UserRelationships,
    UserSeriesItem,
    UserSeriesThumbnails,
    UserVideoItem,
)
from niconico.objects.user.search import UserSearchItem
from niconico.objects.video import (
    EssentialVideo,
    HistoryItem,
    Mylist,
    MylistItem,
    MylistSortKey,
    MylistSortOrder,
    Owner,
    SeriesDetail,
    SeriesItem,
    Tag,
)
from niconico.objects.video.ranking import Genre
from niconico.objects.video.search import EssentialMylist, EssentialSeries, FacetItem, VideoSearchAdditionals

T = TypeVar("T")


class NvAPIMeta(BaseModel):
    """A class that represents the metadata of a response from the NvAPI."""

    status: int
    error_code: str | None = Field(None, alias="errorCode")


class NvAPIResponse(BaseModel, Generic[T]):
    """A class that represents a response from the NvAPI."""

    meta: NvAPIMeta
    data: T | None


class VideoItem(BaseModel):
    """A class that represents an item of a videos response from the NvAPI."""

    watch_id: str = Field(..., alias="watchId")
    video: EssentialVideo


class VideosData(BaseModel):
    """A class that represents the data of a videos response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/videos?watchIds=<video_id>
    """

    items: list[VideoItem]


class TagsData(BaseModel):
    """A class that represents the data of a tags response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v2/videos/<video_id>/tags
    """

    is_lockable: bool = Field(..., alias="isLockable")
    is_editable: bool = Field(..., alias="isEditable")
    uneditable_reason: str | None = Field(None, alias="uneditableReason")
    tags: list[Tag]


class MylistData(BaseModel):
    """A class that represents the data of a mylist response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v2/mylists/<mylist_id>
    """

    mylist: Mylist


class SeriesData(BaseModel):
    """A class that represents the data of a series response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v2/series/<series_id>
    """

    detail: SeriesDetail
    total_count: int = Field(..., alias="totalCount")
    items: list[SeriesItem]


class GenresData(BaseModel):
    """A class that represents the data of a genre response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v2/genres
    """

    genres: list[Genre]


class PopularTagsData(BaseModel):
    """A class that represents the data of a popular tags response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/genres/<genre_key>/popular-tags
    """

    start_at: str = Field(..., alias="startAt")
    tags: list[str]


class RankingData(BaseModel):
    """A class that represents the data of a ranking response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/ranking/genre/<genre_key>
    """

    items: list[EssentialVideo]
    has_next: bool = Field(..., alias="hasNext")


class VideoSearchData(BaseModel):
    """A class that represents the data of a video search response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v2/search/video
    """

    search_id: str = Field(..., alias="searchId")
    keyword: str | None
    tag: str | None
    genres: list[Genre]
    total_count: int = Field(..., alias="totalCount")
    has_next: bool = Field(..., alias="hasNext")
    items: list[EssentialVideo]
    additionals: VideoSearchAdditionals


class FacetData(BaseModel):
    """A class that represents the data of a facet response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v2/search/facet
    """

    items: list[FacetItem]


class ListSearchData(BaseModel):
    """A class that represents the data of a list search response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/search/list
    """

    search_id: str = Field(..., alias="searchId")
    total_count: int = Field(..., alias="totalCount")
    has_next: bool = Field(..., alias="hasNext")
    items: list[EssentialSeries | EssentialMylist]


class AccessRightsData(BaseModel):
    """A class that represents the data of an access rights response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/watch/<video_id>/access-rights/<type>
    """

    content_url: str | None = Field(None, alias="contentUrl")
    create_time: str | None = Field(None, alias="createTime")
    expire_time: str | None = Field(None, alias="expireTime")


class HistoryData(BaseModel):
    """A class that represents the data of a history response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v2/users/me/watch/history
    """

    items: list[HistoryItem]
    total_count: int | None = Field(None, alias="totalCount")
    next_cursor: str | None = Field(None, alias="nextCursor")


class UserData(BaseModel):
    """A class that represents the data of a user response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/<user_id>
    """

    user: NicoUser
    relationships: UserRelationships


class OwnUserData(BaseModel):
    """A class that represents the data of own user response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me
    """

    user: OwnNicoUser


class RelationshipUsersData(BaseModel):
    """A class that represents the data of a relationship users response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/<user_id>/<type>/users
    """

    items: list[RelationshipUser]
    summary: RelationshipUsersSummary


class UserVideosData(BaseModel):
    """A class that represents the data of a user video response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v3/users/<user_id>/videos
    """

    items: list[UserVideoItem]
    total_count: int = Field(..., alias="totalCount")


class OwnVideosData(BaseModel):
    """A class that represents the data of own videos response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v2/users/me/videos
    """

    items: list[OwnVideoItem]
    total_count: int = Field(..., alias="totalCount")
    total_item_count: int = Field(..., alias="totalItemCount")
    limitation: OwnVideosLimitation


class UserMylistsData(BaseModel):
    """A class that represents the data of mylists response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/<user_id>/mylists
    """

    mylists: list[UserMylistItem]


class UserSeriesData(BaseModel):
    """A class that represents the data of a series response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/<user_id>/series
    """

    total_count: int = Field(..., alias="totalCount")
    items: list[UserSeriesItem]


class OwnSeriesData(BaseModel):
    """A class that represents the data of a series response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me/series
    """

    total_count: int = Field(..., alias="totalCount")
    items: list[UserSeriesItem]
    thumbnails: UserSeriesThumbnails


class UserSearchData(BaseModel):
    """A class that represents the data of a list search response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/search/user
    """

    request_id: str = Field(..., alias="requestId")
    total_count: int = Field(..., alias="totalCount")
    has_next: bool = Field(..., alias="hasNext")
    items: list[UserSearchItem]


class FollowingMylistItem(BaseModel):
    """A class that represents a following mylist item."""

    id_: int = Field(..., alias="id")
    status: str
    detail: UserMylistItem | None = None


class FollowingMylistsData(BaseModel):
    """A class that represents the data of following mylists response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me/following/mylists
    """

    follow_limit: int = Field(..., alias="followLimit")
    mylists: list[FollowingMylistItem]


class FollowingTagItem(BaseModel):
    """A class that represents a following tag item."""

    name: str
    followed_at: str = Field(..., alias="followedAt")
    niconic_summary: str | None = Field(None, alias="nicodicSummary")


class FollowingTagsData(BaseModel):
    """A class that represents the data of following tags response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me/following/tags
    """

    tags: list[FollowingTagItem]


class CreateMylistData(BaseModel):
    """A class that represents the data of a create mylist response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me/mylists
    """

    mylist_id: int = Field(..., alias="mylistId")
    mylist: Mylist


class OwnMylistItemsData(BaseModel):
    """A class that represents the data of an own mylist items response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me/mylists/<mylist_id>/items
    """

    id_: int = Field(..., alias="id")
    name: str
    description: str
    decorated_description_html: str = Field(..., alias="decoratedDescriptionHtml")
    default_sort_key: MylistSortKey = Field(..., alias="defaultSortKey")
    default_sort_order: MylistSortOrder = Field(..., alias="defaultSortOrder")
    items: list[MylistItem]
    total_item_count: int = Field(..., alias="totalItemCount")
    has_next: bool = Field(..., alias="hasNext")
    is_public: bool = Field(..., alias="isPublic")
    owner: Owner


class ReorderMylistsData(BaseModel):
    """A class that represents the data of a reorder mylists response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me/mylists/order
    """

    mylist_ids: list[int] = Field(..., alias="mylistIds")


class CopyMylistItemsData(BaseModel):
    """A class that represents the data of a copy mylist items response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me/copy-mylist-items
    """

    duplicated_ids: list[str] = Field(..., alias="duplicatedIds")
    processed_ids: list[str] = Field(..., alias="processedIds")


class ThreadKeyData(BaseModel):
    """A class that represents the data of a thread key response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/comment/keys/thread?videoId=<video_id>
    """

    thread_key: str = Field(..., alias="threadKey")


class LikeData(BaseModel):
    """A class that represents the data of a like response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me/likes/items?videoId=<video_id>
    """

    thanks_message: str | None = Field(None, alias="thanksMessage")


class LikeHistoryItem(BaseModel):
    """A class that represents a like history item."""

    liked_at: str = Field(..., alias="likedAt")
    thanks_message: str | None = Field(None, alias="thanksMessage")
    video: EssentialVideo
    status: str


class LikeHistorySummary(BaseModel):
    """A class that represents the summary of like history."""

    has_next: bool = Field(..., alias="hasNext")
    can_get_next_page: bool = Field(..., alias="canGetNextPage")
    get_next_page_ng_reason: str | None = Field(None, alias="getNextPageNgReason")


class LikeHistoryData(BaseModel):
    """A class that represents the data of a like history response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/users/me/likes
    """

    items: list[LikeHistoryItem]
    summary: LikeHistorySummary


class RecommendRecipe(BaseModel):
    """A class that represents a recipe of a recommend response from the NvAPI."""

    id_: str = Field(..., alias="id")
    meta: None


class RecommendReason(BaseModel):
    """A class that represents a reason of a recommend item response from the NvAPI."""

    tag: str | None = None


class RecommendItem(BaseModel):
    """A class that represents an item of a recommend response from the NvAPI."""

    id_: str = Field(..., alias="id")
    content_type: str = Field(..., alias="contentType")
    recommend_type: str = Field(..., alias="recommendType")
    # Currently only EssentialVideo is confirmed.
    # We use Any to allow for future variations in format.
    content: EssentialVideo | Any
    reason: RecommendReason | None = None


class RecommendData(BaseModel):
    """A class that represents the data of a recommend response from the NvAPI.

    ref: https://nvapi.nicovideo.jp/v1/recommend
    """

    recipe: RecommendRecipe
    recommend_id: str = Field(..., alias="recommendId")
    items: list[RecommendItem]


class ActivityActor(BaseModel):
    """A class that represents an actor in a feed activity."""

    id_: str = Field(..., alias="id")
    type_: str = Field(..., alias="type")
    name: str
    icon_url: str = Field(..., alias="iconUrl")
    url: str
    is_live: bool = Field(..., alias="isLive")


class ActivityMessage(BaseModel):
    """A class that represents a message in a feed activity."""

    text: str


class ActivityLabel(BaseModel):
    """A class that represents a label in a feed activity."""

    text: str


class ActivityVideoContent(BaseModel):
    """A class that represents video content in a feed activity."""

    duration: int


class ActivityContent(BaseModel):
    """A class that represents content in a feed activity."""

    type_: str = Field(..., alias="type")
    id_: str = Field(..., alias="id")
    title: str
    url: str
    started_at: str = Field(..., alias="startedAt")
    video: ActivityVideoContent | None = None


class Activity(BaseModel):
    """A class that represents a feed activity."""

    sensitive: bool
    message: ActivityMessage
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    label: ActivityLabel
    content: ActivityContent
    id_: str = Field(..., alias="id")
    kind: str
    created_at: str = Field(..., alias="createdAt")
    actor: ActivityActor


class FeedData(BaseModel):
    """A class that represents the data of a feed response from the Feed API.

    ref: https://api.feed.nicovideo.jp/v1/activities/followings/publish?context=header_timeline
    """

    activities: list[Activity]
    code: str
    impression_id: str = Field(..., alias="impressionId")
    next_cursor: str | None = Field(None, alias="nextCursor")
