"""A module to interact with the NicoNico API."""

from __future__ import annotations

from logging import Logger, getLogger

import requests

from niconico.channel import ChannelClient
from niconico.exceptions import LoginFailureError
from niconico.user import UserClient
from niconico.video import VideoClient

logger = getLogger("niconico.py")


class NicoNico:
    """A class to interact with the NicoNico API."""

    logger: Logger
    session: requests.Session
    logined: bool
    premium: bool

    video: VideoClient
    user: UserClient
    channel: ChannelClient

    def __init__(self) -> None:
        """Initialize the class."""
        self.logger = logger
        self.session = requests.Session()
        self.logined = False
        self.video = VideoClient(self)
        self.user = UserClient(self)
        self.channel = ChannelClient(self)

    def get(self, url: str) -> requests.Response:
        """Send a GET request to a URL.

        Args:
            url (str): The URL to send the request to.

        Returns:
            requests.Response: The response object.
        """
        headers = {
            "User-Agent": "niconico.py",
            "X-Frontend-Id": "6",
            "X-Frontend-Version": "0",
        }
        return self.session.get(url, headers=headers)

    def post(
        self,
        url: str,
        *,
        data: any | None = None,  # type: ignore[valid-type]
        json: object | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send a POST request to a URL.

        Args:
            url (str): The URL to send the request to.
            data (any): The data to send with the request.
            json (object): The data to send with the request.
            headers (dict[str, str]): The headers to send with the request.

        Returns:
            requests.Response: The response object.
        """
        req_headers = {
            "User-Agent": "niconico.py",
            "X-Frontend-Id": "6",
            "X-Frontend-Version": "0",
            "X-Niconico-Language": "ja-jp",
            "X-Client-Os-Type": "others",
            "X-Request-With": "https://www.nicovideo.jp",
            "Referer": "https://www.nicovideo.jp/",
        }
        if headers is not None:
            req_headers.update(headers)
        if json is None:
            return self.session.post(url, headers=req_headers, data=data)
        return self.session.post(url, headers=req_headers, json=json)

    def login_with_mail(self, mail: str, password: str, mfa: str | None = None) -> None:
        """Login to NicoNico with a mail and password.

        Args:
            mail (str): The mail to login with.
            password (str): The password to login with.
            mfa (str | None): The MFA code to login with. Defaults to None.
        """
        self.logined = False

        res = self.session.post(
            "https://account.nicovideo.jp/login/redirector?site=niconico&next_url=%2F",
            data={
                "mail_tel": mail,
                "password": password,
                "auth_id": "1158188129",
            },
        )

        if "/login" in res.url:
            raise LoginFailureError(message="Login failed")

        if "/mfa" in res.url:
            if mfa is None:
                raise LoginFailureError(message="MFA is required")
            res = self.session.post(
                res.url,
                data={
                    "otp": mfa,
                    "device_name": "niconico.py",
                },
            )

        if res.url != "https://www.nicovideo.jp/":
            raise LoginFailureError(message="Login failed")

        if res.headers.get("x-niconico-authflag") == "1":
            self.premium = False
        elif res.headers.get("x-niconico-authflag") == "3":
            self.premium = True
        else:
            raise LoginFailureError(message="Login failed")

        self.logined = True

    def login_with_session(self, session: str) -> None:
        """Login to NicoNico with a session.

        Args:
            session (str): The session to login with.
        """
        self.logined = False

        self.session.cookies.set("user_session", session)

        res = self.session.get("https://www.nicovideo.jp/")

        if res.url != "https://www.nicovideo.jp/":
            raise LoginFailureError(message="Login failed")

        if res.headers.get("x-niconico-authflag") == "1":
            self.premium = False
        elif res.headers.get("x-niconico-authflag") == "3":
            self.premium = True
        else:
            raise LoginFailureError(message="Login failed")

        self.logined = True

    def get_user_session(self) -> str | None:
        """Get the user session.

        Returns:
            str: The user session.
        """
        return self.session.cookies.get("user_session")
