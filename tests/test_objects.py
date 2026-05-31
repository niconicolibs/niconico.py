"""Tests for response object models."""

from __future__ import annotations

from niconico.objects.nvapi import NvAPIResponse, RelationshipUsersData


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
