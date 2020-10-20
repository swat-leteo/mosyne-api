#! /usr/bin/env bash


# Init db if not exists migrations

aerich init -t db.settings.TORTOISE_ORM_CONFIG --location db/migrations
aerich init-db

# Run migrations

aerich migrate
aerich heads
aerich upgrade