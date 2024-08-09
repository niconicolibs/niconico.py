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
