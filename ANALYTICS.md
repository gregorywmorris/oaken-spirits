# Oaken Spirits Analytics Stack with Airbyte, dbt, Dagster and BigQuery

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting an environment for your project](#1-setting-an-environment-for-your-project)
- [Setting Up BigQuery to work with Airbyte and dbt](#2-setting-up-bigquery)
- [Setting Up Airbyte Connectors](#3-setting-up-airbyte-connectors)
- [Setting Up the dbt Project](#4-setting-up-the-dbt-project)
- [Orchestrating with Dagster](#5-orchestrating-with-dagster)
- [Next Steps](#next-steps)

## Prerequisites

Before you embark on this integration, ensure you have the following set up and ready:

1. **Python 3.11 or later**

2. **Docker and Docker Compose (Docker Desktop)**: Install [Docker](https://docs.docker.com/get-docker/) following the official documentation for your specific OS.

3. **Airbyte OSS version**: Deploy the open-source version of Airbyte locally. Follow the installation instructions from the [Airbyte Documentation](https://docs.airbyte.com/quickstart/deploy-airbyte/).

5. **Google Cloud account with BigQuery**: You will also need to add the necessary permissions to allow Airbyte and dbt to access the data in BigQuery. A step-by-step guide is provided [below](#2-setting-up-bigquery).

## 1. Setting an environment for your project

Get the project up and running on your local machine by following these steps:

- **Navigate to the directory**:

    ```bash
   cd src/production/analytics
   ```

## 2. Setting Up BigQuery

#### 1. **Create a Google Cloud Project**
   - If you have a Google Cloud project, you can skip this step.
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the "Select a project" dropdown at the top right and select "New Project".
   - Give your project a name and follow the steps to create it.

#### 2. **Create BigQuery Datasets**
   - In the Google Cloud Console, go to BigQuery.
   - Make two new datasets: `oken_spririts` for Airbyte and `oaken_transformed` for dbt.
     - If you pick different names, remember to change the names in the code too.
   
   **How to create a dataset:**
   - In the left sidebar, click on your project name.
   - Click “Create Dataset”.
   - Enter the dataset ID (either `oken_spririts` or `oaken_transformed`).
   - Click "Create Dataset".

#### 3. **Create Service Accounts and Assign Roles**
   - Go to “IAM & Admin” > “Service accounts” in the Google Cloud Console.
   - Click “Create Service Account”.
   - Name your service account (like `airbyte-service-account`).
   - Assign the “BigQuery Data Editor” and “BigQuery Job User” roles to the service account.
   - Follow the same steps to make another service account for dbt (like `dbt-service-account`) and assign the roles.

   **How to create a service account and assign roles:**
   - While creating the service account, under the “Grant this service account access to project” section, click the “Role” dropdown.
   - Choose the “BigQuery Data Editor” and “BigQuery Job User” roles.
   - Finish the creation process.
   
#### 4. **Generate JSON Keys for Service Accounts**
   - For both service accounts, make a JSON key to let the service accounts sign in.
   
   **How to generate JSON key:**
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

Start by launching the Airbyte UI by going to **http://localhost:8000/** in your browser. Then:

1. **Create a login (for first time login only)**:
    - enter an email = admin@oakenspirits.org
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

## 4. Setting Up the dbt Project

[dbt (data build tool)](https://www.getdbt.com/) allows you to transform your data by writing, documenting, and executing SQL workflows. Setting up the dbt project requires specifying connection details for your data platform, in this case, BigQuery. Here’s a step-by-step guide to help you set this up:

1. **Navigate to the dbt Project Directory**:

    Move to the directory containing the dbt configuration:
    ```bash
    cd oaken-spirits/src/production/analytics/dbt_project
    ```

2. **Update Connection Details**:

   - You'll find a `profiles.yml` file within the directory. This file contains configurations for dbt to connect with your data platform. Update this file with your BigQuery connection details. Specifically, you need to update the Service Account JSON file path and your BigQuery project ID.
   - Provide your BigQuery project ID in the `database` field of the `dbt_project/models/sources/oaken_sources.yml` file.

If you want to avoid hardcoding credentials in the `profiles.yml` file, you can leverage environment variables. An example of how to use them in this file is provided for the `keyfile` key.

3. **Test the Connection**:

   Once you’ve updated the connection details, you can test the connection to your BigQuery instance using:
   ```bash
   dbt debug
   ```
If everything is set up correctly, this command should report a successful connection to BigQuery 🎉.

## 5. Orchestrating with Dagster

[Dagster](https://dagster.io/) is a modern data orchestrator designed to help you build, test, and monitor your data workflows. In this section, we'll walk you through setting up Dagster to oversee both the Airbyte and dbt workflows:

1. **Navigate to the Orchestration Directory**:

   Switch to the directory containing the Dagster orchestration configurations:
   ```bash
   cd ../orchestration
   ```

2. **Set Environment Variables**:

   Dagster requires certain environment variables to be set to interact with other tools like dbt and Airbyte. Set the following variables:

   ```bash
   export DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1
   export AIRBYTE_PASSWORD=password
   ```
   
   Note: The `AIRBYTE_PASSWORD` is set to `password` as a default for local Airbyte instances. If you've changed this during your Airbyte setup, ensure you use the appropriate password here.

3. **Launch the Dagster UI**:

   With the environment variables in place, kick-start the Dagster UI:
   ```bash
   dagster dev
   ```

4. **Access Dagster in Your Browser**:

   Open your browser and navigate to:
   ```
   http://127.0.0.1:3000
   ```
Here, you should see assets for both Airbyte and dbt. To get an overview of how these assets interrelate, click on `view global asset lineage` at the top right corner of the Dagster UI. This will give you a clear picture of the data lineage, visualizing how data flows between the tools.

5. **Materialize Dagster Assets**:

   In the Dagster UI, click on `Materialize all`. This should trigger the full pipeline. First the Airbyte sync to extract data from Faker and load it into BigQuery, and then dbt to transform the raw data, materializing the `staging` and `marts` models.

You can go to the Airbyte UI and confirm a sync is running, and then, once the dbt jobs have run, go to your BigQuery console and check the views have been created in the `transformed data` dataset.

## Next Steps

Congratulations on deploying and running the E-commerce Analytics Quistart! 🎉 Here are some suggestions on what you can explore next to dive deeper and get more out of your project:

### 1. **Explore the Data and Insights**
   - Dive into the datasets in BigQuery, run some queries, and explore the data you've collected and transformed. This is your chance to uncover insights and understand the data better!

### 2. **Optimize Your dbt Models**
   - Review the transformations you’ve applied using dbt. Try optimizing the models or create new ones based on your evolving needs and insights you want to extract.

### 3. **Expand Your Data Sources**
   - Add more data sources to Airbyte. Explore different types of sources available, and see how they can enrich your existing datasets and broaden your analytical capabilities.

### 4. **Enhance Data Quality and Testing**
   - Implement data quality tests in dbt to ensure the reliability and accuracy of your transformations. Use dbt's testing features to validate your data and catch issues early on.

### 5. **Automate and Monitor Your Pipelines**
   - Explore more advanced Dagster configurations and setups to automate your pipelines further and set up monitoring and alerting to be informed of any issues immediately.

### 6. **Scale Your Setup**
   - Consider scaling your setup to handle more data, more sources, and more transformations. Optimize your configurations and resources to ensure smooth and efficient processing of larger datasets.

### 7. **Contribute to the Community**
   - Share your learnings, optimizations, and new configurations with the community. Contribute to the respective tool’s communities and help others learn and grow.

