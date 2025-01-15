.PHONY: tests

all:
	python main.py

tests:
	pytest --cov=gui --cov=data --cov-report=html --cov-report=term tests
