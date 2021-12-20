# niconico.py - Base

from typing import TYPE_CHECKING, Union, Optional

from .cookies import Cookies

if TYPE_CHECKING:
    from .client import NicoNico


class DictFromAttribute:

    _dfa = True

    def __init__(
        self, data: dict, dfa_class: Optional["DictFromAttribute"] = None
    ):
        self.data = data
        self.__dfa_class__ = dfa_class or [
            cls for cls in self.__mro__ if hasattr(cls, "_dfa")
        ][0]

    @classmethod
    def _from_data(cls, data):
        if isinstance(data, dict):
            return cls(data)
        elif isinstance(data, list):
            return [cls._from_data(item) for item in data]
        else:
            return data

    def __getattr__(self, key: str):
        if key in self.data:
            return self._from_data(self.data[key])
        else:
            raise AttributeError(
                f"class '{self.__class__.__name__}' has no attributre '{key}'"
            )


class BaseClient:

    if TYPE_CHECKING:
        client: NicoNico

    def __init__(self, cookies: Optional[Cookies] = None):
        self.cookies = cookies