# niconico.py - Exceptions


__all__ = ("ExtractFailed","LoginFailureException")


class ExtractFailed(Exception):
    "情報取り出しに失敗した際に発生するエラーです。"
    pass

class LoginFailureException(Exception):
    """ログインの失敗を知らせる例外クラスです。"""
    pass