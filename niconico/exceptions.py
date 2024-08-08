"""This module contains exceptions for the niconico package."""

from __future__ import annotations


class LoginFailureError(Exception):
    """An exception raised when login fails."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        self.message = message
        super().__init__(message)
