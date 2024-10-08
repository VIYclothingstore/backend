ifneq ("$(wildcard .env)","")
    include .env
    export $(shell sed 's/=.*//' .env)
else
endif

WORKDIR := $(shell pwd)
.ONESHELL:
.EXPORT_ALL_VARIABLES:
DOCKER_BUILDKIT=1


help: ## Display help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

build_and_run: ## Run and build application
	 docker compose up -d --build 

run_app:  ## Run application
	docker compose up -d

drop_all_containers: ## Drop all containers
	docker compose down -v --remove-orphans

run_migrate: ## Run migrate
	docker compose exec api ./src/manage.py migrate

migrate: ## Make migrate
	docker compose exec api ./src/manage.py makemigrations

super_user: ## Make super user
	docker compose exec api ./src/manage.py createsuperuser

open_shell: ## Open shell to the app container
	docker compose exec api bash

open_log: ## Open api log
	docker compose logs -f api

