install:
	@ echo 'installing requirements...'
	pip install -r requirements.txt

run:
	@ echo 'starting server...'
	python manage.py runserver

build: install run

lint:
	@ echo 'linting...'
	flake8 --exclude=* venv/,env/, .env, .md, .txt