import yaml

from pages.franchises_page import (
    NbaFranchises,
    NflFranchises,
    NhlFranchises,
    MlbFranchises,
)


def main():
    out = {}
    franchise_pages = [
        ("nba", "https://www.basketball-reference.com/teams/", NbaFranchises),
        ("nfl", "https://www.pro-football-reference.com/teams/", NflFranchises),
        ("nhl", "https://www.hockey-reference.com/teams/", NhlFranchises),
        ("mlb", "https://www.baseball-reference.com/teams/", MlbFranchises),
    ]
    for league, url, cls in franchise_pages:
        page = cls.from_url(url)
        out[league] = page.team_names()

    with open("output/franchises.yml", "w") as fp:
        yaml.dump(out, fp)


if __name__ == "__main__":
    main()
