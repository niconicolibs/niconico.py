"""Fixtures for live integration tests."""

from __future__ import annotations

import os

import pytest

from niconico import NicoNico
from niconico.exceptions import LoginFailureError


@pytest.fixture(scope="module")
def live_client() -> NicoNico:
    """Return a client for live tests."""
    if os.environ.get("NICONICO_LIVE_TESTS") != "1":
        pytest.skip("Set NICONICO_LIVE_TESTS=1 to run live API tests")
    return NicoNico()


@pytest.fixture(scope="module")
def authenticated_client(live_client: NicoNico) -> NicoNico:
    """Return an authenticated client for live tests."""
    session = os.environ.get("NICONICO_USER_SESSION")
    if session:
        try:
            live_client.login_with_session(session)
        except LoginFailureError:
            pass
        else:
            return live_client

    mail = os.environ.get("NICONICO_TEST_EMAIL")
    password = os.environ.get("NICONICO_TEST_PASSWORD")
    if mail and password:
        try:
            live_client.login_with_mail(mail, password)
        except LoginFailureError:
            pass
        else:
            return live_client

    if not mail or not password:
        pytest.skip(
            "Set NICONICO_USER_SESSION or NICONICO_TEST_EMAIL and NICONICO_TEST_PASSWORD "
            "to run authenticated live API tests",
        )
    pytest.fail("NICONICO_USER_SESSION and NICONICO_TEST_EMAIL login both failed", pytrace=False)
    return live_client
