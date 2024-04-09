# Project Requirements

## 1. Setting an environment for your project

### Python environment, choose one of the following:

1. Pipenv
    - `python -m venv .venv`
    - Linux
        - `source .venv/bin/activate`
    - Windows
        - `.venv\Scripts\activate`
1. Anaconda
    - [Installation instructions](https://docs.anaconda.com/free/anaconda/install/index.html) if not already installed.
    - `conda create -n oaken`

> [!NOTE]
> 1. In VS code, **Ctrl+Shift+p** pulls up option to select Python interpreter.
> 1. requirments.txt cannot be used to import into Python environment.

### After activating environment:
1. PDM
    - PDM `.toml` file in main directory.
    - Activate environment of choice.
    - `pip install pdm`
    - `pdm install`

1. **Docker and Docker Compose (Docker Desktop)**: Install [Docker](https://docs.docker.com/get-docker/) following the official documentation for your specific OS.


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