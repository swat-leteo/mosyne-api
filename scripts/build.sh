#!bin/sh -c

docker-compose up --build -d
docker-compose run --rm api aerich init -t db.settings.TORTOISE_ORM_CONFIG --location db/migrations
docker-compose run --rm api aerich init-db
docker-compose down