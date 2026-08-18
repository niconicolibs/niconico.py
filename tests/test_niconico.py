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


class DummyCookieContext:
    """Return a scripted sequence of browser cookie jars."""

    def __init__(self, jars: list[list[dict[str, str]]]) -> None:
        """Initialize the scripted cookie jars."""
        self.jars = jars
        self.calls = 0

    def cookies(self) -> list[dict[str, str]]:
        """Return the next scripted cookie jar."""
        jar = self.jars[min(self.calls, len(self.jars) - 1)]
        self.calls += 1
        return jar


class DummyPage:
    """Record fill calls, accepting only the selectors the page is said to have."""

    def __init__(self, known: tuple[str, ...] = ()) -> None:
        """Initialize the recorded fills and the selectors this page knows."""
        self.fills: list[tuple[str, str]] = []
        self.known = known

    def fill(self, selector: str, value: str, timeout: float | None = None) -> None:
        """Record a fill, or raise when the selector is not on this page."""
        _ = timeout
        if selector not in self.known:
            msg = f"selector not found: {selector}"
            raise RuntimeError(msg)
        self.fills.append((selector, value))


def test_login_with_mail_is_deprecated_and_refuses() -> None:
    """The removed mail login raises instead of sending credentials anywhere."""
    client = NicoNico()

    with (
        pytest.warns(DeprecationWarning, match="no longer supported"),
        pytest.raises(LoginFailureError) as excinfo,
    ):
        client.login_with_mail("sample@example.com", "password")

    assert "login_with_browser" in str(excinfo.value)
    assert client.logined is False


def test_wait_for_session_cookie_returns_the_token() -> None:
    """The session token is picked up once the browser sets it."""
    context = DummyCookieContext(
        [
            [{"name": "nicosid", "value": "1"}],
            [{"name": "user_session", "value": "user_session_sample"}],
        ],
    )

    session = NicoNico._wait_for_session_cookie(context, timeout=5.0)  # type: ignore[arg-type] # noqa: SLF001

    assert session == "user_session_sample"


def test_wait_for_session_cookie_times_out() -> None:
    """No token appears when the login is never completed."""
    context = DummyCookieContext([[{"name": "user_session", "value": ""}]])

    assert NicoNico._wait_for_session_cookie(context, timeout=0.0) is None  # type: ignore[arg-type] # noqa: SLF001


def test_prefill_login_form_uses_the_current_field_names() -> None:
    """The fields the login SPA actually renders are filled."""
    page = DummyPage(known=('input[name="mailOrTel"]', 'input[name="password"]'))

    NicoNico._prefill_login_form(page, "sample@example.com", "password")  # type: ignore[arg-type] # noqa: SLF001

    assert page.fills == [
        ('input[name="mailOrTel"]', "sample@example.com"),
        ('input[name="password"]', "password"),
    ]


def test_prefill_login_form_falls_back_to_generic_selectors() -> None:
    """A renamed field is still filled through the fallback selector."""
    page = DummyPage(known=('input[autocomplete="username"]', 'input[type="password"]'))

    NicoNico._prefill_login_form(page, "sample@example.com", "password")  # type: ignore[arg-type] # noqa: SLF001

    assert page.fills == [
        ('input[autocomplete="username"]', "sample@example.com"),
        ('input[type="password"]', "password"),
    ]


def test_prefill_login_form_skips_missing_values_and_survives_changes() -> None:
    """Only supplied credentials are filled, and an unknown form is tolerated."""
    page = DummyPage(known=('input[name="mailOrTel"]',))
    NicoNico._prefill_login_form(page, "sample@example.com", None)  # type: ignore[arg-type] # noqa: SLF001
    assert page.fills == [('input[name="mailOrTel"]', "sample@example.com")]

    NicoNico._prefill_login_form(DummyPage(), "sample@example.com", "password")  # type: ignore[arg-type] # noqa: SLF001
