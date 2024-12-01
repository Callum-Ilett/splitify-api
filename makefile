migrate:
	docker compose exec splitifyapi python manage.py migrate

migrations:
	docker compose exec splitifyapi python manage.py makemigrations
