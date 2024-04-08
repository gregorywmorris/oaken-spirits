# Oaken Spirits Analytics Stack with Airbyte, DBT, Dagster and BigQuery

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting an environment for your project](#1-setting-an-environment-for-your-project)
- [Setting Up BigQuery to work with Airbyte and DBT](#2-setting-up-bigquery)
- [Setting Up Airbyte Connectors](#3-setting-up-airbyte-connectors)
- [Setting Up the DBT Project](#4-setting-up-the-dbt-project)
- [Orchestrating with Dagster](#5-orchestrating-with-dagster)
- [Next Steps](#next-steps)

## Prerequisites

Ensure you have the following set up and ready:

1. **Python 3.11 or later**

1. **Docker and Docker Compose (Docker Desktop)**: Install [Docker](https://docs.docker.com/get-docker/) following the official documentation for your specific OS.

1. **Airbyte OSS version**: Deploy the open-source version of Airbyte locally. Follow the installation instructions from the [Airbyte Documentation](https://docs.airbyte.com/quickstart/deploy-airbyte/).

1. **Google Cloud account with BigQuery**: You will also need to add the necessary permissions to allow Airbyte and DBT to access the data in BigQuery. A step-by-step guide is provided [below](#2-setting-up-bigquery).

## 1. Setting an environment for your project

Get the project up and running on your local machine by following these steps:

- **Navigate to the directory**:

    ```bash
   cd src/production/analytics
   ```

## 2. Setting Up BigQuery

### 1. **Create a Google Cloud Project**

- If you have a Google Cloud project, you can skip this step.
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Click on the "Select a project" dropdown at the top right and select "New Project".
- Give your project a name and follow the steps to create it.

### 2. **Create BigQuery Datasets**

- In the Google Cloud Console, go to BigQuery.
- Make two new datasets: `oken_spririts` for Airbyte and `oaken_transformed` for DBT.
  - **How to create a dataset:**
  - In the left sidebar, click on your project name.
  - Click “Create Dataset”.
  - Enter the dataset ID (either `oken_spririts` or `oaken_transformed`).
  - Click "Create Dataset".

### 3. **Create Service Accounts and Assign Roles**

- Go to “IAM & Admin” > “Service accounts” in the Google Cloud Console.
- Click “Create Service Account”.
- Name your service account (like `airbyte-service-account`).
- Assign the “BigQuery Data Editor” and “BigQuery Job User” roles to the service account.
- Follow the same steps to make another service account for DBT (like `DBT-service-account`) and assign the roles.
  - **How to create a service account and assign roles:**
    - While creating the service account, under the “Grant this service account access to project” section, click the “Role” dropdown.
    - Choose the “BigQuery Data Editor” and “BigQuery Job User” roles.
    - Finish the creation process.

### 4. **Generate JSON Keys for Service Accounts**

- For both service accounts, make a JSON key to let the service accounts sign in.
  - **How to generate JSON key:**
    - Find the service account in the “Service accounts” list.
    - Click on the service account name.
    - In the “Keys” section, click “Add Key” and pick JSON.
    - The key will download automatically. Keep it safe and don’t share it.
    - Do this for the other service account too.

## 3. Setting Up Airbyte Connectors

### 3.1 Launch Airbyte in Docker

- From the command line:
    1. `cd oaken-spirits/src/production/analytics/airbyte`
    1. Environment variables
        - Create a **.env** file
        - Copy **env-template** into **.env** file
        - In a single command: `cp env-template .env`
    1. Run `docker compose up -d`
    1. Run `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' oaken-mysql` and note the IP address returned. This needed to setup the MySQL source.

### 3.2. Setting Up Airbyte Connectors Using the UI

Start by launching the Airbyte UI by going to **<http://localhost:8000/>** in your browser. Then:

1. **Create a login (for first time login only)**:
    - enter an email = <admin@oakenspirits.org>
    - Organization name = Oaken Spirits
    - Select **Get started**

1. **Create a source**:
    1. Select **Create your first connection** in the middle of the page
        - Or go to the Sources tab and click on `+ New source`.
    1. Search for MySQL and select it.
    1. Set up connection
        - Source name = Oaken MySQL
        - Host = the IP address from above, it will not accept host or container name
        - port = 3306
        - Database = oaken
        - Username = airbyte
        - Password = airbyte
        - Leave all other settings as default
        - Select **Set up source** at the very bottom

1. **Create a destination**:
    1. You will have the prompt to set up a destination.
        - Note: Destinations can also be set up by going to the Destinations tab and click on `+ New destination`.
        - Search for “bigquery” using the search bar and select `BigQuery`.
            - Destination name = Oaken BigQuery
            - Project ID = Your Project ID
            - Dataset Location = Your location selected (US, EU, etc.)
            - Default Dataset ID = oaken_spirits
            - Loading Method = Standard Inserts
            - Service Account Key JSON = Copy and paste your key from `{` to `}`, the dull key.
                - How to get your key:
                    - This will print the contents to your command line. Just copy and past into the above field.
                    - `cat name-and-path-of-your-file.json`
                    - You can also open the file and copy the data.
        - Click on `Set up destination`.

1. **Complete connection**:
    - Under `Activate the streams you want to sync` select the greyed out tab for Sync. This will activate the schema of the MySQL database. All the tabs below should be active. If not, select them manually.
    - Click on `Set up connection`.

1. **Create a connection**: (only if you did not use create your first connection)
    - Go to the Connections tab and click on `+ New connection`.
    - Select the source and destination you just created.
    - Follow instructions above for **Complete connection**.

That’s it! Your connection is set up and ready to go! 🎉

## 4. Setting Up the DBT Project

[DBT (data build tool)](https://www.getDBT.com/) allows you to transform your data by writing, documenting, and executing SQL workflows. Setting up the DBT project requires specifying connection details for your data platform, in this case, BigQuery. Here’s a step-by-step guide to help you set this up:

1. **Navigate to the DBT Project Directory**:

    Move to the directory containing the DBT configuration:

    ```bash
    cd oaken-spirits/src/production/analytics/DBT_project
    ```

2. **Update Connection Details**:

   - You'll find a `profiles.yml` file within the directory. This file contains configurations for DBT to connect with your data platform. Update this file with your BigQuery connection details. Specifically, you need to update the Service Account JSON file path and your BigQuery project ID.
   - Provide your BigQuery project ID in the `database` field of the `DBT_project/models/sources/oaken_sources.yml` file.

If you want to avoid hardcoding credentials in the `profiles.yml` file, you can leverage environment variables. An example of how to use them in this file is provided for the `keyfile` key.

3. **Test the Connection**:

   Once you’ve updated the connection details, you can test the connection to your BigQuery instance using:

   ```bash
   DBT debug
   ```

If everything is set up correctly, this command should report a successful connection to BigQuery 🎉.

## 5. Orchestrating with Dagster

[Dagster](https://dagster.io/) is the chosen orchestrator.

1. **Navigate to the Orchestration Directory**:

    Switch to the directory containing the Dagster orchestration configurations:

    ```bash
    cd oaken-spirits/src/production/analytics/orchestration/dagster
    ```

2. **Set Environment Variables**:

   Dagster requires certain environment variables to be set to interact with other tools like DBT and Airbyte. Set the following variables:

    ```bash
    export DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1
    ```

3. **Launch the Dagster UI**:

    With the environment variables in place, kick-start the Dagster UI:

    ```bash
    dagster dev
    ```

4. **Access Dagster in Your Browser**:

    Open your browser and navigate to:

    ```text
    http://127.0.0.1:3000
    ```

Here, you should see assets for both Airbyte and DBT. To get an overview of how these assets interrelate, click on `view global asset lineage` at the top right corner of the Dagster UI. This will give you a clear picture of the data lineage, visualizing how data flows between the tools.

5. **Materialize Dagster Assets**:

    1. In the Dagster UI, click on `Materialize all`. This should trigger the full pipeline. First the Airbyte sync to extract data from MySQL and load it into BigQuery, and then DBT to transform the raw data, materializing the `staging` and `marts` models.
    1. You can go to the Airbyte UI and confirm a sync is running, and then.
    1. When the DBT jobs have run, go to your BigQuery console and check the views have been created in the `oaken_transformed` dataset.
