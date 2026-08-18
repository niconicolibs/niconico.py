"""A module to interact with the NicoNico API."""

from __future__ import annotations

import warnings
from logging import Logger, getLogger
from typing import TYPE_CHECKING, cast
from urllib.parse import urlparse

import requests

from niconico.channel import ChannelClient
from niconico.exceptions import LoginFailureError
from niconico.user import UserClient
from niconico.video import VideoClient

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = getLogger("niconico.py")

SESSION_COOKIE_NAME = "user_session"
COOKIE_DOMAIN = "nicovideo.jp"


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

    def get(self, url: str, *, headers: dict[str, str] | None = None) -> requests.Response:
        """Send a GET request to a URL.

        Args:
            url (str): The URL to send the request to.
            headers (dict[str, str] | None): Additional headers to send with the request.

        Returns:
            requests.Response: The response object.
        """
        parsed_url = urlparse(url)
        req_headers = {
            "User-Agent": "niconico.py",
            "X-Frontend-Id": "6",
            "X-Frontend-Version": "0",
            "Host": parsed_url.netloc,
        }
        if headers is not None:
            req_headers.update(headers)
        return self.session.get(url, headers=req_headers)

    def post(
        self,
        url: str,
        *,
        data: dict[str, str] | str | bytes | None = None,
        json: object | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send a POST request to a URL.

        Args:
            url (str): The URL to send the request to.
            data (dict[str, str] | str | bytes): The data to send with the request.
            json (object): The data to send with the request.
            headers (dict[str, str]): The headers to send with the request.

        Returns:
            requests.Response: The response object.
        """
        parsed_url = urlparse(url)
        req_headers = {
            "User-Agent": "niconico.py",
            "X-Frontend-Id": "6",
            "X-Frontend-Version": "0",
            "X-Niconico-Language": "ja-jp",
            "X-Client-Os-Type": "others",
            "X-Request-With": "https://www.nicovideo.jp",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.nicovideo.jp",
            "Referer": "https://www.nicovideo.jp/",
            "Host": parsed_url.netloc,
        }
        if headers is not None:
            req_headers.update(headers)
        if json is None:
            return self.session.post(url, headers=req_headers, data=data)
        return self.session.post(url, headers=req_headers, json=json)

    def put(
        self,
        url: str,
        *,
        data: dict[str, str] | str | bytes | None = None,
        json: object | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send a PUT request to a URL.

        Args:
            url (str): The URL to send the request to.
            data (dict[str, str] | str | bytes): The data to send with the request.
            json (object): The JSON data to send with the request.
            headers (dict[str, str]): The headers to send with the request.

        Returns:
            requests.Response: The response object.
        """
        parsed_url = urlparse(url)
        req_headers = {
            "User-Agent": "niconico.py",
            "X-Frontend-Id": "6",
            "X-Frontend-Version": "0",
            "X-Niconico-Language": "ja-jp",
            "X-Client-Os-Type": "others",
            "X-Request-With": "https://www.nicovideo.jp",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.nicovideo.jp",
            "Referer": "https://www.nicovideo.jp/",
            "Host": parsed_url.netloc,
        }
        if headers is not None:
            req_headers.update(headers)
        if json is None:
            return self.session.put(url, headers=req_headers, data=data)
        return self.session.put(url, headers=req_headers, json=json)

    def delete(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send a DELETE request to a URL.

        Args:
            url (str): The URL to send the request to.
            headers (dict[str, str]): The headers to send with the request.

        Returns:
            requests.Response: The response object.
        """
        parsed_url = urlparse(url)
        req_headers = {
            "User-Agent": "niconico.py",
            "X-Frontend-Id": "6",
            "X-Frontend-Version": "0",
            "X-Niconico-Language": "ja-jp",
            "X-Client-Os-Type": "others",
            "X-Request-With": "https://www.nicovideo.jp",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.nicovideo.jp",
            "Referer": "https://www.nicovideo.jp/",
            "Host": parsed_url.netloc,
        }
        if headers is not None:
            req_headers.update(headers)
        return self.session.delete(url, headers=req_headers)

    def login_with_mail(self, mail: str, password: str, mfa: str | None = None) -> None:
        """Login to NicoNico with a mail and password.

        .. deprecated::
            NicoNico moved account authentication to a SPA protected by a bot
            challenge, and the endpoint this method posted to no longer exists.
            Use :meth:`login_with_browser_cookies` to reuse a browser you are already
            signed in with, or :meth:`login_with_session` if you already hold a token.

        Args:
            mail (str): The mail to login with.
            password (str): The password to login with.
            mfa (str | None): The MFA code to login with. Defaults to None.

        Raises:
            LoginFailureError: Always, because the endpoint was removed.
        """
        _ = mail, password, mfa
        message = (
            "login_with_mail is no longer supported: the login endpoint was removed and "
            "the login form is now protected by a bot challenge that has to be solved by a "
            "human. Use login_with_browser_cookies() to reuse a signed-in browser, or login_with_session() "
            "with a user_session token."
        )
        warnings.warn(message, DeprecationWarning, stacklevel=2)
        raise LoginFailureError(message=message)

    def login_with_browser_cookies(self, browser: str | None = None) -> None:
        """Login to NicoNico by importing the session cookie from a browser.

        Signing in through the website is the only supported way to authenticate,
        because the login form is protected by a bot challenge. This reads the
        ``user_session`` cookie held by a browser you are already signed in with,
        so no credentials pass through this library.

        Requires the optional ``browser`` extra::

            pip install "niconico.py[browser]"

        Args:
            browser (str | None): The browser to read the cookie from, for example
                ``"chrome"`` or ``"firefox"``. Every supported browser is tried when None.

        Raises:
            LoginFailureError: If the cookies could not be read, or no browser is
                signed in to NicoNico.
        """
        cookies = self._load_browser_cookies(browser)
        session = self._extract_session_cookie(cookies)
        if session is None:
            raise LoginFailureError(
                message=(
                    "No NicoNico session was found in the browser. Sign in at "
                    "https://www.nicovideo.jp/ first, then try again."
                ),
            )
        self.login_with_session(session)

    @staticmethod
    def _load_browser_cookies(browser: str | None) -> Iterable[object]:
        """Read the NicoNico cookies a browser holds."""
        try:
            import browser_cookie3  # noqa: PLC0415
        except ImportError as e:  # pragma: no cover - depends on the optional extra
            raise LoginFailureError(
                message=(
                    "login_with_browser_cookies requires browser-cookie3. Install it with "
                    '`pip install "niconico.py[browser]"`.'
                ),
            ) from e
        loader = browser_cookie3.load if browser is None else getattr(browser_cookie3, browser, None)
        if loader is None or not callable(loader):
            raise LoginFailureError(message=f"Unsupported browser: {browser}")
        try:
            return cast("Iterable[object]", loader(domain_name=COOKIE_DOMAIN))
        except Exception as e:
            raise LoginFailureError(message=f"Could not read cookies from the browser: {e}") from e

    @staticmethod
    def _extract_session_cookie(cookies: Iterable[object]) -> str | None:
        """Pick the session cookie out of a cookie jar."""
        for cookie in cookies:
            value = getattr(cookie, "value", None)
            if getattr(cookie, "name", None) == SESSION_COOKIE_NAME and value:
                return str(value)
        return None


    def login_with_session(self, session: str) -> None:
        """Login to NicoNico with a session.

        Args:
            session (str): The session to login with.
        """
        self.logined = False

        self.session.cookies.set("user_session", session)

        res = self.session.get("https://www.nicovideo.jp/")

        if res.url != "https://www.nicovideo.jp/":
            self.session.cookies.clear("", "/", "user_session")
            raise LoginFailureError(message="Login failed")

        if res.headers.get("x-niconico-authflag") == "1":
            self.premium = False
        elif res.headers.get("x-niconico-authflag") == "3":
            self.premium = True
        else:
            self.session.cookies.clear("", "/", "user_session")
            raise LoginFailureError(message="Login failed")

        self.logined = True

    def get_user_session(self) -> str | None:
        """Get the user session.

        Returns:
            str: The user session.
        """
        return self.session.cookies.get("user_session")

    def logout(self) -> None:
        """Logout from NicoNico.

        Properly logs out by calling logout endpoint and clearing session data.
        Updates authentication state to reflect logged out status.
        """
        if self.logined:
            self.session.get("https://account.nicovideo.jp/logout")
            self.session.cookies.clear("", "/", "user_session")
            self.logined = False
            self.premium = False
            self.logger.debug("Logged out from NicoNico")
        else:
            self.logger.warning("Not logged in, cannot logout")
