.PHONY: all setup install_requirements requirements docs tests download_data

# Set name of virtual environment here
VENV = .venv
BIN = ${VENV}/bin/

# Code to run when calling `make` by itself. This must be the top instruction in the file.
all: setup docs

# Setup
setup: ${VENV} install_requirements

${VENV}:
	python3 -m venv $@

install_requirements: requirements.txt
	$(BIN)pip install -r requirements.txt

# List requirements
requirements:
	$(BIN)pip freeze | grep -v "pkg-resources" > requirements.txt

# Documentation
docs: docs/conf.py docs/index.rst
	-rm -r docs/_build
	$(BIN)sphinx-build -b html docs docs/_build

# Tests
tests:
	$(BIN)python -m pytest tests/

download_data: