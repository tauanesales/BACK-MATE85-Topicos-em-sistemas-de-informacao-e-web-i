ifneq ("$(wildcard .env)","")
	include .env
	export
endif

.PHONY: run
run: ## Run the project.
	poetry run python -m src.api

.PHONY: install
install: ## Install Python requirements.
	python -m pip install --upgrade pip setuptools wheel poetry
	poetry lock
	poetry install --no-root
	poetry run pre-commit install

.PHONY: test
test: ## Run tests.
	poetry run pytest ./src/tests -vv -s

.PHONY: export-requirements
export-requirements: ## Export requirements to requirements.txt, so it can be used by Vercel.
	poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev

.PHONY: up-db
up-db: ## Start local MySQL database using docker.
	docker compose -f docker-compose.yml up -d db

.PHONY: down
down: ## Stop all docker services from this project.
	docker compose -f docker-compose.yml down

.PHONY: revision
revision: ## Create a new revision of the database using alembic. Use MESSAGE="your message" to add a message.
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"

.PHONY: migrate
migrate: ## Apply the migrations to the database.
	poetry run alembic upgrade head

.PHONY: downgrade
downgrade: ## Undo the last migration.
	poetry run alembic downgrade -1

.PHONY: pre-commit
pre-commit: ## Run pre-commit checks.
	poetry run pre-commit run --config ./.pre-commit-config.yaml

.PHONY: patch
patch: ## Bump project version to next patch (bugfix release/chores).
	poetry version patch

.PHONY: minor
minor: ## Bump project version to next minor (feature release).
	poetry version minor

.PHONY: clean
clean: ## Clean project's temporary files.
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.log' -exec rm -f {} +

.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'