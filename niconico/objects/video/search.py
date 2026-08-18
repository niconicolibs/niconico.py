"""This module provides classes that represent search objects."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from niconico.objects.video import Owner
from niconico.objects.video.ranking import Genre

VideoSearchSortKey = Literal[
    "registeredAt",
    "viewCount",
    "lastCommentTime",
    "commentCount",
    "likeCount",
    "mylistCount",
    "duration",
    "hot",
    "personalized",
]

VideoSearchSortOrder = Literal["desc", "asc", "none"]


class RelatedTag(BaseModel):
    """A class that represents a related tag."""

    text: str
    type_: str = Field(..., alias="type")


class VideoSearchAdditionals(BaseModel):
    """A class that represents additional parameters for a video search."""

    tags: list[RelatedTag]


class FacetItem(BaseModel):
    """A class that represents a facet item."""

    genre: Genre
    count: int


ListType = Literal["mylist", "series"]


ListSearchSortKey = Literal["_hotTotalScore", "videoCount", "startTime"]


class EssentialSeries(BaseModel):
    """A class that represents an essential series."""

    id_: int = Field(..., alias="id")
    type_: Literal["series"] = Field(..., alias="type")
    title: str
    description: str
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    video_count: int = Field(..., alias="videoCount")
    owner: Owner
    is_muted: bool = Field(..., alias="isMuted")
    is_following: bool = Field(..., alias="isFollowing")
    follower_count: int = Field(..., alias="followerCount")
    last_video_added_at: str | None = Field(None, alias="lastVideoAddedAt")


class EssentialMylist(BaseModel):
    """A class that represents an essential mylist."""

    id_: int = Field(..., alias="id")
    type_: Literal["mylist"] = Field(..., alias="type")
    title: str
    description: str
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    video_count: int = Field(..., alias="videoCount")
    owner: Owner
    is_muted: bool = Field(..., alias="isMuted")
    is_following: bool = Field(..., alias="isFollowing")
    follower_count: int = Field(..., alias="followerCount")
    last_video_added_at: str | None = Field(None, alias="lastVideoAddedAt")


SnapshotTargetField = Literal["title", "description", "tags", "tagsExact"]

SnapshotResponseField = Literal[
    "contentId",
    "title",
    "description",
    "userId",
    "channelId",
    "viewCounter",
    "mylistCounter",
    "likeCounter",
    "lengthSeconds",
    "thumbnailUrl",
    "startTime",
    "lastResBody",
    "commentCounter",
    "lastCommentTime",
    "categoryTags",
    "tags",
    "genre",
]

SnapshotSortKey = Literal[
    "viewCounter",
    "mylistCounter",
    "likeCounter",
    "lengthSeconds",
    "startTime",
    "commentCounter",
    "lastCommentTime",
]

SnapshotSortOrder = Literal["desc", "asc"]


class SnapshotSearchMeta(BaseModel):
    """A class that represents the meta of a snapshot search response."""

    status: int
    total_count: int | None = Field(None, alias="totalCount")
    id_: str | None = Field(None, alias="id")
    error_code: str | None = Field(None, alias="errorCode")
    error_message: str | None = Field(None, alias="errorMessage")


class SnapshotVideoItem(BaseModel):
    """A class that represents a video of a snapshot search response.

    Every field is optional because a response only contains the fields
    requested through the ``fields`` parameter.
    """

    content_id: str | None = Field(None, alias="contentId")
    title: str | None = None
    description: str | None = None
    user_id: int | None = Field(None, alias="userId")
    channel_id: int | None = Field(None, alias="channelId")
    view_counter: int | None = Field(None, alias="viewCounter")
    mylist_counter: int | None = Field(None, alias="mylistCounter")
    like_counter: int | None = Field(None, alias="likeCounter")
    length_seconds: int | None = Field(None, alias="lengthSeconds")
    thumbnail_url: str | None = Field(None, alias="thumbnailUrl")
    start_time: str | None = Field(None, alias="startTime")
    last_res_body: str | None = Field(None, alias="lastResBody")
    comment_counter: int | None = Field(None, alias="commentCounter")
    last_comment_time: str | None = Field(None, alias="lastCommentTime")
    category_tags: str | None = Field(None, alias="categoryTags")
    tags: str | None = None
    genre: str | None = None


class SnapshotSearchData(BaseModel):
    """A class that represents a snapshot search response.

    ref: https://snapshot.search.nicovideo.jp/api/v2/snapshot/video/contents/search
    """

    meta: SnapshotSearchMeta
    data: list[SnapshotVideoItem]
