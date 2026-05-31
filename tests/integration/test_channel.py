"""Live channel API tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.integration.helpers import require

if TYPE_CHECKING:
    from niconico import NicoNico

pytestmark = pytest.mark.live


def test_channel_read_apis(live_client: NicoNico) -> None:
    """Exercise channel read API wrappers against live endpoints."""
    channels = require(live_client.channel.search.search_channels("niconico", limit=5), "channel search")

    assert require(live_client.channel.get_channel(str(channels[0].id_)), "channel")
