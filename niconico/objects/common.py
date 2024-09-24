"""This module contains the class that represents common objects."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class UserIcon(BaseModel):
    """A class that represents the icons of a user."""

    small: str
    large: str


class EssentialUser(BaseModel):
    """A class that represents an essential user object."""

    type_: Literal["essential"] = Field(..., alias="type")
    is_premium: bool = Field(..., alias="isPremium")
    description: str
    stripped_description: str = Field(..., alias="strippedDescription")
    short_description: str = Field(..., alias="shortDescription")
    id_: int = Field(..., alias="id")
    nickname: str
    icons: UserIcon


class EssentialChannel(BaseModel):
    """A class that represents a essential channel object."""

    id_: str = Field(..., alias="id")
    name: str
    description: str
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    thumbnail_small_url: str = Field(..., alias="thumbnailSmallUrl")
