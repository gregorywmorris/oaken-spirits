#!/bin/bash

docker build -t oaken-mysql-kafka -f mysql-api.yml .
docker build -t oaken-shipping -f shipping.yml .
docker build -t oaken-accounting -f accounting.yml .

cp docker.env.template .env

docker-compose up -d