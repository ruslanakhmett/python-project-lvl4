run:
	python3 manage.py runserver
req:
	poetry export -f requirements.txt --output requirements.txt

install:
	poetry install

lint:
	poetry run flake8

test-cov:
	poetry run pytest --cov=task_manager/ --cov-report xml

check: selfcheck test


.PHONY: install test lint selfcheck check test-coverage