import copy
import json
import random
import yaml


class Simulator:
    def __init__(self, data) -> None:
        data = copy.deepcopy(data)
        for t in data["players"]:
            ll = data["players"][t]
            data["players"][t] = sorted(ll, key=lambda p: -data["scores"][p])
        self.data = data

    def sim_one(self, k=5):
        seq = [random.choice(self.data["teams"]) for _ in range(k)]
        tot = 0
        done = set()
        for team in seq:
            for p in self.data["players"][team]:
                if p not in done:
                    done.add(p)
                    tot += self.data["scores"][p]
                    break
        return tot

    def avg_score(self, k=5, n=10_000):
        return sum(self.sim_one(k) for _ in range(n)) / n

    def pct_above(self, tgt, k=5, n=10_000):
        return sum(self.sim_one(k) > tgt for _ in range(n)) / n


def check_win_conditions():
    game_specs = yaml.load(open("input/game_specs.yml", "r"), Loader=yaml.Loader)

    for spec_name in game_specs:
        filename = f"output/facts/{spec_name}.json"
        data = json.load(open(filename, "r"))
        sim = Simulator(data)

        targets = game_specs[spec_name]["targets"]
        for rounds, target in targets.items():
            pct = sim.pct_above(target, k=rounds)
            avg = int(sim.avg_score(k=rounds))
            print(f"{pct:0.3f} {target:7d} {avg:7d} | {spec_name} {rounds}")


if __name__ == "__main__":
    check_win_conditions()
