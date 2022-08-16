cov:
	pytest --cov=task_manager
test-cov:
	poetry run pytest --cov=task_manager/ --cov-report xml
test:
	pytest
run:
	python3 manage.py runserver
req:
	poetry export -f requirements.txt --output requirements.txt