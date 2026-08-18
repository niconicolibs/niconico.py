"""Tests for the video search client."""

from __future__ import annotations

from typing import Any

import requests

from niconico.video.search import VideoSearchClient

SNAPSHOT_TOTAL_COUNT = 2


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
    """Capture requests from VideoSearchClient."""

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


def _snapshot_payload() -> dict[str, Any]:
    """Return a minimal snapshot search payload."""
    return {
        "meta": {
            "status": 200,
            "totalCount": SNAPSHOT_TOTAL_COUNT,
            "id": "00000000-0000-0000-0000-000000000000",
        },
        "data": [
            {"contentId": "sm9", "title": "sample", "viewCounter": 1},
            {"contentId": "sm1097445", "title": "sample 2", "viewCounter": 2},
        ],
    }


def test_snapshot_search_builds_default_query() -> None:
    """Defaults are applied and the keyword is percent encoded."""
    niconico = DummyNicoNico(_snapshot_payload())
    client = VideoSearchClient(niconico)  # type: ignore[arg-type]

    result = client.search_videos_by_snapshot("初音ミク & ボカロ")

    assert result is not None
    assert result.meta.total_count == SNAPSHOT_TOTAL_COUNT
    assert [item.content_id for item in result.data] == ["sm9", "sm1097445"]
    url = niconico.calls[0]
    assert url.startswith("https://snapshot.search.nicovideo.jp/api/v2/snapshot/video/contents/search?")
    assert "q=%E5%88%9D%E9%9F%B3%E3%83%9F%E3%82%AF+%26+%E3%83%9C%E3%82%AB%E3%83%AD" in url
    assert "targets=title%2Cdescription%2Ctags" in url
    assert "fields=contentId%2Ctitle" in url
    assert "_sort=-viewCounter" in url
    assert "_offset=0" in url
    assert "_limit=10" in url
    assert "_context=niconico.py" in url


def test_snapshot_search_builds_sort_and_filters() -> None:
    """Ascending order and filter conditions are encoded."""
    niconico = DummyNicoNico(_snapshot_payload())
    client = VideoSearchClient(niconico)  # type: ignore[arg-type]

    client.search_videos_by_snapshot(
        "sample",
        ["tagsExact"],
        sort_key="startTime",
        sort_order="asc",
        fields=["contentId", "startTime"],
        filters={"viewCounter": {"gte": "10000"}, "genre": ["ゲーム"]},
        offset=25,
        limit=50,
        context="test",
    )

    url = niconico.calls[0]
    assert "targets=tagsExact" in url
    assert "_sort=%2BstartTime" in url
    assert "filters%5BviewCounter%5D%5Bgte%5D=10000" in url
    assert "filters%5Bgenre%5D%5B0%5D=%E3%82%B2%E3%83%BC%E3%83%A0" in url
    assert "_offset=25" in url
    assert "_limit=50" in url
    assert "_context=test" in url


def test_snapshot_search_prefers_json_filter() -> None:
    """A JSON filter replaces the simple filters."""
    niconico = DummyNicoNico(_snapshot_payload())
    client = VideoSearchClient(niconico)  # type: ignore[arg-type]

    client.search_videos_by_snapshot(
        "sample",
        filters={"viewCounter": {"gte": "10000"}},
        json_filter='{"type":"range","field":"viewCounter","from":10000}',
    )

    url = niconico.calls[0]
    assert "jsonFilter=" in url
    assert "filters%5B" not in url


def test_snapshot_search_returns_none_on_error() -> None:
    """A non-200 response yields None."""
    niconico = DummyNicoNico(
        {"meta": {"status": 400, "errorCode": "QUERY_PARSE_ERROR"}},
        status_code=requests.codes.bad_request,
    )
    client = VideoSearchClient(niconico)  # type: ignore[arg-type]

    assert client.search_videos_by_snapshot("sample") is None


def _video_search_payload() -> dict[str, Any]:
    """Return a minimal video search payload."""
    return {
        "meta": {"status": 200},
        "data": {
            "searchId": "search",
            "keyword": "sample",
            "tag": None,
            "genres": [],
            "totalCount": 0,
            "hasNext": False,
            "items": [],
            "additionals": {"tags": []},
        },
    }


def test_keyword_search_sends_sensitive_contents_plural() -> None:
    """The sensitive content filter uses the plural parameter the API validates."""
    niconico = DummyNicoNico(_video_search_payload())
    client = VideoSearchClient(niconico)  # type: ignore[arg-type]

    client.search_videos_by_keyword("sample", sensitive_content="filter")

    url = niconico.calls[0]
    assert "sensitiveContents=filter" in url
    assert "sensitiveContent=" not in url.replace("sensitiveContents=", "")


def test_keyword_search_sends_select_content_type() -> None:
    """Short videos can be selected through selectContentType."""
    niconico = DummyNicoNico(_video_search_payload())
    client = VideoSearchClient(niconico)  # type: ignore[arg-type]

    client.search_videos_by_keyword("sample", select_content_type="short")

    assert "selectContentType=short" in niconico.calls[0]


def test_search_omits_unset_optional_params() -> None:
    """Optional parameters stay absent when not provided."""
    niconico = DummyNicoNico(_video_search_payload())
    client = VideoSearchClient(niconico)  # type: ignore[arg-type]

    client.search_videos_by_keyword("sample")

    url = niconico.calls[0]
    assert "selectContentType" not in url
    assert "sensitiveContents" not in url
    assert "allowFutureContents" not in url
