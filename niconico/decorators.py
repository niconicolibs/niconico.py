"""Decorators for the niconico package."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from niconico.exceptions import LoginRequiredError, PremiumRequiredError

if TYPE_CHECKING:
    from niconico.base.client import BaseClient

F = TypeVar("F", bound=Callable[..., Any])


def login_required(*, premium: bool = False) -> Callable[[F], F]:
    """A decorator that requires a login to be performed."""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(self: BaseClient, *args: Any, **kwargs: Any) -> F:  # noqa: ANN401
            if not self.niconico.logined:
                raise LoginRequiredError(message="Login is required to use this function.")
            if premium and not self.niconico.premium:
                raise PremiumRequiredError(message="Premium account is required to use this function.")
            return func(self, *args, **kwargs)

        return wrapper  # type: ignore  # noqa: PGH003

    return decorator
