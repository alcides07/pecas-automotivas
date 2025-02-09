DOCKER_COMPOSE := docker-compose -f docker-compose.yml
DJANGO := docker exec -it pecas-api-dev python manage.py

# -------------------------------------------
# manage.py

make:
	@${DJANGO} makemigrations

migrate:
	@${DJANGO} migrate

superuser:
	@${DJANGO} createsuperuser

# -------------------------------------------
# docker-compose.yml

build:
	@${DOCKER_COMPOSE} build

up:
	@${DOCKER_COMPOSE} up -d

down:
	@${DOCKER_COMPOSE} down --remove-orphans

full:
	@${DOCKER_COMPOSE} build
	@${DOCKER_COMPOSE} up -d
	@${DJANGO} migrate
