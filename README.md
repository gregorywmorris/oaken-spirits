<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: black; /* Specify your desired background color */
            color: offwhite;
        }
        .container { /* class="container" */
            margin: 0 auto;
            max-width: 800px;
            padding: 20px;
            background-color: black; /* Specify the background color of the content area */
        }
    </style>
</head>
<body>

![Oaken Spirirts Logo](images/oaken-spirits-logo.png)

![Python](https://img.shields.io/badge/Python-blue)![Kafka](https://img.shields.io/badge/kafka-black)![MySQL](https://img.shields.io/badge/MySQL-lightblue)![Ubuntu](https://img.shields.io/badge/Ubuntu-green)![FastAPI](https://img.shields.io/badge/FastAPI-lightgreen)![Airflow](https://img.shields.io/badge/Airflow-red)![Static Badge](https://img.shields.io/badge/AWS-yellow)


## $$ {\color{salmon}Project Prompt} $$

### <span style="color:#FECEA8">Overview</span>

Oaken Sprits is an alcohol distributor that gets its name from its popular private selection of whiskey. Its popularity has spurred growth and the company is looking to expand outside of Iowa, USA. Currently, the applications supporting the business are not integrated and the CEO is concerned that they will not support future growth.

### <span style="color:#FECEA8">Concerns</span>

1. Not scalable
1. Does not deliver real-time updates
1. Has multiple databases
1. Lacks a consolidated analytics solutions

### <span style="color:#FECEA8">Objectives</span>

1. Create a single database as the source of truth
1. Create a data pipeline that integrates the systems and provides real-time updates
1. Ensure the system is scalable
1. Provide an analytics solution for management

### <span style="color:#FECEA8">Technical Design</span>

See [OAKEN_TECHNICAL_DESIGN](OAKEN_TECHNICAL_DESIGN.md)

## <span style="color:#FF847C">Data</span>

[Dataset](https://www.kaggle.com/datasets/residentmario/iowa-liquor-sales)

1. [Ubuntu Kaggle API instructions](https://www.endtoend.ai/tutorial/how-to-download-kaggle-datasets-on-ubuntu/)
1. `kaggle datasets download -d residentmario/iowa-liquor-sales`
1. Alternatively, download data via the web browser
1. `unzip iowa-liquor-sales.zip` - 3.47 GB file

## <span style="color:#FF847C">Set Up Services</span>

![App Services Diagram](images/oaken-service-diagram.png)

### <span style="color:#FECEA8">Instructions order</span>

1. AWS S3
1. Environment Variables
1. Choose either AWS or local Docker for Business Services
1. Analytics

### <span style="color:#FECEA8">AWS S3</span>

1. See [**AWS_S3.md**](AWS_S3.md)

### <span style="color:#FECEA8">Environment Variables</span>

1. See [**ENV_VARIABLES.md**](ENV_VARIABLES.md)

### <span style="color:#FECEA8">Business Services</span>

- On AWS

1. Create EC2: see [**EC2.md**](EC2.md)
1. Kafka: see [**1A_Kafka_AWS.md**](1A_Kafka_AWS.md)
1. Run business services: see [**2A_AWS.md**](2A_AWS.md)

or

- On local Docker

1. Kafka: see [**1B_KAFKA_ON_DOCKER.md**](1B_KAFKA_ON_DOCKER.md)
1. Run business: see [**2B_LOCAL_DOCKER.md**](2B_LOCAL_DOCKER.md)

### <span style="color:#FECEA8">Analytics</span>

1. Run analytics services: see [**3_ANALYTICS.md**](3_ANALYTICS.md)

</body>
</html>