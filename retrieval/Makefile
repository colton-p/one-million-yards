
facts: output/facts/*.json
franchises: output/franchises.yml
game_specs: output/game_specs.json

output/franchises.yml: make_franchises.py pages/franchises_page.py
	python make_franchises.py

output/game_specs.json: make_games.py input/game_specs.yml
	python make_games.py

output/facts/*.json: make_facts.py pages/*.py
	-mkdir output/facts
	python make_facts.py
