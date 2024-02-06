from fetcher import Fetcher

from bs4 import BeautifulSoup


class Page:
    def __init__(self, doc: BeautifulSoup):
        self.doc = doc

    @classmethod
    def from_url(cls, url, **kwargs):
        html = Fetcher.get(url)
        doc = BeautifulSoup(html, "html.parser")
        return cls(doc, **kwargs)
