run:
	docker-compose up -d

down:
	docker-compose down

load-fixtures:
	docker-compose run app python manage.py loaddata fixtures/fixtures.json

test:
	docker-compose run app python manage.py test

check:
	ruff check

format:
	ruff format
