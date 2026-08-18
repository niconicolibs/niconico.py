"""This module provides classes that represent playlist objects."""

from __future__ import annotations

from pydantic import BaseModel, Field

from niconico.objects.video import EssentialVideo


class PlaylistId(BaseModel):
    """A class that represents the identifier of a playlist."""

    type_: str = Field(..., alias="type")
    value: str


class PlaylistMeta(BaseModel):
    """A class that represents the meta information of a playlist."""

    title: str
    owner_name: str | None = Field(None, alias="ownerName")


class PlaylistItem(BaseModel):
    """A class that represents an item of a playlist."""

    watch_id: str = Field(..., alias="watchId")
    content: EssentialVideo
