"""A module to interact with the NicoNico API."""

from __future__ import annotations

import requests

from .exceptions import LoginFailureError


class NicoNico:
    """A class to interact with the NicoNico API."""

    session: requests.Session
    logined: bool

    def __init__(self) -> None:
        """Initialize the class."""
        self.session = requests.Session()
        self.logined = False

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

        if res.headers.get("x-niconico-authflag") not in ["1", "3"]:
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

        if res.headers.get("x-niconico-authflag") not in ["1", "3"]:
            raise LoginFailureError(message="Login failed")

        self.logined = True
