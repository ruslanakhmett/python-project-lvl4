test-cov:
	poetry run pytest --cov=task_manager/ --cov-report xml
test:
	pytest --capture=no
run:
	python3 manage.py runserver
req:
	poetry export -f requirements.txt --output requirements.txt

install:
	poetry install

install:
	poetry install

lint:
	poetry run flake8

cov:
	pytest --cov=task_manager

check: selfcheck test


.PHONY: install test lint selfcheck check build page_loader deploy test-coverage