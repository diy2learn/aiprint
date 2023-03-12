.DEFAULT_GOAL := help
.PHONY: coverage deps help lint publish push test

SRC_DIR = src
TEST_DIR = tests

install: install_dev ## Default install is dev
.PHONY: install

ci: typecheck lint test ## Run all checks (test, lint, typecheck) for continuous integration
.PHONY: ci

install_prod: update install_pip ## Install the dependencies listed in the pyproject.toml file (production)
	poetry install --no-dev
.PHONY: install_prod

install_dev: update install_pip ## Install the dependencies listed in the pyproject.toml file (development)
	poetry install
.PHONY: install_dev

install_pip: ## Install pip or upgrade it, --user is optional, in case you don't have write access on python install
	python -m pip install --upgrade pip --user
.PHONY: install_pip

update: ## Update your project’s dependencies
	poetry update
.PHONY: update

lint:  ## Linting
	poetry run black $(SRC_DIR) $(TEST_DIR)
	poetry run isort $(SRC_DIR) $(TEST_DIR)
	poetry run flake8 --max-line-length 120 $(SRC_DIR) $(TEST_DIR)
	poetry run pylint $(SRC_DIR) $(TEST_DIR)

lint_in_ci:  ## Linting
	black --check --verbose $(SRC_DIR) $(TEST_DIR)
	isort --check --verbose $(SRC_DIR) $(TEST_DIR)
	pylint $(SRC_DIR) $(TEST_DIR)

.PHONY: lint

typecheck: ## Type checking
	poetry run mypy $(SRC_DIR) $(TEST_DIR)
.PHONY: typecheck

test:  ## Run tests wiith coverage
	poetry run coverage run --source=$(SRC_DIR) -m pytest -v -m "not integration" tests && poetry run coverage report -m
.PHONY: test

clean: clean-poetry clean-py ## Clean the poetry install and associated environments
.PHONY: clean

clean-poetry: ## Clean poetry
	poetry env remove all
.PHONY: clean-poetry

clean-py:
	rm -rf  ./*.egg-info
	rm -rf  ./**/__pycache__/

wheel: ## Build Python binary distribution wheel package
	poetry build --format wheel

source: ## Build Python source distribution package
	poetry build --format sdist

.PHONY: help
help: ## Show help message
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%s\n\n" "Usage: make [task]"; \
	printf "%-20s %s\n" "task" "help" ; \
	printf "%-20s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-20s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done