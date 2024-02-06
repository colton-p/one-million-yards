import argparse
from collections import defaultdict
from functools import cached_property
import logging
import json
import yaml

from pages.leaders_page import LeadersPage
from pages.player_page import PlayerPage

FRANCHISE_MAP = yaml.load(open("output/franchises.yml", "r"), Loader=yaml.Loader)


class FactsBuilder:
    def __init__(self, spec, limit=None) -> None:
        self.spec = spec
        self.limit = limit

    @cached_property
    def page(self):
        cls = LeadersPage.cls_for_league(self.spec["league"])
        kwargs = {}
        if "table_id" in self.spec:
            kwargs = {"table_id": self.spec.get("table_id", None)}
        return cls.from_url(self.spec["url"], **kwargs)

    @cached_property
    def _players(self):
        def _player_iter():
            team_map = FRANCHISE_MAP[self.spec["league"]]
            for ix, row in enumerate(self.page.table_rows()):
                if self.limit and ix + 1 > self.limit:
                    break

                name, stat = self.page.name(row), self.page.stat(row)
                logging.info("%d: %s", ix + 1, name)
                url = self.page.url(row)
                # TODO: make this two passes: x -> player pages -> name, stat, teams
                player_page = PlayerPage.from_url(url)
                clean_teams = sorted(
                    {team_map[t] for t in player_page.team_names() if t in team_map}
                )
                yield (name, stat, list(clean_teams))

        return [x for x in _player_iter()]

    def scores(self):
        return {name: stat for (name, stat, _) in self._players}

    def teams(self):
        all_teams = set()
        for _, _, teams in self._players:
            all_teams |= set(teams)
        return list(all_teams)

    def player_map(self):
        ret = defaultdict(set)
        for name, _, teams in self._players:
            for t in teams:
                ret[t] |= {name}
        return {team: tuple(names) for (team, names) in ret.items()}

    def output(self):
        return {
            "teams": self.teams(),
            "players": self.player_map(),
            "scores": self.scores(),
        }


def main(args):
    specs = yaml.load(open("input/leaders.yml", "r"), Loader=yaml.Loader)
    if args.spec_name and not args.all:
        specs = [
            spec
            for spec in specs
            if args.spec_name == f"{spec['league']}-{spec['stat']}"
        ]

    for spec in specs:
        builder = FactsBuilder(spec, limit=args.limit)
        spec_name = f"{spec['league']}-{spec['stat']}"
        filename = f"{spec_name}.json"
        logging.info(spec_name)
        with open(f"output/facts/{filename}", "w") as fp:
            json.dump(builder.output(), fp, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("spec_name", nargs="?", default=None)
    group.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=250)
    logging.basicConfig(level=logging.INFO)

    main(parser.parse_args())
