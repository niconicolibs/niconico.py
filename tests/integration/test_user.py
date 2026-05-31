"""Live user API tests."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING
from uuid import uuid4

import pytest

from tests.integration.helpers import SM9_VIDEO_ID, get_sample_user_id, mutation_cooldown, require

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


@pytest.mark.mutating()
def test_authenticated_mylist_write_apis(authenticated_client: NicoNico) -> None:
    """Exercise own mylist write API wrappers against live endpoints."""
    if os.environ.get("NICONICO_MUTATING_LIVE_TESTS") != "1":
        pytest.skip("Set NICONICO_MUTATING_LIVE_TESTS=1 to run mutating live API tests")

    marker = f"niconico.py live test {uuid4().hex[:8]}"
    mutation_cooldown()
    source = require(
        authenticated_client.user.create_mylist(marker, "created by niconico.py live test", is_public=False),
        "source mylist creation",
    )
    source_id = str(source.mylist_id)
    target_id: str | None = None

    try:
        mutation_cooldown()
        updated = require(
            authenticated_client.user.update_mylist(
                source_id,
                name=f"{marker} updated",
                description="updated by niconico.py live test",
                is_public=False,
                default_sort_key="addedAt",
                default_sort_order="desc",
            ),
            "mylist metadata update",
        )
        assert updated.name == f"{marker} updated"
        mutation_cooldown()
        assert authenticated_client.user.add_mylist_item(source_id, SM9_VIDEO_ID, description="live test") is True

        detail = require(
            authenticated_client.user.get_own_mylist(source_id, page_size=5, sort_key="addedAt", sort_order="desc"),
            "own mylist detail",
        )
        assert any(item.watch_id == SM9_VIDEO_ID for item in detail.items)

        items = require(
            authenticated_client.user.get_own_mylist_items(
                source_id,
                sort_key="addedAt",
                sort_order="asc",
            ),
            "own mylist items",
        )
        assert any(item.watch_id == SM9_VIDEO_ID for item in items.items)

        mutation_cooldown()
        target = require(
            authenticated_client.user.create_mylist(
                f"{marker} copy",
                "created by niconico.py live test",
                is_public=False,
            ),
            "target mylist creation",
        )
        target_id = str(target.mylist_id)
        mutation_cooldown()
        copied = require(
            authenticated_client.user.copy_mylist_items(source_id, target_id, [SM9_VIDEO_ID]),
            "mylist item copy",
        )
        assert SM9_VIDEO_ID in copied.processed_ids or SM9_VIDEO_ID in copied.duplicated_ids

        mutation_cooldown()
        ordered = require(
            authenticated_client.user.reorder_mylists(
                [mylist.id_ for mylist in authenticated_client.user.get_own_mylists()],
            ),
            "mylist reorder",
        )
        assert int(source_id) in ordered.mylist_ids
        mutation_cooldown()
        assert authenticated_client.user.remove_mylist_items(source_id, [SM9_VIDEO_ID]) is True
    finally:
        if target_id is not None:
            mutation_cooldown()
            authenticated_client.user.delete_mylist(target_id)
        mutation_cooldown()
        authenticated_client.user.delete_mylist(source_id)
