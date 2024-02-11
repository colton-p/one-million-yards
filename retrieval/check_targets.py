import copy
import json
import random
import yaml

import networkx as nx

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

    def best_possible(self, k=5):
        G = nx.Graph()
        for t in self.data['teams']:
            for s in self.data['players'][t]:
                G.add_edge(s, t, weight=-self.data['scores'][s])

        M = nx.min_weight_matching(G)
        wgts = [G.edges()[e]['weight'] for e in M]

        return -sum(sorted(wgts)[:k])

def check_win_conditions():
    game_specs = yaml.load(open("input/game_specs.yml", "r"), Loader=yaml.Loader)

    for rounds in [5, 20]:
        for spec_name in game_specs:
            filename = f"output/facts/{spec_name}.json"
            data = json.load(open(filename, "r"))
            sim = Simulator(data)

            target = game_specs[spec_name]["targets"][rounds]
            pct = sim.pct_above(target, k=rounds)
            avg = int(sim.avg_score(k=rounds))
            print(f"{pct:0.3f} {target:7d} {avg:7d} | {spec_name} {rounds}")


def summary():
    game_specs = yaml.load(open("input/game_specs.yml", "r"), Loader=yaml.Loader)

    for rounds in [5, 20]:
        for spec_name in game_specs:
            filename = f"output/facts/{spec_name}.json"
            name = f'{spec_name}-{rounds}'
            data = json.load(open(filename, "r"))
            sim = Simulator(data)

            best = sim.best_possible(k=rounds)
            vals = [sim.sim_one(k=rounds) for _ in range(10000)]

            print(f'{name:16s} {min(vals):7d} {max(vals):7d} {best:7d}')

    #import matplotlib.pyplot as plt
    #fig, axs = plt.subplots()
    #axs.hist(vals, bins=40)
    #plt.show()


if __name__ == "__main__":
    check_win_conditions()
    print('')
    summary()
