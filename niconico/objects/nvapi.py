"""A module that contains classes that represent responses from the NvAPI."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from niconico.objects.video import EssentialVideo, Mylist, SeriesDetail, SeriesItem, Tag

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

    ref: https://nvapi.nicovideo.jp/v1/videos/<video_id>/tags
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
