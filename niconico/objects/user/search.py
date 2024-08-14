"""This module provides classes that represent search objects."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from niconico.objects.user import UserIcon, UserRelationships

UserSearchSortKey = Literal["_personalized", "followerCount", "videoCount", "liveCount"]


class UserSearchItem(BaseModel):
    """A class that represents an item of a user search response from the NvAPI."""

    type_: Literal["userSearch"] = Field(..., alias="type")
    follower_count: int = Field(..., alias="followerCount")
    video_count: int = Field(..., alias="videoCount")
    live_count: int = Field(..., alias="liveCount")
    relationships: UserRelationships
    is_premium: bool = Field(..., alias="isPremium")
    description: str
    stripped_description: str = Field(..., alias="strippedDescription")
    short_description: str = Field(..., alias="shortDescription")
    id_: int = Field(..., alias="id")
    nickname: str
    icons: UserIcon
