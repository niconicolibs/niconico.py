"""This module contains the class that represents a search channel object."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChSearchAPIMeta(BaseModel):
    """Represents the metadata of a channel API response."""

    status: int
    total: int | None = Field(None)
    count: int | None = Field(None)
    error_code: str | None = Field(None, alias="errorCode")
    error_message: str | None = Field(None, alias="errorMessage")
    error_details: dict[str, str] | None = Field(None, alias="errorDetails")


class ChSearchAPIResponse(BaseModel):
    """Represents a channel API response."""

    meta: ChSearchAPIMeta
    data: list[ChannelSearchItem] | None

class ChannelTag(BaseModel):
    """Represents a channel tag."""

    text: str


class ChannelCategory(BaseModel):
    """Represents a channel category."""

    category_id: int = Field(..., alias="categoryId")
    category_name: str = Field(..., alias="categoryName")
    category_top_page_url: str = Field(..., alias="categoryTopPageUrl")


class ChannelDetail(BaseModel):
    """Represents a channel detail."""

    tags: list[ChannelTag]
    category: ChannelCategory


class ChannelSearchItem(BaseModel):
    """Represents a channel search item."""

    id_: int = Field(..., alias="id")
    name: str
    description: str
    description_html: str | None = Field(None, alias="descriptionHtml")
    is_free: bool = Field(..., alias="isFree")
    screen_name: str = Field(..., alias="screenName")
    owner_name: str = Field(..., alias="ownerName")
    price: int
    body_price: int = Field(..., alias="bodyPrice")
    url: str
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    thumbnail_small_url: str = Field(..., alias="thumbnailSmallUrl")
    can_admit: bool = Field(..., alias="canAdmit")
    is_adult: bool = Field(..., alias="isAdult")
    detail: ChannelDetail
