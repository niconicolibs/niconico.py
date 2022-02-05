# niconico.py - Exceptions


__all__ = ("ExtractFailed",)


class ExtractFailed(Exception):
    "情報取り出しに失敗した際に発生するエラーです。"