.PHONY: all setup install_requirements requirements docs tests download_data data

# Set name of virtual environment here
VENV = .venv
BIN = ${VENV}/bin/

# Code to run when calling `make` by itself. This must be the top instruction in the file.
all: setup docs download_data data

# Setup
setup: ${VENV} install_requirements docs

${VENV}:
	python3 -m venv $@

install_requirements: requirements.txt
	$(BIN)pip install --upgrade pip
	$(BIN)pip install -r requirements.txt
	$(BIN)pre-commit install

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

docker:
	-docker rm -f $(shell docker ps -aq)
	docker build --tag nameofdockerimage .
	docker run --name temporarycontainername nameofdockerimage

# Download Data --------------------------------------------------------------------------------------------------------
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


# DATA WRANGLING -------------------------------------------------------------------------------------------------------
data: data/processed/memory_optimized_data.pkl \
data/processed/test.pkl data/processed/train.pkl \
data/processed/features.pkl data/processed/test_features.pkl

#Preprocessing pipelines
data/processed/memory_optimized_data.pkl: src/data/data_optimizer_script.py data/raw/train.csv
	(cd src/data/ ; ../../$(BIN)python data_optimizer_script.py)

data/processed/features.pkl: src/features/make_features.py data/processed/memory_optimized_data.pkl
	$(BIN)python -m src.features.make_features 'data/processed/memory_optimized_data.pkl' 'data/processed/features.pkl' True

data/processed/test_features.pkl: src/features/make_features.py data/processed/test.pkl
	$(BIN)python -m src.features.make_features 'data/processed/test.pkl' 'data/processed/test_features.pkl'

data/processed/test.pkl: src/data/clean.py data/raw/test.csv
	$(BIN)python -m src.data.clean 'data/raw/test.csv' 'data/processed/test.pkl'

data/processed/train.pkl: src/data/clean.py data/raw/train.csv
	$(BIN)python -m src.data.clean 'data/raw/train.csv' 'data/processed/train.pkl'