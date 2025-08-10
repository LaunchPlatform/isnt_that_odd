.PHONY: help install install-dev test test-cov lint format type-check clean build publish

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	uv sync

install-dev:  ## Install development dependencies
	uv sync --group dev

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=src/isnt_that_odd --cov-report=html --cov-report=term-missing

lint:  ## Run linting
	ruff check src/ tests/
	mypy src/

format:  ## Format code
	black src/ tests/
	isort src/ tests/

type-check:  ## Run type checking
	mypy src/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	uv build

publish:  ## Publish to PyPI (requires authentication)
	uv publish

prompt-test:  ## Test prompts with promptfoo
	promptfoo eval -c promptfoo.yaml

dev-setup: install-dev format lint  ## Setup development environment
	@echo "Development environment setup complete!"

all: format lint test  ## Run all checks (format, lint, test)
