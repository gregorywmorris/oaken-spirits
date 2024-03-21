# Local Docker

1. Navigate to `/src/docker/`
1. Create `docker.env` using `docker.env.template`. Update variables accordingly.
1. build images
    - `docker build -t oaken-mysql-kafka -f mysql-kafka-processor.yml .`
    - `docker build -t oaken-shipping -f shipping.yml .`
    - `docker build -t oaken-accounting -f accounting.yml .`
1. docker compose: `docker-compose up -d`
