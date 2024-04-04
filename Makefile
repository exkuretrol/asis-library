.PHONY: run

init:
	@poetry install
	@django-admin startproject django_project .
	@mkdir -p static/src

tailwind:
	@npx tailwind -i ./static/src/input.css -o ./static/css/output.css -c tailwind.config.js --watch

run:
	@python manage.py runserver

test:
	@python manage.py test

makemigrations:
	@python manage.py makemigrations account
	@python manage.py makemigrations book

migrate:
	@python manage.py migrate

collectstatic:
	@python manage.py collectstatic

shell:
	@python manage.py shell

clean:
	@find . -type f -name ".DS_Store" -execdir rm -rf {} \;
	@find . -type d -name "migrations" -execdir rm -rf {} \;
	@find . -type d -name "__pycache__" -execdir rm -rf {} \;
	@find . -type f -name "db.sqlite3" -execdir rm -rf {} \;
	@find ./media -type f -execdir rm -rf {} \;

