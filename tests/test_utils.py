"""Tests for utility helpers."""

from __future__ import annotations

from niconico.utils import add_optional_param, extract_video_id_from_url


def test_extract_video_id_from_url() -> None:
    """Video IDs are extracted from common watch URLs."""
    assert extract_video_id_from_url("https://www.nicovideo.jp/watch/sm9") == "sm9"
    assert extract_video_id_from_url("https://nico.ms/sm9") == "sm9"
    assert extract_video_id_from_url("watch/12345") == "12345"


def test_add_optional_param_skips_none_and_stringifies_values() -> None:
    """Optional params skip None and stringify scalar values."""
    query: dict[str, str] = {}

    add_optional_param(query, "limit", 10)
    add_optional_param(query, "empty", None)
    add_optional_param(query, "site", "nicovideo")

    assert query == {"limit": "10", "site": "nicovideo"}
