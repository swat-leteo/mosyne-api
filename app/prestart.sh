#! /usr/bin/env bash

# Await until DB is up
sleep 3s

# Init db if not exists migrations

aerich init -t db.TORTOISE_ORM_CONFIG
aerich init-db

# Allow register the ORM (needed cause an aerich bug)

rm -rf migrations
rm -rf aerich.ini
aerich init -t db.TORTOISE_ORM_CONFIG
aerich init-db

# Run migrations

aerich migrate
aerich heads
aerich upgrade
