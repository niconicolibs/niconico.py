"""Helpers for live integration tests."""

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from niconico import NicoNico
    from niconico.objects.video.watch import WatchData

SM9_VIDEO_ID = "sm9"
SM9_TITLE = "新・豪血寺一族 -煩悩解放 - レッツゴー！陰陽師"  # noqa: RUF001
SM9_OWNER_NAME = "中の"


def require(value: Any, label: str) -> Any:  # noqa: ANN401
    """Return a live API value, failing when it is absent."""
    assert value is not None, f"{label} returned None"
    assert not isinstance(value, dict | list | set | tuple) or value, f"{label} returned an empty collection"
    return value


def mutation_cooldown() -> None:
    """Wait between live test mutations when configured."""
    seconds = float(os.environ.get("NICONICO_MUTATION_COOLDOWN_SECONDS", "0"))
    if seconds > 0:
        time.sleep(seconds)


def get_sm9_watch_data(client: NicoNico) -> WatchData:
    """Return live watch data for sm9."""
    return require(client.video.watch.get_watch_data(SM9_VIDEO_ID), "sm9 watch data")


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
    video = require(client.video.get_video(SM9_VIDEO_ID), "sm9 video")
    if video.owner.id_ is not None:
        return str(video.owner.id_)
    users = require(client.user.search.search_users("niconico", page_size=5), "user search")
    return str(users.items[0].user.id_)


def get_sample_list_id(client: NicoNico, list_type: str) -> str:
    """Return a sample mylist or series ID."""
    lists = require(client.video.search.search_lists("VOCALOID", page_size=10, types=[list_type]), "list search")
    return str(lists.items[0].id_)
