![Oaken Spirirts Logo](images/oaken-spirits-logo.png)

![Python](https://img.shields.io/badge/Python-darkblue)![Kafka](https://img.shields.io/badge/kafka-black)![MySQL](https://img.shields.io/badge/MySQL-lightblue)![Ubuntu](https://img.shields.io/badge/Ubuntu-green)![Airflow](https://img.shields.io/badge/Airflow-red)![Static Badge](https://img.shields.io/badge/AWS-yellow)![Static Badge](https://img.shields.io/badge/docker-purple)

## Project Prompt

### Data Engineering Zoomcamp

Format: **Requirement**: My solution

- **Problem description:** [Overview section](#overview)
- **Cloud:** Google Cloud Platform, site link [GCP](https://cloud.google.com/)
- **Data ingestion:**
  - Stream with Apache Kafka, site link [here](https://kafka.apache.org/)
  - Batch with Airbyte and Dagster, GitHub links for [Airbyte](https://github.com/airbytehq) and [Dagster](https://github.com/dagster-io/dagster)
- **Data warehouse:** GCP BigQuery
- **Transformations:** [Data Build Tool (DBT)](https://www.getdbt.com/)
- **Dashboard:** TBD
- **Reproducibility:** Instructions [start at this section](#instructions-order)

#### Assumptions and Limitations

##### **Assumptions**

- Instructions completed in VS Code, ability to convert to your IDE if different
- Access to a bash command line
- Basic familiarity with github
- Ability to access cloud service providers

##### **Limitations**

> For grader reproducibility, some things were hard coded that normally would not be. Host names, secrets, etc. best practices would be to define these either in environment variables or in an encrypted manner.

## Overview

> Oaken Spirits is an alcohol distributor that gets its name from its popular private selection of whiskey. Its popularity has spurred growth and the company has recently signed a deal to expand at a national level with several large vendors. Currently, the applications supporting the business are for Iowa sales only and the CEO is concerned that they will not support future growth and would like a system that can handle national-level sales.

### Scenario

> Oaken Spirit management does not want to spend money on more modern, but expensive, applications. You have been directed to work with the vendors to find a solution. The sales application stores data locally and does not integrate with external databases. Working with the vendors we can get a JSON message from each application. The shipping and accounting applications can integrate with an external database.

### Concern

1. Not scalable, some manual data entry and transfers. This could cause delays or errors, more so as we scale nationally. The current processes may not be practical.
1. Does not integrate or deliver real-time updates between the applications. This can lead to delays in shipping and accounting.
1. Has data in multiple locations; sometimes duplicated. Lack of integration and centralization has led to departments such as sales and shipping recording duplicate data.
1. Lacks an analytics solution. There are no options for leadership to make data-informed decisions.
1. Lacks integration options making replacement or adding applications difficult. As the business grows and technology improves, new applications may be added and current applications replaced.

### Objectives

1. Create a single database as the source of truth
1. Create a data pipeline that integrates the systems and provides real-time updates
1. Ensure the system is scalable
1. Provide an analytics solution

### Technical Design

See [OAKEN_TECHNICAL_DESIGN](OAKEN_TECHNICAL_DESIGN.md)

## Data

[Dataset](https://www.kaggle.com/datasets/residentmario/iowa-liquor-sales)

1. [Ubuntu Kaggle API instructions](https://www.endtoend.ai/tutorial/how-to-download-kaggle-datasets-on-ubuntu/)
1. `kaggle datasets download -d residentmario/iowa-liquor-sales`
1. `unzip iowa-liquor-sales.zip 'unzip iowa-liquor-sales_dirty.csv'` - 3.47 GB file

## Set Up Services

![App Services Diagram](images/oaken-service-diagram.png)

### Instructions order

1. Clone the repository locally
1. Choose Local
1. Cloud Analytics

### Business Services

- Local

1. [**LOCAL_DOCKER.md**](LOCAL_DOCKER.md), streaming data pipeline for business services.

or

- Full Cloud - not available yet

![Under Construction](images/under-construction.jpg)

<!-- 1. Kafka: see [**1A_Kafka_AWS.md**](1A_Kafka_AWS.md)
1. Run business services: see [**2A_AWS.md**](2A_AWS.md)-->

### Cloud Analytics

1. Run analytics services: see [**ANALYTICS_PIPELINE.md**](ANALYTICS_PIPELINE.md), batch data pipeline for analytics.
1. Dashboard: [DASHBOARD.md](DASHBOARD.md)

### Close Project

1. [Clean up](CLEAN_UP.md)