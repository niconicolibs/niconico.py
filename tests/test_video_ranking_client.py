"""Tests for the video ranking client."""

from __future__ import annotations

from typing import Any

import requests

from niconico.video.ranking import VideoRankingClient

TEIBAN_MAX_ITEM_COUNT = 1000


class DummyResponse:
    """Minimal response object for client tests."""

    def __init__(self, payload: dict[str, Any], status_code: int = requests.codes.ok) -> None:
        """Initialize the response payload."""
        self._payload = payload
        self.status_code = status_code

    def json(self) -> dict[str, Any]:
        """Return a JSON payload."""
        return self._payload


class DummyNicoNico:
    """Capture requests from VideoRankingClient."""

    logined = False
    premium = False

    def __init__(self, payload: dict[str, Any], *, status_code: int = requests.codes.ok) -> None:
        """Initialize captured requests and response payload."""
        self.payload = payload
        self.status_code = status_code
        self.calls: list[str] = []

    def get(self, url: str, *, headers: dict[str, str] | None = None) -> DummyResponse:
        """Capture a GET request."""
        _ = headers
        self.calls.append(url)
        return DummyResponse(self.payload, self.status_code)


def _featured_key(key: str, label: str) -> dict[str, Any]:
    """Return a minimal featured key payload."""
    return {
        "featuredKey": key,
        "label": label,
        "isEnabledTrendTag": True,
        "isMajorFeatured": True,
        "isTopLevel": True,
        "isImmoral": False,
        "isEnabled": True,
    }


def test_get_teiban_ranking_featured_keys() -> None:
    """The featured keys are returned as models."""
    niconico = DummyNicoNico(
        {
            "meta": {"status": 200},
            "data": {
                "definition": {"maxItemCount": {"teiban": 1000, "trendTag": 300, "forYou": 15}},
                "items": [_featured_key("e9uj2uks", "総合"), _featured_key("4eet3ca4", "ゲーム")],
            },
        },
    )
    client = VideoRankingClient(niconico)  # type: ignore[arg-type]

    keys = client.get_teiban_ranking_featured_keys()

    assert [key.featured_key for key in keys] == ["e9uj2uks", "4eet3ca4"]
    assert keys[0].label == "総合"
    assert niconico.calls == ["https://nvapi.nicovideo.jp/v1/ranking/teiban/featured-keys"]


def test_get_teiban_ranking_builds_query() -> None:
    """The ranking request carries the term and paging parameters."""
    niconico = DummyNicoNico(
        {
            "meta": {"status": 200},
            "data": {
                "featuredKey": "e9uj2uks",
                "label": "総合",
                "tag": None,
                "maxItemCount": TEIBAN_MAX_ITEM_COUNT,
                "hasNext": True,
                "items": [],
            },
        },
    )
    client = VideoRankingClient(niconico)  # type: ignore[arg-type]

    ranking = client.get_teiban_ranking("e9uj2uks", "24h", page_size=25, sensitive_contents="mask")

    assert ranking is not None
    assert ranking.featured_key == "e9uj2uks"
    assert ranking.max_item_count == TEIBAN_MAX_ITEM_COUNT
    url = niconico.calls[0]
    assert url.startswith("https://nvapi.nicovideo.jp/v1/ranking/teiban/e9uj2uks?")
    assert "term=24h" in url
    assert "pageSize=25" in url
    assert "page=1" in url
    assert "sensitiveContents=mask" in url


def test_get_teiban_ranking_returns_none_on_error() -> None:
    """A non-200 response yields None."""
    niconico = DummyNicoNico({"meta": {"status": 404}}, status_code=requests.codes.not_found)
    client = VideoRankingClient(niconico)  # type: ignore[arg-type]

    assert client.get_teiban_ranking("nope", "24h") is None
