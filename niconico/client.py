# niconico.py - Client

from typing import Optional

import requests

from .video import Client as VideoClient
from .cookies import Cookies


class NicoNico:
    def __init__(self, cookies: Optional[Cookies] = None):
        self.video = VideoClient()
        self.cookies = cookies

    def request(self, *args, **kwargs) -> requests.Response:
        kwargs["cookies"] = self.cookies
        response = requests.request(*args, **kwargs)
        if self.cookies is None:
            self.cookies = Cookies.guest(response.cookies["nicosid"])
        return response