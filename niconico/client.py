# niconico.py - Client

from typing import Optional

from .video import Client as VideoClient
from .cookies import Cookies


class NicoNico:
    def __init__(self, cookies: Optional[Cookies] = None):
        self.video = VideoClient(cookies)