"""This module provides a class that represents a channel client."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from niconico.base.client import BaseClient
from niconico.objects.channel import ChannelData, ChAPIResponse

if TYPE_CHECKING:
    from niconico.niconico import NicoNico


class ChannelClient(BaseClient):
    """A client that represents a channel client."""

    def __init__(self, niconico: NicoNico) -> None:
        """Initialize the client."""
        super().__init__(niconico)

    def get_channel(self, channel_id: str) -> ChannelData | None:
        """Get a channel."""
        channel_id = channel_id.replace("ch", "")
        res = self.niconico.get(f"https://public-api.ch.nicovideo.jp/v2/open/channels/{channel_id}")
        if res.status_code == requests.codes.ok:
            res_cls = ChAPIResponse[ChannelData](**res.json())
            if res_cls.data is not None:
                return res_cls.data
        return None
