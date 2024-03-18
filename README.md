![Oaken Spirirts Logo](images/oaken-spirits-logo.png)
# Oaken Spirits
Liquor sales data engineering project.

[Dataset](https://www.kaggle.com/datasets/residentmario/iowa-liquor-sales)

1. [Ubuntu Kaggle API instructions](https://www.endtoend.ai/tutorial/how-to-download-kaggle-datasets-on-ubuntu/)
1. `kaggle datasets download -d residentmario/iowa-liquor-sales`
1. Alternatively, download data via web browser
1. `unzip iowa-liquor-sales.zip` - 3.47 GB file

![App Services Diagram](images/oaken-service-diagram.png)

## Set Up Services

Instructions order:

1. AWS S3
1. Environment Variables
1. Choose either AWS or Docker Business Services
1. Analytics

## AWS S3

1. See [**AWS_S3.md**](AWS_S3.md)

### Environment Variables

1. See [**ENV_VARIABLES.md**](ENV_VARIABLES.md)

### Business Services

- On AWS

1. Create EC2: see [**EC2.md**](EC2.md)
1. Kafka: see [**1A_Kafka_AWS.md**](1A_Kafka_AWS.md)
1. Run business services: see [**2A_AWS.md**](2A_AWS.md)

or

- On local Docker

1. Kafka: see [**1B_KAFKA_ON_DOCKER.md**](1B_KAFKA_ON_DOCKER.md)
1. Run business: see [**2B_LOCAL_DOCKER.md**](2B_LOCAL_DOCKER.md)

### Analytics

1. Run analytics services: see [**3_ANALYTICS.md**](3_ANALYTICS.md)
