.PHONY: help install install-dev test lint format clean build publish docs run

help:
	@echo "LOAD-SPAN Makefile Commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build distribution packages"
	@echo "  make publish      - Publish to PyPI"
	@echo "  make docs         - Build documentation"
	@echo "  make run          - Run the assessment pipeline"
	@echo "  make dashboard    - Launch monitoring dashboard"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest tests/ -v --cov=load_span --cov-report=html --cov-report=term

lint:
	flake8 load_span/ tests/
	pylint load_span/ --fail-under=7.0
	mypy load_span/ --ignore-missing-imports

format:
	black load_span/ tests/ examples/
	isort load_span/ tests/ examples/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build
	@echo "Build complete. Check dist/ directory"

publish: build
	twine upload dist/*

docs:
	cd docs && make html
	@echo "Documentation built in docs/_build/html/"

run:
	python -m load_span.pipeline --config configs/default.yaml

dashboard:
	streamlit run load_span/monitoring/app.py

benchmark:
	python simulation/benchmarks.py

validate:
	python simulation/validate.py --all

docker-build:
	docker build -t load-span:latest .

docker-run:
	docker run -p 8000:8000 -p 8501:8501 load-span:latest
