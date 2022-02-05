# niconico.py - Utils


__all__ = ()


def parse_link(url: str) -> str:
    "URLがもしスマホ用の場合はPC版に修正します。"
    if "sp" in url:
        url = url.replace("sp", "www")
    return url