from typing import List

class SearchClient:
    APIURL = "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
    def __init__(self, client):
        self.__client = client
        
    def search(self, keyword: str, *,
               sort: str="-viewCounter", targets: List[str]=["title"],
              fields: List[str]=["contentId", "title", "viewCounter"]):
        query = {
            "q": keyword,
            "_sort": sort,
            "targets": ",".join(target for target in targets),
            "fields": ",".join(field for field in fields)
        }
        return self.__client.request(APIURL, params=query).json()
