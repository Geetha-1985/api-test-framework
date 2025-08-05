.PHONY: help install test test-smoke test-regression test-performance clean reports

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $1, $2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run all tests
	pytest tests/ --html=reports/report.html --alluredir=reports/allure-results

test-smoke: ## Run smoke tests only
	pytest tests/ -m smoke --html=reports/smoke-report.html

test-regression: ## Run regression tests
	pytest tests/ -m regression --html=reports/regression-report.html

test-performance: ## Run performance tests
	pytest tests/ -m performance --html=reports/performance-report.html

test-parallel: ## Run tests in parallel
	pytest tests/ -n auto --html=reports/parallel-report.html

clean: ## Clean up generated files
	rm -rf reports/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

reports: ## Generate Allure reports
	allure generate reports/allure-results -o reports/allure-report --clean
	allure open reports/allure-report

setup-env: ## Setup environment file
	cp .env.example .env
	@echo "Please update .env file with your API tokens"

docker-test: ## Run tests in Docker
	docker run --rm -v $(PWD):/app -w /app python:3.9 sh -c "pip install -r requirements.txt && pytest tests/"