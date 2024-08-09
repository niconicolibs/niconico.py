"""This module contains the class that represents a ranking object."""

from __future__ import annotations

from pydantic import BaseModel


class Genre(BaseModel):
    """A class that represents a genre."""

    key: str
    label: str
