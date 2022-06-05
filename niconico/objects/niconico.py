# niconico.py - Common

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, Literal, Optional, List, Any

from ..base import DictFromAttribute
from .__init__ import Unknown


__all__ = (
    "LoginFailureException"
)


class LoginFailureException(Exception):
    """ログインの失敗を知らせる例外クラスです。"""
    pass