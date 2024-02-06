import json
import yaml


def main():
    with open("input/game_specs.yml", "r") as fp:
        win_conds = yaml.load(fp, Loader=yaml.Loader)

    out = {}
    for game, spec in win_conds.items():
        title = spec["title"]
        for rounds, target in spec["targets"].items():
            key = f"{game}-{rounds}"
            out[key] = {
                "title": title,
                "rounds": rounds,
                "target": target,
                "data_file": f"{game}.json",
            }

    with open("output/game_specs.json", "w") as fp:
        json.dump(out, fp, indent=2)


if __name__ == "__main__":
    main()
