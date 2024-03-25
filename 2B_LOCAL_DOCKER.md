# Local Docker

1. Navigate to `/src`
1. Create `docker.env` using `docker.env.template`. Update variables accordingly.
1. Run `chmod +x create-topics.sh`
1. build images
    - `docker build -t oaken-mysql-kafka -f mysql-kafka-processor.yml .`
    - `docker build -t oaken-shipping -f shipping.yml .`
    - `docker build -t oaken-accounting -f accounting.yml .`
1. docker compose: `docker-compose up -d`
1. Once services are up see [CLOUD_BEAVER.md](CLOUD_BEAVER.md)

## Testing and trouble shooting a single service

1. `docker-compose stop <service_name>`
1. `docker-compose up --force-recreate <service_name>`
