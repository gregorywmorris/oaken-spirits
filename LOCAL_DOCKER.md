# Local Docker

## Set up services

1. Run the Docker Desktop app.
1. Navigate to `oaken-spirits/src/production/docker` in the local repository.
1. Set up services:

    ```bash
    chmod +x create-topics.sh
    chmod +x run-docker-apps.sh
    ./run-docker-apps.sh
    ```

1. Once services are up, see [CLOUD_BEAVER.md](CLOUD_BEAVER.md).

## Run invoice processes

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
> If you stop the notebook, it may be necessary to reset and Run All again to restart.

### For testing and trouble shooting a single service

1. `docker-compose stop <service_name>`
1. `docker-compose up --force-recreate <service_name>`