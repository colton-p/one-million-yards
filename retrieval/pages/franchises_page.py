from functools import cached_property

from pages.base_page import Page


class FranchisesPage(Page):
    table_id = None
    franch_stat = "franch_name"
    team_stat = "team_name"

    @cached_property
    def table(self):
        return self.doc.find(id=self.table_id)

    def _is_franchise_row(self, tr):
        return "full_table" in tr.attrs.get("class", [])

    def _is_alternate_row(self, tr):
        return "partial_table" in tr.attrs.get("class", [])

    def _alternate_name(self, tr):
        return tr.find(**{"data-stat": self.team_stat}).text

    def franchises(self):
        return {
            tr.find(**{"data-stat": self.franch_stat}).text
            for tr in self.table.find_all("tr")
            if self._is_franchise_row(tr)
        }

    def team_names(self):
        alt_names = {}
        franchise = None
        for tr in self.table.find_all("tr"):
            if self._is_franchise_row(tr):
                franchise = tr.find(**{"data-stat": self.franch_stat}).text
                alt_names[franchise] = franchise
            elif self._is_alternate_row(tr):
                alternate = self._alternate_name(tr)
                alt_names[alternate] = franchise

        return alt_names


class NflFranchises(FranchisesPage):
    table_id = "teams_active"
    franch_stat = "team_name"

    def _is_franchise_row(self, tr):
        return tr.attrs.get("class", []) == []


class MlbFranchises(FranchisesPage):
    table_id = "teams_active"
    franch_stat = "franchise_name"
    team_stat = "alternate_names"

    def _is_franchise_row(self, tr):
        return tr.attrs.get("class", []) == []

    def _is_alternate_row(self, tr):
        return super()._is_alternate_row(tr) and tr.find(**{"class": "alternate_names"})

    def _alternate_name(self, tr):
        return tr.find(**{"class": "alternate_names"}).text

    def team_names(self):
        def _clean_teams(alt_names):
            alt_names = alt_names.replace("Also played as", "")
            alt_names = alt_names.replace(" and ", ", ")
            alt_names = alt_names.split(",")
            return [name.strip() for name in alt_names]

        unparsed = super().team_names()
        ret = {}
        for alt_names, franch in unparsed.items():
            for name in _clean_teams(alt_names):
                if name in ret:
                    # TODO: fix repeated team names
                    continue
                ret[name] = franch
        return ret


class NbaFranchises(FranchisesPage):
    table_id = "teams_active"


class NhlFranchises(FranchisesPage):
    table_id = "active_franchises"
