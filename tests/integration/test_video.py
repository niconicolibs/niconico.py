"""Live video API tests."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from tests.integration.helpers import (
    SM9_OWNER_NAME,
    SM9_TITLE,
    SM9_VIDEO_ID,
    get_sample_list_id,
    get_sm9_watch_data,
    get_tag_edit_key,
    mutation_cooldown,
    require,
)

if TYPE_CHECKING:
    from niconico import NicoNico

pytestmark = pytest.mark.live

MIN_SM9_DOWNLOAD_BYTES = 1_000_000


def test_sm9_metadata(live_client: NicoNico) -> None:
    """Fetch stable sm9 title, owner name, and tags from live APIs."""
    video = require(live_client.video.get_video(SM9_VIDEO_ID), "sm9 video")
    watch_data = get_sm9_watch_data(live_client)

    assert video.id_ == SM9_VIDEO_ID
    assert video.title == SM9_TITLE
    assert video.owner.name == SM9_OWNER_NAME
    videos = live_client.video.get_videos([SM9_VIDEO_ID, "sm1097445"])
    assert [item.id_ for item in videos] == [SM9_VIDEO_ID, "sm1097445"]
    assert watch_data.video.id_ == SM9_VIDEO_ID
    assert watch_data.video.title == SM9_TITLE
    assert watch_data.owner is not None
    assert watch_data.owner.nickname == SM9_OWNER_NAME
    assert any(tag.name == "陰陽師" for tag in watch_data.tag.items)


def test_video_read_apis(live_client: NicoNico) -> None:
    """Exercise video read API wrappers against live endpoints."""
    watch_data = get_sm9_watch_data(live_client)
    outputs = require(live_client.video.watch.get_outputs(watch_data), "sm9 outputs")
    output_ids = next(iter(outputs.values()))

    assert require(live_client.video.ranking.get_genres(), "genres")
    assert require(live_client.video.ranking.get_popular_tags("music_sound"), "popular tags")
    assert require(live_client.video.ranking.get_ranking("all", "24h", page_size=25), "ranking")
    assert require(live_client.video.ranking.get_hot_topics("24h", page_size=25), "hot topics")
    assert require(live_client.video.search.search_videos_by_keyword("VOCALOID", page_size=5), "keyword search")
    assert require(live_client.video.search.search_videos_by_tag("VOCALOID", page_size=5), "tag search")
    assert require(live_client.video.search.get_facet_by_keyword("VOCALOID"), "keyword facet")
    assert require(live_client.video.search.search_facet_by_tag("VOCALOID"), "tag facet")
    assert require(live_client.video.search.search_lists("VOCALOID", page_size=5), "list search")
    assert require(live_client.video.get_video_tags(SM9_VIDEO_ID, get_tag_edit_key(watch_data)), "sm9 tags")
    assert require(live_client.video.get_mylist(get_sample_list_id(live_client, "mylist"), page_size=5), "mylist")
    assert require(live_client.video.get_series(get_sample_list_id(live_client, "series"), page_size=5), "series")
    assert require(live_client.video.watch.generate_action_track_id(), "action track id")
    assert require(live_client.video.watch.get_hls_content_url(watch_data, [output_ids]), "HLS URL")
    assert require(live_client.video.watch.get_thread_key(SM9_VIDEO_ID), "thread key")
    assert require(live_client.video.watch.get_comments(watch_data), "comments")


def test_sm9_downloads_video(live_client: NicoNico, tmp_path: Path) -> None:
    """Download sm9 with the lowest available quality."""
    if shutil.which("ffmpeg") is None:
        pytest.skip("ffmpeg is required to run live download tests")
    watch_data = get_sm9_watch_data(live_client)
    outputs = require(live_client.video.watch.get_outputs(watch_data), "sm9 outputs")
    output_label = "低画質" if "低画質" in outputs else next(iter(outputs))

    output_path = live_client.video.watch.download_video(
        watch_data,
        output_label,
        str(tmp_path / "%(id)s.%(ext)s"),
    )
    downloaded = Path(output_path)

    assert downloaded.name == "sm9.mp4"
    assert downloaded.exists()
    assert downloaded.stat().st_size > MIN_SM9_DOWNLOAD_BYTES


def test_authenticated_video_like_apis(authenticated_client: NicoNico) -> None:
    """Exercise authenticated video like wrappers against live endpoints."""
    liked = False
    try:
        mutation_cooldown()
        like_data = authenticated_client.video.like_video(SM9_VIDEO_ID)
        liked = like_data is not None
        assert require(like_data, "like video") is not None
    finally:
        if liked:
            mutation_cooldown()
            assert authenticated_client.video.unlike_video(SM9_VIDEO_ID) is True
