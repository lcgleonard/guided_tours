PROJECT_DIR=$(dir $(realpath $(firstword $(MAKEFILE_LIST))))
export USERNAME=$(shell hostname | cut -d '-' -f2)

help:
	@echo "Usage: make command"
	@echo "start           - Run settler server using docker container"
	@echo "up              - Build and start the docker container"
	@echo "stop            - Stop container"
	@echo "down            - Stop and remove the container"
	@echo "logs            - Follow log output"
	@echo "restart         - Restart server"
	@echo "kill            - Kill server"
	@echo "install-docker  - Install docker and docker-compose"

start: up
	@docker-compose start

stop:
	@docker-compose stop

up:
	@docker-compose up -d

down:
	@docker-compose down

logs:
	@docker-compose logs --tail 60 -f

restart: stop start

kill:
	@docker-compose kill

status:
	@docker-compose ps

install-docker:
	./scripts/install_docker.sh

test:
	@py.test --cov=application tests/
