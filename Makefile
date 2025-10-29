.PHONY: help install install-dev test test-cov lint format type-check security clean build publish docs

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	poetry install --no-dev

install-dev: ## Install the package with development dependencies
	poetry install

test: ## Run tests
	poetry run pytest tests/ -v

test-cov: ## Run tests with coverage
	poetry run pytest tests/ -v --cov=aioyookassa --cov-report=term-missing --cov-report=html:htmlcov

test-fast: ## Run tests without coverage (faster)
	poetry run pytest tests/ -v --no-cov

lint: ## Run linting
	poetry run black --check aioyookassa tests

format: ## Format code
	poetry run black aioyookassa tests
	poetry run isort aioyookassa tests

type-check: ## Run type checking
	poetry run mypy aioyookassa


clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build the package
	poetry build

publish: ## Publish to PyPI
	poetry publish

publish-test: ## Publish to Test PyPI
	poetry publish --repository testpypi

docs: ## Build documentation
	cd docs && make html

docs-serve: ## Serve documentation locally
	cd docs && make html && python -m http.server 8000 -d _build/html

pre-commit: ## Install pre-commit hooks
	poetry run pre-commit install

pre-commit-run: ## Run pre-commit on all files
	poetry run pre-commit run --all-files

all-checks: lint type-check test-cov ## Run all checks

dev: install-dev all-checks build ## Run development pipeline locally
