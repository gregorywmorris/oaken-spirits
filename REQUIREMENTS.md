# Project Requirements

> [!IMPORTANT]
> This project simulates a data center on a local PC. Underpowered PCs may have difficulty running all process simultaneously. In particular when uploading data to BigQuery.

> [!TIP]
> If having or concerned about having difficulty, consider the following:
>
> 1. Run the business services for a short period to confirm the flow then stop the invoice notebook.
> 1. Stop these docker services after you have run them for at least a few minutes (**oaken-mysql must stay running!**):
>    - dbeaver
>    - shipping
>    - accounting
>    - kafka: all instances and zookeeper
> 1. Compare your device to mine to prepare for any difficulty.
>    - **Note:** While it's not mandatory for your PC to match mine, I can only assure optimal operation based on my own system. Other hardware configurations may yield different results.
>       - 12 core (24 logical) CPU at 4.2 GHZ
>       - 48 GB of ram
>       - 2 TB NVME SSD drive
>       - Nvidia 3080 GPU

## 1. Local environment

### Python environment, choose one of the following

1. Pipenv
    - `python -m venv .venv`
    - Linux
        - `source .venv/bin/activate`
    - Windows
        - `.venv\Scripts\activate`
1. Anaconda or Miniconda
    - Using Anaconda or Miniconda strongly advised.
    - [Anaconda installation instructions](https://docs.anaconda.com/free/anaconda/install/index.html) if not already installed.
    - [Miniconda installation instructions](https://docs.anaconda.com/free/miniconda/)
    - `conda create -n oaken`

> [!NOTE]
> In VS code, **Ctrl+Shift+p** pulls up option to select Python interpreter.

### After activating environment

- PDM `.toml` file in main directory.
    1. Activate environment of choice.
    1. `pip install pdm`
    1. `pdm install`

### Docker and Docker Compose (Docker Desktop)

Install [Docker](https://docs.docker.com/get-docker/) following the official documentation for your specific OS.

## 2. Setting Up BigQuery

### 1. Create a Google Cloud Project

- If you have a Google Cloud project, you can skip this step if you wish to use your existing project.
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Click on the "Select a project" dropdown at the top right and select "New Project".
- Give your project a name and follow the steps to create it.

### 2. Create BigQuery Datasets

- In the Google Cloud Console, go to BigQuery.
- Make two new datasets: `oaken_spirits` for **Airbyte** and `oaken_transformed` for **DBT**.
  - **How to create a dataset:**
    - In the left sidebar, click on your project name.
    - Click “Create Dataset”.
    - Enter the dataset ID  `oaken_spirits`.
    - Click "Create Dataset".
    - Repeat these steps for `oaken_transformed`.
- Copy and run the `oaken-spirits/src/production/analytics/bigquery/bigquery.sql` in BigQuery.

### 3. Create Service Accounts and Assign Roles

- Go to “IAM & Admin” > “Service accounts” in the Google Cloud Console.
- Click “Create Service Account”.
- Name your service account, `oaken-service-account`.
- Assign the “BigQuery Data Editor” and “BigQuery Job User” roles to the service account.
  - **How to create a service account and assign roles:**
    - While creating the service account, under the “Grant this service account access to project” section, click the “Role” dropdown.
    - Choose the “BigQuery Data Editor” and “BigQuery Job User” roles.
    - Finish the creation process.

### 4. Generate JSON Keys for Service Accounts

- For service account, make a JSON key to let the service accounts sign in.
  - **How to generate JSON key:**
    - Find the service account in the “Service accounts” list.
    - Click on the service account name.
    - In the “Keys” section, click “Add Key” and pick JSON.
    - The key will download automatically. Keep it safe and don’t share it.
    - This key location is needed for the analytics portion of the project.

## 3. Data prep

1. [Dataset](https://www.kaggle.com/datasets/residentmario/iowa-liquor-sales)
1. Download and move dataset to `oaken-spirits/src/data`
1. Unzip and save as **iowa-liquor-sales_dirty.csv** - 3.47 GB file

    ```bash
    unzip iowa-liquor-sales.zip 'iowa-liquor-sales_dirty.csv'
    ```

1. Go to `oaken-spirits/src/non-production/data-preprocessing`
1. Open `data-cleaning.ipynb` and **Run All**.
