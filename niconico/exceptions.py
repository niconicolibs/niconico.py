"""This module contains exceptions for the niconico package."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from niconico.objects.video.watch import WatchResponseError


class LoginFailureError(Exception):
    """An exception raised when login fails."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        self.message = message
        super().__init__(message)


class DownloadError(Exception):
    """An exception raised when download fails."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        self.message = message
        super().__init__(message)


class NicoAPIError(Exception):
    """An exception raised when an error occurs in the Nico API."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        self.message = message
        super().__init__(message)


class LoginRequiredError(Exception):
    """An exception raised when login is required."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        self.message = message
        super().__init__(message)


class PremiumRequiredError(Exception):
    """An exception raised when a premium account is required."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        self.message = message
        super().__init__(message)


class WatchAPIError(Exception):
    """An exception raised when an error occurs in the watch API."""

    def __init__(self, response: WatchResponseError) -> None:
        """Initialize the exception."""
        self.response = response
        super().__init__(response.error_code)
