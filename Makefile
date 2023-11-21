SHELL := /bin/bash

install_dependecies:
	./resolve_dependencies.sh
	python3 -m venv .venv
	source .venv/bin/activate
	.venv/bin/pip install -r requirements.txt

run: install_dependecies
	@printf "\e[1;34mStart installing...\e[0m\n"
	.venv/bin/python3 main.py
