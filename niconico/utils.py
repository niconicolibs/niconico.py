# niconico.py - Utils

import requests

from .cookies import Cookies


def _set_cookies(self, response: requests.Response) -> None:
    # クッキーを渡されたselfに設定されていない場合のみselfに設定します。
    if self.cookies is None:
        self.client.cookies = self.cookies = Cookies.guest(
            response.cookies["nicosid"]
        )


def request(self, *args, **kwargs) -> requests.Response:
    response = requests.request(*args, **kwargs)
    _set_cookies(self, response)
    return response