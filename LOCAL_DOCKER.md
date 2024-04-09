# Local Docker

1. [Install Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/) <- External link
1. [Install Docker Desktop on Mac](https://docs.docker.com/desktop/install/mac-install/) <- External link
1. Run the Docker Desktop app.
1. Navigate to `oaken-spirits/src/production/docker` in the local repository.
1. Create `.env` using `docker.env.template`. Update variables accordingly.
    - `cp docker.env.template` 
1. Run `chmod +x create-topics.sh .env`
1. build images

    ```bash
    docker build -t oaken-mysql-kafka -f mysql-api.yml .
    docker build -t oaken-shipping -f shipping.yml .
    docker build -t oaken-accounting -f accounting.yml .
    ```

1. docker compose: `docker-compose up -d`
1. Once services are up read [CLOUD_BEAVER.md](CLOUD_BEAVER.md)
    - Or you may use a database manager running on your pc of your own choice. MySQL is available at `localhost:3306`.

## Testing and trouble shooting a single service

1. `docker-compose stop <service_name>`
1. `docker-compose up --force-recreate <service_name>`