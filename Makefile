all:
	python main.py

tests:
	rm -rf htmlcov
	pytest --cov=gui --cov=data tests