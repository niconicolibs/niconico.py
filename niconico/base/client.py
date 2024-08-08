"""This module contains the base client class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from niconico.niconico import NicoNico


class BaseClient:
    """A class that represents a base client."""

    niconico: NicoNico

    def __init__(self, niconico: NicoNico) -> None:
        """Initialize the base client."""
        self.niconico = niconico
