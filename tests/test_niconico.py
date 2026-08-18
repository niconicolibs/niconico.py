"""Tests for core HTTP helpers."""

from __future__ import annotations

from typing import Any

import pytest

from niconico import NicoNico
from niconico.exceptions import LoginFailureError


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


class DummyCookie:
    """A minimal stand-in for a cookie in a browser cookie jar."""

    def __init__(self, name: str, value: str) -> None:
        """Initialize the cookie name and value."""
        self.name = name
        self.value = value


def test_login_with_mail_is_deprecated_and_refuses() -> None:
    """The removed mail login raises instead of sending credentials anywhere."""
    client = NicoNico()

    with (
        pytest.warns(DeprecationWarning, match="no longer supported"),
        pytest.raises(LoginFailureError) as excinfo,
    ):
        client.login_with_mail("sample@example.com", "password")

    assert "login_with_browser_cookies" in str(excinfo.value)
    assert client.logined is False


def test_extract_session_cookie_finds_the_session() -> None:
    """The session cookie is picked out of the jar."""
    cookies = [
        DummyCookie("nicosid", "1"),
        DummyCookie("user_session", "user_session_sample"),
    ]

    assert NicoNico._extract_session_cookie(cookies) == "user_session_sample"  # noqa: SLF001


def test_extract_session_cookie_ignores_empty_and_unrelated_cookies() -> None:
    """An empty or missing session cookie yields None."""
    assert NicoNico._extract_session_cookie([DummyCookie("user_session", "")]) is None  # noqa: SLF001
    assert NicoNico._extract_session_cookie([DummyCookie("nicosid", "1")]) is None  # noqa: SLF001
    assert NicoNico._extract_session_cookie([]) is None  # noqa: SLF001


def test_login_with_browser_cookies_reports_a_signed_out_browser(monkeypatch: pytest.MonkeyPatch) -> None:
    """A browser without a NicoNico session gives an actionable error."""
    client = NicoNico()
    monkeypatch.setattr(NicoNico, "_load_browser_cookies", staticmethod(lambda _browser: [DummyCookie("nicosid", "1")]))

    with pytest.raises(LoginFailureError, match="Sign in"):
        client.login_with_browser_cookies()


def test_login_with_browser_cookies_uses_the_imported_session(monkeypatch: pytest.MonkeyPatch) -> None:
    """A found session cookie is handed to login_with_session."""
    client = NicoNico()
    monkeypatch.setattr(
        NicoNico,
        "_load_browser_cookies",
        staticmethod(lambda _browser: [DummyCookie("user_session", "user_session_sample")]),
    )
    used: list[str] = []
    monkeypatch.setattr(NicoNico, "login_with_session", lambda _self, session: used.append(session))

    client.login_with_browser_cookies("firefox")

    assert used == ["user_session_sample"]


def test_load_browser_cookies_rejects_an_unknown_browser() -> None:
    """An unsupported browser name is reported instead of silently ignored."""
    with pytest.raises(LoginFailureError, match="Unsupported browser"):
        NicoNico._load_browser_cookies("netscape")  # noqa: SLF001
