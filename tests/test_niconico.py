"""Tests for core HTTP helpers."""

from __future__ import annotations

from typing import Any

from niconico import NicoNico


class DummySession:
    """Capture requests issued by NicoNico."""

    def __init__(self) -> None:
        """Initialize captured request storage."""
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def get(self, url: str, *, headers: dict[str, str]) -> object:
        """Capture a GET request."""
        self.calls.append(("GET", url, {"headers": headers}))
        return object()

    def post(
        self,
        url: str,
        *,
        headers: dict[str, str],
        data: object | None = None,
        json: object | None = None,
    ) -> object:
        """Capture a POST request."""
        self.calls.append(("POST", url, {"headers": headers, "data": data, "json": json}))
        return object()

    def put(
        self,
        url: str,
        *,
        headers: dict[str, str],
        data: object | None = None,
        json: object | None = None,
    ) -> object:
        """Capture a PUT request."""
        self.calls.append(("PUT", url, {"headers": headers, "data": data, "json": json}))
        return object()

    def delete(self, url: str, *, headers: dict[str, str]) -> object:
        """Capture a DELETE request."""
        self.calls.append(("DELETE", url, {"headers": headers}))
        return object()


def test_get_sets_frontend_headers_and_allows_overrides() -> None:
    """GET requests include NvAPI headers and preserve explicit overrides."""
    client = NicoNico()
    session = DummySession()
    client.session = session  # type: ignore[assignment]

    client.get("https://nvapi.nicovideo.jp/v1/videos?watchIds=sm9", headers={"X-Test": "1"})

    method, url, kwargs = session.calls[0]
    assert method == "GET"
    assert url == "https://nvapi.nicovideo.jp/v1/videos?watchIds=sm9"
    assert kwargs["headers"]["User-Agent"] == "niconico.py"
    assert kwargs["headers"]["X-Frontend-Id"] == "6"
    assert kwargs["headers"]["Host"] == "nvapi.nicovideo.jp"
    assert kwargs["headers"]["X-Test"] == "1"


def test_post_sends_json_when_provided() -> None:
    """POST requests choose JSON payloads when supplied."""
    client = NicoNico()
    session = DummySession()
    client.session = session  # type: ignore[assignment]

    payload = {"outputs": [["video", "audio"]]}
    client.post("https://nvapi.nicovideo.jp/v1/watch/sm9/access-rights/hls", json=payload)

    method, _, kwargs = session.calls[0]
    assert method == "POST"
    assert kwargs["json"] == payload
    assert kwargs["data"] is None
    assert kwargs["headers"]["X-Niconico-Language"] == "ja-jp"


def test_put_sends_form_data_when_json_is_absent() -> None:
    """PUT requests send form data by default."""
    client = NicoNico()
    session = DummySession()
    client.session = session  # type: ignore[assignment]

    payload = {"name": "new name"}
    client.put("https://nvapi.nicovideo.jp/v1/users/me/mylists/1", data=payload)

    method, url, kwargs = session.calls[0]
    assert method == "PUT"
    assert url == "https://nvapi.nicovideo.jp/v1/users/me/mylists/1"
    assert kwargs["data"] == payload
    assert kwargs["json"] is None
    assert kwargs["headers"]["X-Niconico-Language"] == "ja-jp"
