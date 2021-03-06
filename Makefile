clean:
	@ echo 'cleaning...'
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

init-db:
	@ echo 'initializing database...'
	flask db stamp base
	flask db upgrade head

update-db:
	@ echo 'updating database...'
	flask db upgrade head

migrate:
	@ echo 'creating migrations...'
	flask db stamp head
	flask db migrate --message="$(message)"

update:
	@ echo 'updating requirements...'
	pip freeze | grep -v "pkg-resources" > requirements.txt

install:
	@ echo 'installing requirements...'
	pip install --upgrade pip
	pip install --upgrade pip setuptools
	pip install -r requirements.txt

test:
	pytest --cov-report term-missing --cov=api

run:
	@ echo 'starting server...'
	python manage.py runserver

init-app: init-db install run

lint:
	@ echo 'linting...'
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --select=E9,F63,F7,F82 --show-source --statistics --exclude=*.tox,.git,__pycache__,venv,env,__init__.py,*.pyc,*.egg-info,.eggs,alembic,migrations,.circleci