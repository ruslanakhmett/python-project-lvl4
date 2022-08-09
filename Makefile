cov:
	pytest --cov=task_manager
test:
	pytest
run:
	python3 manage.py runserver
req:
	poetry export -f requirements.txt --output requirements.txt