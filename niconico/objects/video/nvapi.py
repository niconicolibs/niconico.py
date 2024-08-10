"""A module that contains classes that represent responses from the NvAPI."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from niconico.objects.video import EssentialVideo, HistoryItem, Mylist, SeriesDetail, SeriesItem, Tag
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

    ref: https://nvapi.nicovideo.jp/v1/users/me/watch/history
    """

    items: list[HistoryItem]
    total_count: int = Field(..., alias="totalCount")
