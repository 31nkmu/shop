run:
	./manage.py runserver
migrate:
	./manage.py makemigrations
	./manage.py migrate
user:
	./manage createsuperuser
celery:
	celery -A config worker -l debug
beat:
	celery -A config beat
