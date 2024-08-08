"""This module contains the classes that represent the user objects."""

from typing import Literal

from pydantic import BaseModel, Field


class UserIcon(BaseModel):
    """A class that represents the icons of a user."""

    small: str
    large: str


class EssentialUser(BaseModel):
    """A class that represents an essential user object."""

    _type: Literal["essential"] = Field(..., alias="type")
    is_premium: bool = Field(..., alias="isPremium")
    description: str
    stripped_description: str = Field(..., alias="strippedDescription")
    short_description: str = Field(..., alias="shortDescription")
    _id: int = Field(..., alias="id")
    nickname: str
    icons: UserIcon
