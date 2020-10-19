#!bin/sh -c

docker-compose up --build -d
docker-compose run --rm api aerich init -t config.TORTOISE_ORM --location db/migrations
docker-compose run --rm api aerich init-db
docker-compose down