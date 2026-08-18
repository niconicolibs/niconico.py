"""A module to interact with the NicoNico API."""

from __future__ import annotations

import time
import warnings
from contextlib import contextmanager
from logging import Logger, getLogger
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import requests

from niconico.channel import ChannelClient
from niconico.exceptions import LoginFailureError
from niconico.user import UserClient
from niconico.video import VideoClient

if TYPE_CHECKING:
    from collections.abc import Iterator

    from playwright.sync_api import BrowserContext, Page

logger = getLogger("niconico.py")

LOGIN_PAGE_URL = "https://account.nicovideo.jp/login"
SESSION_COOKIE_NAME = "user_session"


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
            Use :meth:`login_with_browser` to sign in interactively, or
            :meth:`login_with_session` if you already hold a session token.

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
            "human. Use login_with_browser() to sign in interactively, or login_with_session() "
            "with a user_session token."
        )
        warnings.warn(message, DeprecationWarning, stacklevel=2)
        raise LoginFailureError(message=message)

    def login_with_browser(
        self,
        mail: str | None = None,
        password: str | None = None,
        *,
        timeout: float = 300.0,
        user_data_dir: str | None = None,
        headless: bool = False,
    ) -> None:
        """Login to NicoNico by completing the login form in a real browser.

        Opens the NicoNico login page with Playwright and waits until you have
        signed in, then picks up the resulting session token. When ``mail`` and
        ``password`` are given the form is filled in for you, but you still have
        to solve the bot challenge and submit the form yourself.

        Requires the optional ``browser`` extra::

            pip install "niconico.py[browser]"
            playwright install chromium

        Args:
            mail (str | None): The mail to prefill. Left blank when None.
            password (str | None): The password to prefill. Left blank when None.
            timeout (float): How long to wait for the login to complete, in seconds.
            user_data_dir (str | None): A directory to persist the browser profile in.
                Reusing a profile keeps you signed in and makes the bot challenge less
                likely to fail. A throwaway profile is used when None.
            headless (bool): Whether to run the browser headless. The bot challenge
                usually fails without a visible browser, so leave this False.

        Raises:
            LoginFailureError: If the login did not complete within the timeout.
        """
        with self._browser_page(user_data_dir=user_data_dir, headless=headless) as (context, page):
            page.goto(LOGIN_PAGE_URL)
            self._prefill_login_form(page, mail, password)
            self.logger.info("Waiting for the login to be completed in the browser.")
            session = self._wait_for_session_cookie(context, timeout=timeout)
        if session is None:
            raise LoginFailureError(message="Login was not completed before the timeout expired")
        self.login_with_session(session)

    @contextmanager
    def _browser_page(self, *, user_data_dir: str | None, headless: bool) -> Iterator[tuple[BrowserContext, Page]]:
        """Open a Playwright browser context and yield it together with a blank page."""
        try:
            from playwright.sync_api import sync_playwright  # noqa: PLC0415
        except ImportError as e:  # pragma: no cover - depends on optional extra
            raise LoginFailureError(
                message=(
                    "login_with_browser requires Playwright. Install it with "
                    '`pip install "niconico.py[browser]"` and `playwright install chromium`.'
                ),
            ) from e
        with sync_playwright() as playwright:
            if user_data_dir is not None:
                context = playwright.chromium.launch_persistent_context(user_data_dir, headless=headless)
                page = context.pages[0] if context.pages else context.new_page()
                try:
                    yield context, page
                finally:
                    context.close()
                return
            browser = playwright.chromium.launch(headless=headless)
            context = browser.new_context()
            try:
                yield context, context.new_page()
            finally:
                browser.close()

    @staticmethod
    def _prefill_login_form(page: Page, mail: str | None, password: str | None) -> None:
        """Fill the login form when credentials were supplied, ignoring layout changes."""
        for selector, value in (("input#mail_tel", mail), ("input#password", password)):
            if value is None:
                continue
            try:
                page.fill(selector, value, timeout=5000)
            except Exception:  # noqa: BLE001 - the form is free to change, the user can still type
                logger.debug("Could not prefill %s; fill it in manually.", selector)

    @staticmethod
    def _wait_for_session_cookie(context: BrowserContext, *, timeout: float) -> str | None:
        """Poll the browser context until the session cookie shows up."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            for cookie in context.cookies():
                value = cookie.get("value")
                if cookie.get("name") == SESSION_COOKIE_NAME and value:
                    return str(value)
            time.sleep(1.0)
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
