"""This module contains the class that represents a channel object."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ChAPIMeta(BaseModel):
    """Represents the metadata of a channel API response."""

    status: int
    error_code: str | None = Field(None, alias="errorCode")
    error_message: str | None = Field(None, alias="errorMessage")
    error_details: dict[str, str] | None = Field(None, alias="errorDetails")


class ChAPIResponse(BaseModel, Generic[T]):
    """Represents a channel API response."""

    meta: ChAPIMeta
    data: T | None


class ChannelStatus(BaseModel):
    """Represents the status of a channel API response."""

    is_open: bool = Field(..., alias="isOpen")
    is_admission_available : bool = Field(..., alias="isAdmissionAvailable")
    is_adult_channel: bool = Field(..., alias="isAdultChannel")
    is_gravure_channel: bool = Field(..., alias="isGravureChannel")


class ChannelCategory(BaseModel):
    """Represents the category of a channel API response."""

    id_: int = Field(..., alias="id")
    name: str


class ChannelBasicConfiguration(BaseModel):
    """Represents the basic configuration of a channel API response."""

    name: str
    description: str
    screen_name: str = Field(..., alias="screenName")
    category: ChannelCategory
    owner_name: str = Field(..., alias="ownerName")


class ChannelExposureConfiguration(BaseModel):
    """Represents the exposure configuration of a channel API response."""

    open_time: str | None = Field(..., alias="openTime")
    close_time: str | None = Field(..., alias="closeTime")


class ChannelAdmissionConfiguration(BaseModel):
    """Represents the admission configuration of a channel API response."""

    is_free: bool = Field(..., alias="isFree")
    is_first_month_free: bool = Field(..., alias="isFirstMonthFree")


class ChannelOthersConfiguration(BaseModel):
    """Represents the others configuration of a channel API response."""

    checkpoint_sales_enabled_flag: bool = Field(..., alias="checkpointSalesEnabledFlag")


class ChannelConfiguration(BaseModel):
    """Represents the configuration of a channel API response."""

    basic: ChannelBasicConfiguration
    exposure: ChannelExposureConfiguration
    admission: ChannelAdmissionConfiguration
    others: ChannelOthersConfiguration


class ChannelLocation(BaseModel):
    """Represents the location of a channel API response."""

    url: str
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    thumbnail_small_url: str = Field(..., alias="thumbnailSmallUrl")
    category_top_page_url: str = Field(..., alias="categoryTopPageUrl")


class ChannelData(BaseModel):
    """Represents the data of a channel API response."""

    id_: int = Field(..., alias="id")
    status: ChannelStatus
    configuration: ChannelConfiguration
    location: ChannelLocation
