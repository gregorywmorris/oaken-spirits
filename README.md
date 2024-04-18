![Oaken Spirirts Logo](images/oaken-spirits-logo.png)

![Python](https://img.shields.io/badge/Python-gluegreen)![Kafka](https://img.shields.io/badge/kafka-black)![MySQL](https://img.shields.io/badge/MySQL-lightblue)![Ubuntu](https://img.shields.io/badge/Ubuntu-lightgreen)![Docker](https://img.shields.io/badge/Docker-darkblue)![Dagster](https://img.shields.io/badge/Dagster-violet)![Airbyte](https://img.shields.io/badge/Airbyte-purple)![DBT](https://img.shields.io/badge/DBT-orange)![GCP](https://img.shields.io/badge/GCP-blue)![BigQuery](https://img.shields.io/badge/BigQuery-skyblue)![Looker](https://img.shields.io/badge/Looker_Studio-darkred)

## Video Overview

[Access 17 minute video here](https://youtu.be/nwtH_r85Qpw)
{% include youtube.html id="nwtH_r85Qpw" %}

## Project Prompt

### Data Engineering Zoomcamp

Formatted as: **Requirement**: My solution

- **Problem description:** [Overview section](#overview)
- **Cloud:** Google Cloud Platform, site link [GCP](https://cloud.google.com/)
- **Data ingestion:**
  - Stream with Apache Kafka, site link [here](https://kafka.apache.org/)
  - Batch with Airbyte and Dagster, GitHub links for [Airbyte](https://github.com/airbytehq) and [Dagster](https://github.com/dagster-io/dagster)
- **Data warehouse:** GCP BigQuery
- **Transformations:** [Data Build Tool (DBT)](https://www.getdbt.com/)
- **Dashboard:** Looker Studio
- **Reproducibility:** Instructions [start at this section](#instructions-order)
- **Tests:**
  - Added to `start-dagster.sh`
  - Included in the `start-airbyte.sh` from the source template

#### Assumptions and Limitations

##### Assumptions

- Instructions completed in VS Code, ability to convert to your IDE if different
- Access to a bash command line
- Basic familiarity with GitHub
- Ability to access cloud service providers
- A computer capable of running applications in this project

##### Limitations

1. For grader reproducibility, some things were hardcoded that normally would not be. Host names, secrets, etc. best practices would be to define these either in environment variables or in an encrypted manner.
1. Operational applications are scripts to simulate real app output.
1. A single service account was created, in production there would be a service account for each service.
1. Batch processing is run manually for demonstration, this would be put on a schedule in production.
1. Markdown is written for GitHub Markdown, as such it may render better if read on GitHub.

## Overview

> Oaken Spirits is an alcohol distributor that has gained popularity from it's private selection of whiskey. Its popularity has spurred growth and the company has recently signed a deal to expand at a national level with several large vendors. Currently, the applications supporting the business are for Iowa sales only and the CEO is concerned that they will not support future growth and would like a system that can handle national-level sales.

### Scenario

> Oaken Spirit management does not want to spend money on more modern, but expensive, applications. You have been directed to work with the vendors to find a solution. The sales application stores data locally and does not integrate with external databases. Working with the vendors we can get a JSON message from each application. The shipping and accounting applications can integrate with an external database.

### Concern

>1. Not scalable, some manual data entry and transfers. This could cause delays or errors, more so as we scale nationally. The current processes may not be practical.
>1. Does not integrate or deliver real-time updates between the applications. This can lead to delays in shipping and accounting.
>1. Has data in multiple locations; sometimes duplicated. Lack of integration and centralization has led to departments such as sales and shipping recording duplicate data.
>1. Lacks an analytics solution. There are no options for leadership to make data-informed decisions.
>1. Desire integration options that allows adding or replacing applications. As the business grows and technology improves, new applications may be added and current applications replaced.

### Objectives

>1. Create a single database as the source of truth.
>1. Create a data pipeline that integrates the systems and provides real-time updates.
>1. Ensure the system is scalable.
>1. Provide an analytics solution.

## Technical Design

See [**OAKEN_TECHNICAL_DESIGN.md**](OAKEN_TECHNICAL_DESIGN.md)

## Set Up Services

![App Services Diagram](images/oaken-service-diagram.png)

### Instructions Order

1. Clone the repository locally
1. Requirements
1. Choose Local
1. Cloud Analytics
1. Clean up

### Requirements

- [**REQUIREMENTS.md**](REQUIREMENTS.md)

### Business Services

- On-site data center: [**LOCAL_DOCKER.md**](LOCAL_DOCKER.md), streaming data pipeline for business services.

or

- Full Cloud - not available yet

![Under Construction](images/under-construction.jpg)

### Cloud Analytics

1. Run analytics services: see [**ANALYTICS_PIPELINE.md**](ANALYTICS_PIPELINE.md), batch data pipeline for analytics.
1. Dashboard: [**DASHBOARD.md**](DASHBOARD.md)

### Close Project

- [**CLEAN_UP.md**](CLEAN_UP.md)