"""Utility functions for niconico module."""

from __future__ import annotations

import re


def extract_video_id_from_url(url: str) -> str | None:
    """Extract video ID from URL.

    Args:
        url (str): URL to extract video ID from.

    Returns:
        str | None: Extracted video ID or None if not found.
    """
    match = re.search(r"(?:sm|nm|so)?\d+", url)
    if match:
        return match.group(0)
    return None
