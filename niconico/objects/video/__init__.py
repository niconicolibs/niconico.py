"""This module contains the class that represents a video object."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from niconico.objects.common import EssentialChannel, EssentialUser


class VideoCount(BaseModel):
    """A class that represents the count of a video."""

    view: int
    comment: int
    mylist: int
    like: int


class VideoThumbnail(BaseModel):
    """A class that represents the thumbnail of a video."""

    url: str
    middle_url: str | None = Field(..., alias="middleUrl")
    large_url: str | None = Field(..., alias="largeUrl")
    listing_url: str = Field(..., alias="listingUrl")
    nhd_url: str = Field(..., alias="nHdUrl")


class Owner(BaseModel):
    """A class that represents the owner of a video."""

    owner_type: Literal["user", "channel", "hidden"] = Field(..., alias="ownerType")
    type_: Literal["user", "channel", "unknown"] = Field(..., alias="type")
    visibility: Literal["visible", "hidden"]
    id_: str | None = Field(..., alias="id")
    name: str | None
    icon_url: str | None = Field(..., alias="iconUrl")


class VideoLive(BaseModel):
    """A class that represents a live video."""

    live_start_time: str | None = Field(..., alias="liveStartTime")


class EssentialVideo(BaseModel):
    """A class that represents an essential video object."""

    type_: Literal["essential"] = Field(..., alias="type")
    id_: str = Field(..., alias="id")
    title: str
    registered_at: str = Field(..., alias="registeredAt")
    count: VideoCount
    thumbnail: VideoThumbnail
    duration: int
    short_description: str = Field(..., alias="shortDescription")
    latest_comment_summary: str = Field(..., alias="latestCommentSummary")
    is_channel_video: bool = Field(..., alias="isChannelVideo")
    is_payment_required: bool = Field(..., alias="isPaymentRequired")
    playback_position: float | None = Field(..., alias="playbackPosition")
    owner: Owner
    require_sensitive_masking: bool = Field(..., alias="requireSensitiveMasking")
    video_live: VideoLive | None = Field(..., alias="videoLive")
    is_muted: bool | None = Field(..., alias="isMuted")


class Tag(BaseModel):
    """A class that represents a tag."""

    name: str
    is_locked: bool = Field(..., alias="isLocked")
    is_locked_by_system: bool = Field(..., alias="isLockedBySystem")
    is_nicodic_article_exists: bool = Field(..., alias="isNicodicArticleExists")


MylistSortKey = Literal[
    "addedAt",
    "title",
    "mylistComment",
    "registeredAt",
    "viewCount",
    "lastComment",
    "commentCount",
    "likeCount",
    "mylistCount",
    "duration",
]


MylistSortOrder = Literal["desc", "asc"]


class MylistItem(BaseModel):
    """A class that represents a mylist item."""

    item_id: int = Field(..., alias="itemId")
    watch_id: str = Field(..., alias="watchId")
    description: str
    decorated_description_html: str = Field(..., alias="decoratedDescriptionHtml")
    added_at: str = Field(..., alias="addedAt")
    status: Literal["public", "hidden", "deleted"]
    video: EssentialVideo


class Mylist(BaseModel):
    """A class that represents a mylist."""

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
    has_invisible_items: bool = Field(..., alias="hasInvisibleItems")
    follower_count: int = Field(..., alias="followerCount")
    is_following: bool = Field(..., alias="isFollowing")


class SeriesOwner(BaseModel):
    """A class that represents the owner of a series."""

    type_: Literal["user", "channel"] = Field(..., alias="type")
    id_: str = Field(..., alias="id")
    user: EssentialUser | None = None
    channel: EssentialChannel | None = None


class SeriesDetail(BaseModel):
    """A class that represents the detail of a series."""

    id_: int = Field(..., alias="id")
    owner: SeriesOwner
    title: str
    description: str
    decorated_description_html: str = Field(..., alias="decoratedDescriptionHtml")
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    is_listed: bool = Field(..., alias="isListed")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")


class SeriesVideoMeta(BaseModel):
    """A class that represents the metadata of a series video."""

    id_: str = Field(..., alias="id")
    order: int
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")


class SeriesItem(BaseModel):
    """A class that represents a series item."""

    meta: SeriesVideoMeta
    video: EssentialVideo


class HistoryItem(BaseModel):
    """A class that represents a history item."""

    frontend_id: int = Field(..., alias="frontendId")
    is_maybe_like_user_item: bool = Field(..., alias="isMaybeLikeUserItem")
    last_viewed_at: str = Field(..., alias="lastViewedAt")
    playback_position: float = Field(..., alias="playbackPosition")
    video: EssentialVideo
    views: int
    watch_id: str = Field(..., alias="watchId")
