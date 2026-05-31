"""Tests for response object models."""

from __future__ import annotations

from niconico.objects.nvapi import FollowingMylistsData, HistoryData, NvAPIResponse, RelationshipUsersData


def test_relationship_response_accepts_anonymous_relationships() -> None:
    """Public relationship endpoints may return an empty relationships object."""
    payload = {
        "meta": {"status": 200},
        "data": {
            "items": [
                {
                    "id": 125337489,
                    "nickname": "sample",
                    "icons": {"small": "https://example.com/s.jpg", "large": "https://example.com/l.jpg"},
                    "type": "relationship",
                    "isPremium": False,
                    "description": "",
                    "strippedDescription": "",
                    "shortDescription": "",
                    "relationships": {},
                },
            ],
            "summary": {
                "followees": 1,
                "followers": 1,
                "hasNext": False,
                "cursor": "",
            },
        },
    }
    response = NvAPIResponse[RelationshipUsersData].model_validate(payload)

    assert response.data is not None
    assert response.data.items[0].relationships.session_user is None
    assert response.data.items[0].relationships.is_me is False


def test_history_response_accepts_current_v2_shape() -> None:
    """Current watch history responses use itemId/viewedAt and nextCursor."""
    payload = {
        "meta": {"status": 200},
        "data": {
            "items": [
                {
                    "itemId": "h#20260525#sm9",
                    "viewedAt": "2026-05-25T17:28:55+09:00",
                    "isMaybeLikeUserItem": False,
                    "video": {
                        "type": "essential",
                        "id": "sm9",
                        "title": "sample",
                        "registeredAt": "2007-03-06T00:33:00+09:00",
                        "count": {"view": 1, "comment": 1, "mylist": 1, "like": 1},
                        "thumbnail": {
                            "url": "https://example.com/thumb.jpg",
                            "middleUrl": None,
                            "largeUrl": None,
                            "listingUrl": "https://example.com/listing.jpg",
                            "nHdUrl": "https://example.com/nhd.jpg",
                        },
                        "duration": 1,
                        "shortDescription": "",
                        "latestCommentSummary": "",
                        "isChannelVideo": False,
                        "isPaymentRequired": False,
                        "playbackPosition": 0,
                        "owner": {
                            "ownerType": "user",
                            "type": "user",
                            "visibility": "visible",
                            "id": "1",
                            "name": "sample",
                            "iconUrl": None,
                        },
                        "requireSensitiveMasking": False,
                        "videoLive": None,
                        "isMuted": False,
                    },
                },
            ],
            "nextCursor": None,
        },
    }
    response = NvAPIResponse[HistoryData].model_validate(payload)

    assert response.data is not None
    assert response.data.total_count is None
    assert response.data.items[0].item_id == "h#20260525#sm9"
    assert response.data.items[0].viewed_at == "2026-05-25T17:28:55+09:00"


def test_following_mylists_accept_deleted_items_and_last_comment_time_sort() -> None:
    """Following mylists may contain deleted rows without detail."""
    payload = {
        "meta": {"status": 200},
        "data": {
            "followLimit": 100,
            "mylists": [
                {"id": 1, "status": "deleted"},
                {
                    "id": 2,
                    "status": "public",
                    "detail": {
                        "id": 2,
                        "isPublic": True,
                        "name": "sample",
                        "description": "",
                        "decoratedDescriptionHtml": "",
                        "defaultSortKey": "lastCommentTime",
                        "defaultSortOrder": "desc",
                        "itemsCount": 0,
                        "owner": {
                            "ownerType": "user",
                            "type": "user",
                            "visibility": "visible",
                            "id": "1",
                            "name": "sample",
                            "iconUrl": None,
                        },
                        "sampleItems": [],
                        "followerCount": 0,
                        "createdAt": "2026-05-25T17:28:55+09:00",
                        "isFollowing": True,
                    },
                },
            ],
        },
    }
    response = NvAPIResponse[FollowingMylistsData].model_validate(payload)

    assert response.data is not None
    assert response.data.mylists[0].detail is None
    assert response.data.mylists[1].detail is not None
    assert response.data.mylists[1].detail.default_sort_key == "lastCommentTime"
