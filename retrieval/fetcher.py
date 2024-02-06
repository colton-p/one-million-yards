import logging
import os.path
import time
import urllib.parse

import requests


def url_key(url):
    o = urllib.parse.urlparse(url)
    parts = [
        o.netloc,
        o.path.replace("/", "-").strip("-"),
        o.query.replace("&", "-")
    ]

    return "-".join(parts)


class Fetcher:
    _instance = None

    @classmethod
    def get(cls, url, force=False):
        if cls._instance is None:
            cls._instance = Fetcher()
        return cls._instance.fetch(url, force=force)

    def __init__(self, delay=6) -> None:
        self.last_get = 0
        self.delay = delay

    def _wait(self):
        since_last = time.time() - self.last_get
        if since_last > self.delay:
            return

        to_wait = int(1 + self.delay - since_last)
        logging.info("... waiting %s", to_wait)
        time.sleep(to_wait)

    def _get(self, url):
        logging.info("get url: %s", url)
        self._wait()
        self.last_get = time.time()
        return requests.get(url, timeout=20).text

    def fetch(self, url, force=False):
        path = f".cache/{url_key(url)}"
        if os.path.exists(path) and not force:
            return open(path, "r", encoding="utf8").read()

        result = self._get(url)

        with open(path, "w", encoding="utf8") as fp:
            fp.write(result)

        return result
