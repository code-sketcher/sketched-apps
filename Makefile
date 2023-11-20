SHELL := /bin/bash

install_dependecies:
	./resolve_dependencies.sh
	python3 -m venv ~/sketched-apps-venv
	source ~/sketched-apps-venv/bin/activate
	~/sketched-apps-venv/bin/pip install -r requirements.txt

run: install_dependecies
	@printf "\e[1;34mStart installing...\e[0m\n"
	~/sketched-apps-venv/bin/python3 main.py
