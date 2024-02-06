import re

from pages.base_page import Page


def clean_team(team):
    team = re.sub(r"\d\d\d\d", "#Y#", team)
    team = re.sub("#Y#-#Y#", "", team)
    team = re.sub("#Y#", "", team)
    team = team.replace(",", "")

    return team.strip()


class PlayerPage(Page):
    def team_names(self):
        teams_el = self.doc.find(**{"class": "uni_holder"})
        for box in teams_el.find_all("a"):
            yield clean_team(box.attrs["data-tip"])
