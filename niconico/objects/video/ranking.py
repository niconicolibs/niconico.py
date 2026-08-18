"""This module contains the class that represents a ranking object."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Genre(BaseModel):
    """A class that represents a genre."""

    key: str
    label: str


class TeibanRankingFeaturedKey(BaseModel):
    """A class that represents a featured key of a teiban ranking."""

    featured_key: str = Field(..., alias="featuredKey")
    label: str
    is_enabled_trend_tag: bool = Field(..., alias="isEnabledTrendTag")
    is_major_featured: bool = Field(..., alias="isMajorFeatured")
    is_top_level: bool = Field(..., alias="isTopLevel")
    is_immoral: bool = Field(..., alias="isImmoral")
    is_enabled: bool = Field(..., alias="isEnabled")


class TeibanRankingMaxItemCount(BaseModel):
    """A class that represents the item limits of the teiban rankings."""

    teiban: int
    trend_tag: int = Field(..., alias="trendTag")
    for_you: int = Field(..., alias="forYou")


class TeibanRankingDefinition(BaseModel):
    """A class that represents the definition of the teiban rankings."""

    max_item_count: TeibanRankingMaxItemCount = Field(..., alias="maxItemCount")
