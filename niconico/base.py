# niconico.py - Base

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .niconico import NicoNico


class DictFromAttribute:

    _dfa = True

    def __init__(
        self, data: dict, dfa_class: Optional["DictFromAttribute"] = None
    ):
        self.data = data
        self.__dfa_class__ = dfa_class or [
            cls for cls in self.__class__.__mro__ if hasattr(cls, "_dfa")
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
    """クライアントクラスのベースクラスです。  
    ここでいうベースクラスはニコニコの各サービスのために用意するクライアントに使われるもので、 :class:`niconico.niconico.NicoNico` では使われません。

    Parameters
    ----------
    cookies : Cookies, optional
        リクエストを行う際に使用するクッキーです。
        指定しない場合は :func:`niconico.cookies.Cookies.guest` を実行して返ってきたものが使われます。"""

    if TYPE_CHECKING:
        niconico: NicoNico

    def log(self, type_: str, content: str, *args, **kwargs):
        """クラスの名前を使ってログ出力を行います。
        :attr:`niconico.niconico.NicoNico.logger` が使用されます。
        普通これは開発者が使います。

        Parameters
        ----------
        type_ : str
        content : str
        *args
        **kwargs"""
        return getattr(self.niconico.logger, type_)(content, *args, **kwargs)

    def __init__(self, niconico: NicoNico):
        self.niconico = niconico