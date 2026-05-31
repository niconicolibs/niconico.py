"""Live read-only API smoke tests."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import pytest

from niconico import NicoNico
from niconico.exceptions import LoginFailureError

if TYPE_CHECKING:
    from niconico.objects.video.watch import WatchData

pytestmark = pytest.mark.live


def require(value: Any, label: str) -> Any:  # noqa: ANN401
    """Return a live API value, failing when it is absent."""
    assert value is not None, f"{label} returned None"
    assert not isinstance(value, dict | list | set | tuple) or value, f"{label} returned an empty collection"
    return value


@pytest.fixture(scope="module")
def live_client() -> NicoNico:
    """Return a client for live tests."""
    if os.environ.get("NICONICO_LIVE_TESTS") != "1":
        pytest.skip("Set NICONICO_LIVE_TESTS=1 to run live API tests")
    return NicoNico()


@pytest.fixture(scope="module")
def authenticated_client(live_client: NicoNico) -> NicoNico:
    """Return an authenticated client for live read-only tests."""
    session = os.environ.get("NICONICO_USER_SESSION")
    if not session:
        pytest.skip("Set NICONICO_USER_SESSION to run authenticated live API tests")
    try:
        live_client.login_with_session(session)
    except LoginFailureError:
        pass
    else:
        return live_client
    pytest.fail("NICONICO_USER_SESSION is invalid or expired", pytrace=False)
    return live_client


def get_sample_video_id(client: NicoNico) -> str:
    """Return a current sample video ID from ranking data."""
    ranking = require(client.video.ranking.get_ranking("all", "24h", page_size=25), "ranking")
    return ranking.items[0].id_


def get_watch_data(client: NicoNico) -> WatchData:
    """Return current watch data for the sample video."""
    return require(client.video.watch.get_watch_data(get_sample_video_id(client)), "watch data")


def get_tag_edit_key(watch_data: WatchData) -> str:
    """Return a tag edit key from watch data."""
    edit_key = None
    if watch_data.tag.edit is not None:
        edit_key = watch_data.tag.edit.edit_key
    if edit_key is None and watch_data.tag.viewer is not None:
        edit_key = watch_data.tag.viewer.edit_key
    assert edit_key is not None, "tag edit key is unavailable"
    return edit_key


def get_sample_user_id(client: NicoNico) -> str:
    """Return a visible sample user ID."""
    video = require(client.video.get_video(get_sample_video_id(client)), "video")
    if video.owner.id_ is not None:
        return str(video.owner.id_)
    users = require(client.user.search.search_users("niconico", page_size=5), "user search")
    return str(users.items[0].user.id_)


def get_sample_list_id(client: NicoNico, list_type: str) -> str:
    """Return a sample mylist or series ID."""
    lists = require(client.video.search.search_lists("VOCALOID", page_size=10, types=[list_type]), "list search")
    return str(lists.items[0].id_)


def test_public_read_only_live_apis(live_client: NicoNico) -> None:
    """Exercise public read-only API wrappers against live endpoints."""
    video_id = get_sample_video_id(live_client)
    watch_data = get_watch_data(live_client)
    outputs = require(live_client.video.watch.get_outputs(watch_data), "outputs")
    output_ids = next(iter(outputs.values()))
    user_id = get_sample_user_id(live_client)
    channel = require(live_client.channel.search.search_channels("niconico", limit=5), "channel search")[0]

    assert live_client.get("https://www.nicovideo.jp/").ok
    assert require(live_client.video.ranking.get_genres(), "genres")
    assert require(live_client.video.ranking.get_popular_tags("music_sound"), "popular tags")
    assert require(live_client.video.ranking.get_hot_topics("24h", page_size=25), "hot topics")
    assert require(live_client.video.search.search_videos_by_keyword("VOCALOID", page_size=5), "keyword search")
    assert require(live_client.video.search.search_videos_by_tag("VOCALOID", page_size=5), "tag search")
    assert require(live_client.video.search.get_facet_by_keyword("VOCALOID"), "keyword facet")
    assert require(live_client.video.search.search_facet_by_tag("VOCALOID"), "tag facet")
    assert require(live_client.video.search.search_lists("VOCALOID", page_size=5), "list search")
    assert require(live_client.video.get_video(video_id), "video")
    assert require(live_client.video.get_video_tags(video_id, get_tag_edit_key(watch_data)), "video tags")
    assert require(live_client.video.get_mylist(get_sample_list_id(live_client, "mylist"), page_size=5), "mylist")
    assert require(live_client.video.get_series(get_sample_list_id(live_client, "series"), page_size=5), "series")
    assert require(live_client.video.watch.generate_action_track_id(), "action track id")
    assert require(live_client.video.watch.get_hls_content_url(watch_data, [output_ids]), "HLS URL")
    assert require(live_client.video.watch.get_thread_key(video_id), "thread key")
    assert require(live_client.video.watch.get_comments(watch_data), "comments")
    assert require(live_client.user.search.search_users("niconico", page_size=5), "user search")
    assert require(live_client.user.get_user(user_id), "user")
    assert live_client.user.get_user_followers(user_id, page_size=5) is not None
    assert live_client.user.get_user_followings(user_id, page_size=5) is not None
    assert require(live_client.user.get_user_videos(user_id, page_size=5), "user videos")
    assert live_client.user.get_user_mylists(user_id, sample_item_count=1) is not None
    assert live_client.user.get_user_series(user_id, page_size=5) is not None
    assert require(live_client.channel.get_channel(str(channel.id_)), "channel")


def test_authenticated_read_only_live_apis(authenticated_client: NicoNico) -> None:
    """Exercise authenticated read-only API wrappers against live endpoints."""
    video_id = get_sample_video_id(authenticated_client)

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
            video_id=video_id,
            limit=5,
        ),
        "recommendations",
    )
    assert authenticated_client.video.get_history(page_size=5) is not None
    assert authenticated_client.video.get_like_history(page_size=5) is not None
