migrate:
	docker compose exec -it splitifyapi bash -c "cd src && python manage.py migrate"

migrations:
	docker compose exec -it splitifyapi bash -c "cd src && python manage.py makemigrations"
