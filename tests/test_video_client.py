"""Tests for the video client."""

from __future__ import annotations

from typing import Any

import requests

from niconico.video import VideoClient


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
    """Capture requests from VideoClient."""

    logined = True
    premium = False

    def __init__(
        self,
        payload: dict[str, Any] | list[dict[str, Any]],
        *,
        status_code: int = requests.codes.ok,
    ) -> None:
        """Initialize captured requests and response payload."""
        self.payloads = payload if isinstance(payload, list) else [payload]
        self.status_code = status_code
        self.calls: list[tuple[str, str]] = []

    def _payload(self) -> dict[str, Any]:
        """Return the next queued payload."""
        index = min(len(self.calls), len(self.payloads) - 1)
        return self.payloads[index]

    def get(self, url: str, *, headers: dict[str, str] | None = None) -> DummyResponse:
        """Capture a GET request."""
        payload = self._payload()
        _ = headers
        self.calls.append(("GET", url))
        return DummyResponse(payload, self.status_code)

    def post(
        self,
        url: str,
        *,
        data: dict[str, str] | str | bytes | None = None,
        json: object | None = None,
        headers: dict[str, str] | None = None,
    ) -> DummyResponse:
        """Capture a POST request."""
        payload = self._payload()
        _ = data, json, headers
        self.calls.append(("POST", url))
        return DummyResponse(payload, self.status_code)

    def delete(self, url: str, *, headers: dict[str, str] | None = None) -> DummyResponse:
        """Capture a DELETE request."""
        payload = self._payload()
        _ = headers
        self.calls.append(("DELETE", url))
        return DummyResponse(payload, self.status_code)


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


def _video_payload(video_id: str) -> dict[str, Any]:
    """Return a minimal essential video payload."""
    return {
        "type": "essential",
        "id": video_id,
        "title": f"sample {video_id}",
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


def test_get_videos_fetches_each_video() -> None:
    """Multiple video lookup fetches each ID."""
    niconico = DummyNicoNico(
        [
            {
                "meta": {"status": 200},
                "data": {"items": [{"watchId": "sm9", "video": _video_payload("sm9")}]},
            },
            {
                "meta": {"status": 200},
                "data": {"items": [{"watchId": "sm1097445", "video": _video_payload("sm1097445")}]},
            },
        ],
    )
    client = VideoClient(niconico)  # type: ignore[arg-type]

    result = client.get_videos(["sm9", "sm1097445"])

    assert [video.id_ for video in result] == ["sm9", "sm1097445"]
    assert niconico.calls == [
        ("GET", "https://nvapi.nicovideo.jp/v1/videos?watchIds=sm9"),
        ("GET", "https://nvapi.nicovideo.jp/v1/videos?watchIds=sm1097445"),
    ]


def test_like_video_accepts_created_status() -> None:
    """The like endpoint returns 201 when a video is newly liked."""
    niconico = DummyNicoNico(
        {"meta": {"status": 201}, "data": {"thanksMessage": None}},
        status_code=requests.codes.created,
    )
    client = VideoClient(niconico)  # type: ignore[arg-type]

    result = client.like_video("sm9")

    assert result is not None
    assert result.thanks_message is None
    assert niconico.calls == [
        ("POST", "https://nvapi.nicovideo.jp/v1/users/me/likes/items?videoId=sm9"),
    ]


def test_unlike_video_uses_delete_endpoint() -> None:
    """Unlike removes the authenticated user's like from a video."""
    niconico = DummyNicoNico({"meta": {"status": 200}})
    client = VideoClient(niconico)  # type: ignore[arg-type]

    result = client.unlike_video("sm9")

    assert result is True
    assert niconico.calls == [
        ("DELETE", "https://nvapi.nicovideo.jp/v1/users/me/likes/items?videoId=sm9"),
    ]
