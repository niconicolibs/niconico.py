# niconico.py - Base

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, Type, Optional

if TYPE_CHECKING:
    from .niconico import NicoNico


SuperT = TypeVar("SuperT")
class DictFromAttribute(Generic[SuperT]):
    "辞書を属性からアクセスできるようにするものです。"

    __dfa_class__: Type[DictFromAttribute]

    def __init__(
        self, data: dict, super_: SuperT, *,
        dfa_class: Optional["DictFromAttribute"] = None
    ):
        self.__data__, self.super_ = data, super_

    @classmethod
    def _from_data(cls, data, super_: SuperT):
        if isinstance(data, dict):
            return cls.__dfa_class__(data, super_)
        elif isinstance(data, list):
            return [cls.__dfa_class__._from_data(item, super_) for item in data]
        else:
            return data

    def __getattr__(self, key: str):
        if key in self.__data__:
            return self._from_data(self.__data__[key], self.super_)
        else:
            raise AttributeError(
                f"class '{self.__class__.__name__}' has no attributre '{key}'"
            )
DictFromAttribute.__dfa_class__ = DictFromAttribute


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


Headers = "dict[str, str]"