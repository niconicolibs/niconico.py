"""Live user API tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.integration.helpers import SM9_VIDEO_ID, get_sample_user_id, require

if TYPE_CHECKING:
    from niconico import NicoNico

pytestmark = pytest.mark.live


def test_user_read_apis(live_client: NicoNico) -> None:
    """Exercise public user read API wrappers against live endpoints."""
    user_id = get_sample_user_id(live_client)

    assert require(live_client.user.search.search_users("niconico", page_size=5), "user search")
    assert require(live_client.user.get_user(user_id), "user")
    assert live_client.user.get_user_followers(user_id, page_size=5) is not None
    assert live_client.user.get_user_followings(user_id, page_size=5) is not None
    assert require(live_client.user.get_user_videos(user_id, page_size=5), "user videos")
    assert live_client.user.get_user_mylists(user_id, sample_item_count=1) is not None
    assert live_client.user.get_user_series(user_id, page_size=5) is not None


def test_authenticated_user_read_apis(authenticated_client: NicoNico) -> None:
    """Exercise authenticated user read API wrappers against live endpoints."""
    assert require(authenticated_client.user.get_own(), "own user")
    assert authenticated_client.user.get_own_followers(page_size=5) is not None
    assert authenticated_client.user.get_own_followings(page_size=5) is not None
    assert authenticated_client.user.get_own_videos(page_size=5) is not None
    assert authenticated_client.user.get_own_mylists(sample_item_count=1) is not None
    assert authenticated_client.user.get_own_series(page_size=5) is not None
    assert authenticated_client.user.get_own_following_mylists(sample_item_count=1) is not None
    assert authenticated_client.user.get_own_following_tags() is not None
    assert authenticated_client.user.get_following_activities() is not None
    assert require(
        authenticated_client.user.get_recommendations(
            "video_watch_recommendation",
            video_id=SM9_VIDEO_ID,
            limit=5,
        ),
        "recommendations",
    )


def test_authenticated_video_history_apis(authenticated_client: NicoNico) -> None:
    """Exercise authenticated video history wrappers against live endpoints."""
    assert authenticated_client.video.get_history(page_size=5) is not None
    assert authenticated_client.video.get_like_history(page_size=5) is not None
