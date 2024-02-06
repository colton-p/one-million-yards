from functools import cached_property
import unicodedata

from bs4 import BeautifulSoup

from pages.base_page import Page


def clean_name(name):
    nfkd_form = unicodedata.normalize("NFKD", name)
    name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    name = name.strip("+")
    name = name.translate(
        {
            0x2005: " ",
        }
    )
    return name


class LeadersPage(Page):
    table_id = None

    def player_el(self, row):
        raise NotImplementedError

    def stat_el(self, row):
        raise NotImplementedError

    @staticmethod
    def cls_for_league(league):
        return {
            "nba": NbaLeaders,
            "nfl": NflLeaders,
            "nhl": NhlLeaders,
            "mlb": MlbLeaders,
        }[league]

    @cached_property
    def base_url(self):
        meta_el = self.doc.find("meta", itemprop="url")
        return meta_el.attrs["content"]

    @cached_property
    def table(self):
        return self.doc.find(id=self.table_id)

    def table_rows(self):
        for tr in self.table.find_all("tr"):
            if not tr.td:
                continue
            yield tr

    def name(self, row):
        return clean_name(self.player_el(row).a.text)

    def url(self, row):
        path = self.player_el(row).a.attrs["href"]
        return f"{self.base_url}{path}"

    def stat(self, row):
        return int(self.stat_el(row).text.replace(",", ""))

    def code(self, row):
        url = self.url(row)
        return url.split("/")[-1].split(".")[0]


class NflLeaders(LeadersPage):
    def __init__(self, doc: BeautifulSoup, table_id=""):
        self.table_id = table_id
        super().__init__(doc)

    def player_el(self, row):
        return row.find(**{"data-stat": "player"})

    def stat_el(self, row):
        # return row.find(**{'data-stat': 'pass_yds'})
        return (row.find_all("td"))[1]


class MlbLeaders(LeadersPage):
    def __init__(self, doc: BeautifulSoup, table_id=""):
        self.table_id = table_id
        super().__init__(doc)

    def player_el(self, row):
        return (row.find_all("td"))[1]

    def stat_el(self, row):
        return row.find_all("td")[2]


class NbaLeaders(LeadersPage):
    table_id = "nba"

    def player_el(self, row):
        return row.find_all("td")[1]

    def stat_el(self, row):
        return row.find_all("td")[2]


class NhlLeaders(LeadersPage):
    table_id = "stats_career_NHL"

    def player_el(self, row):
        return row.find_all("td")[1]

    def stat_el(self, row):
        return row.find_all("td")[3]
