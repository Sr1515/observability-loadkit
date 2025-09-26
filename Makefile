run:
	docker compose up -d

build:
	docker compose build 

off:
	docker compose down -v 

reset:
	make off & make build & make run

mk:
	python3 manage.py makemigrations
mg:
	python3 manage.py migrate
