.PHONY: help build up down logs migrate shell createsuperuser test

help:
	@echo "Available commands:"
	@echo "  make build          - Build Docker containers"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make logs           - View logs"
	@echo "  make migrate        - Run database migrations"
	@echo "  make shell          - Open Django shell"
	@echo "  make createsuperuser - Create Django superuser"
	@echo "  make test           - Run tests"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

migrate:
	docker-compose exec backend python manage.py makemigrations
	docker-compose exec backend python manage.py migrate

shell:
	docker-compose exec backend python manage.py shell

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

test:
	docker-compose exec backend python manage.py test
