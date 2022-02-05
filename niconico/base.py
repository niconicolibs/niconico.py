# niconico.py - Base

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, Type, Optional

if TYPE_CHECKING:
    from .niconico import NicoNico


__all__ = ("DictFromAttribute", "BaseClient")


SuperT = TypeVar("SuperT")
class DictFromAttribute(Generic[SuperT]):
    """辞書を属性からアクセスできるようにするものです。
    属性からアクセスされた際に返すものもこのクラスのインスタンスです。
    niconico.pyでのほとんどのニコニコのデータはこのクラスのインスタンスに格納されます。

    Parameters
    ----------
    data : dict
        属性でアクセスされた際に返すべき値がある辞書です。
    super_ : SuperT
        属性からアクセスされた際に返すインスタンスに渡すものです。

    Attributes
    ----------
    __data__ : dict
        インスタンス化時に引数の ``data`` に渡された辞書が入っています。

        Notes
        -----
        データに属性からではない方法でアクセスしたい場合はこれを使用しましょう。
        また、生のデータを取得したい場合はこちらを使用してください。
    __super__ : SuperT
        インスタンス化時に引数の ``super_`` に渡されたオブジェクトです。
        ニコニコのデータの場合はそのデータの提供元(例：ニコニコ動画)のクライアント用クラスのインスタンスが入ります。"""

    __dfa_class__: Type[DictFromAttribute]

    def __init__(self, data: dict, super_: SuperT):
        self.__data__, self.__super__ = data, super_

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
            return self._from_data(self.__data__[key], self.__super__)
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