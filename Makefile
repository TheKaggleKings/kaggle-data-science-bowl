.PHONY: all setup install_requirements requirements docs tests download_data

# Set name of virtual environment here
VENV = .venv
BIN = ${VENV}/bin/

# Code to run when calling `make` by itself. This must be the top instruction in the file.
all: setup docs

# Setup
setup: ${VENV} install_requirements download_data

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

# Data -----------------------------------------------------------------------------------------------------------------
download_data: data/raw/sample_submission.csv data/raw/specs.csv data/raw/test.csv data/raw/train.csv \
data/raw/train_labels.csv

data/raw/sample_submission.csv:
	$(BIN)kaggle competitions download data-science-bowl-2019 -f sample_submission.csv -p data/raw

data/raw/specs.csv:
	$(BIN)kaggle competitions download data-science-bowl-2019 -f specs.csv -p data/raw

data/raw/test.csv:
	$(BIN)kaggle competitions download data-science-bowl-2019 -f test.csv -p data/raw
	unzip data/raw/test.csv.zip -d data/raw
	rm data/raw/test.csv.zip

data/raw/train.csv:
	$(BIN)kaggle competitions download data-science-bowl-2019 -f train.csv -p data/raw
	unzip data/raw/train.csv.zip -d data/raw
	rm data/raw/train.csv.zip

data/raw/train_labels.csv:
	$(BIN)kaggle competitions download data-science-bowl-2019 -f train_labels.csv -p data/raw
	unzip data/raw/train_labels.csv.zip -d data/raw
	rm data/raw/train_labels.csv.zip
