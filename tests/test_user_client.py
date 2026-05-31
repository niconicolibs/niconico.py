"""Tests for the user client."""

from __future__ import annotations

from typing import Any

import requests

from niconico.user import UserClient


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
    """Capture GET requests from UserClient."""

    logined = True
    premium = False

    def __init__(self, payload: dict[str, Any], *, status_code: int = requests.codes.ok) -> None:
        """Initialize captured URLs and response payload."""
        self.payload = payload
        self.status_code = status_code
        self.urls: list[str] = []
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def get(self, url: str, *, headers: dict[str, str] | None = None) -> DummyResponse:
        """Capture a GET request and return the configured payload."""
        _ = headers
        self.urls.append(url)
        self.calls.append(("GET", url, {}))
        return DummyResponse(self.payload, self.status_code)

    def post(
        self,
        url: str,
        *,
        data: dict[str, str] | None = None,
        json: object | None = None,
        headers: dict[str, str] | None = None,
    ) -> DummyResponse:
        """Capture a POST request and return the configured payload."""
        _ = headers
        self.urls.append(url)
        self.calls.append(("POST", url, {"data": data, "json": json}))
        return DummyResponse(self.payload)

    def put(
        self,
        url: str,
        *,
        data: dict[str, str] | None = None,
        json: object | None = None,
        headers: dict[str, str] | None = None,
    ) -> DummyResponse:
        """Capture a PUT request and return the configured payload."""
        _ = headers
        self.urls.append(url)
        self.calls.append(("PUT", url, {"data": data, "json": json}))
        return DummyResponse(self.payload)

    def delete(self, url: str, *, headers: dict[str, str] | None = None) -> DummyResponse:
        """Capture a DELETE request and return the configured payload."""
        _ = headers
        self.urls.append(url)
        self.calls.append(("DELETE", url, {}))
        return DummyResponse(self.payload)


def _owner_payload() -> dict[str, Any]:
    """Return a minimal owner payload."""
    return {
        "ownerType": "user",
        "type": "user",
        "visibility": "visible",
        "id": "4",
        "name": "sample",
        "iconUrl": "https://example.com/icon.jpg",
    }


def _video_payload() -> dict[str, Any]:
    """Return a minimal essential video payload."""
    return {
        "type": "essential",
        "id": "sm9",
        "title": "sample",
        "registeredAt": "2007-03-06T00:33:00+09:00",
        "count": {"view": 1, "comment": 2, "mylist": 3, "like": 4},
        "thumbnail": {
            "url": "https://example.com/thumb.jpg",
            "middleUrl": "https://example.com/thumb_m.jpg",
            "largeUrl": "https://example.com/thumb_l.jpg",
            "listingUrl": "https://example.com/thumb_list.jpg",
            "nHdUrl": "https://example.com/thumb_nhd.jpg",
        },
        "duration": 1,
        "shortDescription": "",
        "latestCommentSummary": "",
        "isChannelVideo": False,
        "isPaymentRequired": False,
        "playbackPosition": None,
        "owner": _owner_payload(),
        "requireSensitiveMasking": False,
        "videoLive": None,
        "isMuted": False,
    }


def _mylist_item_payload() -> dict[str, Any]:
    """Return a minimal mylist item payload."""
    return {
        "itemId": 1,
        "watchId": "sm9",
        "description": "memo",
        "decoratedDescriptionHtml": "memo",
        "addedAt": "2026-01-01T00:00:00+09:00",
        "status": "public",
        "video": _video_payload(),
    }


def _mylist_payload() -> dict[str, Any]:
    """Return a minimal full mylist payload."""
    return {
        "id": 1,
        "name": "sample",
        "description": "desc",
        "decoratedDescriptionHtml": "desc",
        "defaultSortKey": "addedAt",
        "defaultSortOrder": "desc",
        "items": [_mylist_item_payload()],
        "totalItemCount": 1,
        "hasNext": False,
        "isPublic": False,
        "owner": _owner_payload(),
        "hasInvisibleItems": False,
        "followerCount": 0,
        "isFollowing": False,
    }


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


def test_get_own_mylist_builds_sort_query() -> None:
    """Own mylist detail requests include optional sorting parameters."""
    payload = {"meta": {"status": 200}, "data": {"mylist": _mylist_payload()}}
    niconico = DummyNicoNico(payload)
    client = UserClient(niconico)  # type: ignore[arg-type]

    result = client.get_own_mylist("1", page_size=5, sort_key="addedAt", sort_order="asc")

    assert result is not None
    assert result.id_ == 1
    assert niconico.urls == [
        "https://nvapi.nicovideo.jp/v1/users/me/mylists/1?pageSize=5&page=1&sortKey=addedAt&sortOrder=asc",
    ]


def test_get_own_mylist_items_returns_item_focused_data() -> None:
    """Own mylist item endpoint returns the direct data object."""
    data = _mylist_payload()
    data.pop("hasInvisibleItems")
    data.pop("followerCount")
    data.pop("isFollowing")
    payload = {"meta": {"status": 200}, "data": data}
    niconico = DummyNicoNico(payload)
    client = UserClient(niconico)  # type: ignore[arg-type]

    result = client.get_own_mylist_items("1", sort_key="viewCount", sort_order="desc")

    assert result is not None
    assert result.items[0].watch_id == "sm9"
    assert niconico.urls == [
        "https://nvapi.nicovideo.jp/v1/users/me/mylists/1/items?sortKey=viewCount&sortOrder=desc",
    ]


def test_add_mylist_item_accepts_description_and_existing_item_success() -> None:
    """Adding an already registered video returns 200 and still counts as success."""
    niconico = DummyNicoNico({"meta": {"status": 200}})
    client = UserClient(niconico)  # type: ignore[arg-type]

    result = client.add_mylist_item("1", "sm9", description="memo note")

    assert result is True
    assert niconico.calls == [
        (
            "POST",
            "https://nvapi.nicovideo.jp/v1/users/me/mylists/1/items?itemId=sm9&description=memo+note",
            {"data": None, "json": None},
        ),
    ]


def test_update_mylist_sends_only_supplied_metadata() -> None:
    """Own mylist metadata updates omit unspecified fields."""
    payload = {"meta": {"status": 200}, "data": {"mylist": _mylist_payload()}}
    niconico = DummyNicoNico(payload)
    client = UserClient(niconico)  # type: ignore[arg-type]

    result = client.update_mylist("1", name="renamed", is_public=False, default_sort_order="asc")

    assert result is not None
    assert niconico.calls == [
        (
            "PUT",
            "https://nvapi.nicovideo.jp/v1/users/me/mylists/1",
            {"data": {"name": "renamed", "isPublic": "false", "defaultSortOrder": "asc"}, "json": None},
        ),
    ]


def test_reorder_mylists_returns_ordered_ids() -> None:
    """Own mylist reordering sends a comma-separated full order."""
    payload = {"meta": {"status": 200}, "data": {"mylistIds": [3, 2, 1]}}
    niconico = DummyNicoNico(payload)
    client = UserClient(niconico)  # type: ignore[arg-type]

    result = client.reorder_mylists([3, "2", 1])

    assert result is not None
    assert result.mylist_ids == [3, 2, 1]
    assert niconico.calls == [
        ("PUT", "https://nvapi.nicovideo.jp/v1/users/me/mylists/order", {"data": {"order": "3,2,1"}, "json": None}),
    ]


def test_delete_mylist_uses_delete_endpoint() -> None:
    """Own mylist deletion calls the documented endpoint."""
    niconico = DummyNicoNico({"meta": {"status": 200}})
    client = UserClient(niconico)  # type: ignore[arg-type]

    result = client.delete_mylist("1")

    assert result is True
    assert niconico.calls == [("DELETE", "https://nvapi.nicovideo.jp/v1/users/me/mylists/1", {})]


def test_copy_mylist_items_returns_processed_and_duplicated_ids() -> None:
    """Copying mylist items parses the processed item summary."""
    payload = {
        "meta": {"status": 200},
        "data": {"duplicatedIds": ["sm1"], "processedIds": ["sm9"]},
    }
    niconico = DummyNicoNico(payload)
    client = UserClient(niconico)  # type: ignore[arg-type]

    result = client.copy_mylist_items("1", "2", ["sm9", "sm1"])

    assert result is not None
    assert result.processed_ids == ["sm9"]
    assert result.duplicated_ids == ["sm1"]
    assert niconico.calls == [
        (
            "POST",
            "https://nvapi.nicovideo.jp/v1/users/me/copy-mylist-items?from=1&to=2&itemIds=sm9,sm1",
            {"data": None, "json": None},
        ),
    ]
