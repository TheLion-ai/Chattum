# export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose build
docker-compose run --remove-orphans  -p 27017:27017 backend poetry run python -m pytest
