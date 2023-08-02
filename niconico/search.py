# niconico.py - Search
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from niconico import NicoNico


class SearchClient:
    "スナップショットAPIを利用するためのクライアントです"
    APIURL = "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
    def __init__(self, client):
        self.__client = client
        
    def search(self, keyword: str, *,
               sort: str="-viewCounter", targets: List[str]=["title"],
              fields: List[str]=["contentId", "title", "viewCounter"]):
        """ニコニコ動画の動画をスナップショットAPIを利用して検索します。
        Parameters
        ----------
        keyword : str
            検索キーワード
        sort : str
            ソート方式
        targets : List[str]
        fields : List[str]"""
        query = {
            "q": keyword,
            "_sort": sort,
            "targets": ",".join(target for target in targets),
            "fields": ",".join(field for field in fields)
        }
        return self.__client.request("GET", self.APIURL, params=query).json()
