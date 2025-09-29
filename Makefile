run:
	docker compose up -d

build:
	docker compose build 

off:
	docker compose down -v 

reset:
	make off & make build & make run

mk:
	docker compose exec backend python manage.py makemigrations

mg:
	docker compose exec backend python manage.py migrate

logs:
	docker compose logs -f 

