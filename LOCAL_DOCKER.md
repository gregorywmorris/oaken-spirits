# Local Docker

## Set up services

1. Run the Docker Desktop app.
1. Navigate to `oaken-spirits/src/production/docker` in the local repository.
1. Create `.env` using `docker.env.template`. Update variables accordingly.
    - `cp docker.env.template` 
1. Run `chmod +x create-topics.sh`
1. build images:

    ```bash
    docker build -t oaken-mysql-kafka -f mysql-api.yml .
    docker build -t oaken-shipping -f shipping.yml .
    docker build -t oaken-accounting -f accounting.yml .
    ```

1. docker compose: `docker-compose up -d`
1. Once services are up read [CLOUD_BEAVER.md](CLOUD_BEAVER.md)
    - Or you may use a database manager running on your pc of your own choice. MySQL is available at `localhost:3306`.

### IGNORE: For testing and trouble shooting a single service

1. `docker-compose stop <service_name>`
1. `docker-compose up --force-recreate <service_name>`

## Run business processes

1. Go to `src/production/docker/app/steaming-invoice`
1. Open **streaming-invoice-docker.ipynb** and **Run All**.
    - Service is generating about one record a second
1. Go to Cloud Beaver and run SQL to confirm processing

    ```sql
    --examples
    select * from sales;
    select * from salesLedger;
    select count(1) from sales;
    ```

1. Once satisfied, move to the next step, analytics.

> [!NOTE]
> If you leave notebook running it is continuing to generate sales data.
>
> If you stop the notebook, it may be neccesary to reset and Run All again to restart.