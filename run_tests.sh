# export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose build
docker-compose run backend poetry run python -m pytest
