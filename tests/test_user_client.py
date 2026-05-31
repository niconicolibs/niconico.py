"""Tests for the user client."""

from __future__ import annotations

from typing import Any

import requests

from niconico.user import UserClient


class DummyResponse:
    """Minimal response object for client tests."""

    status_code = requests.codes.ok

    def __init__(self, payload: dict[str, Any]) -> None:
        """Initialize the response payload."""
        self._payload = payload

    def json(self) -> dict[str, Any]:
        """Return a JSON payload."""
        return self._payload


class DummyNicoNico:
    """Capture GET requests from UserClient."""

    logined = True
    premium = False

    def __init__(self, payload: dict[str, Any]) -> None:
        """Initialize captured URLs and response payload."""
        self.payload = payload
        self.urls: list[str] = []

    def get(self, url: str, *, headers: dict[str, str] | None = None) -> DummyResponse:
        """Capture a GET request and return the configured payload."""
        _ = headers
        self.urls.append(url)
        return DummyResponse(self.payload)


def test_get_following_activities_builds_cursor_query() -> None:
    """Feed API requests include context and cursor query parameters."""
    payload = {"activities": [], "code": "OK", "impressionId": "impression", "nextCursor": None}
    niconico = DummyNicoNico(payload)
    client = UserClient(niconico)  # type: ignore[arg-type]

    result = client.get_following_activities(context="my_timeline", cursor="cursor-1")

    assert result is not None
    assert result.activities == []
    assert niconico.urls == [
        "https://api.feed.nicovideo.jp/v1/activities/followings/publish?context=my_timeline&cursor=cursor-1",
    ]
