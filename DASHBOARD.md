# Dashboard

[Stack overflow BQ export](https://stackoverflow.com/questions/54317565/how-can-i-export-data-from-bigquery-to-an-external-server-in-a-csv)

1. Login to GCP
1. Go to API Library, then select the link for it.
    - Search for and enable each of these APIs
        - Cloud Build API
        - Artifact Registry API
        - Cloud Logging API
        - Cloud Run Admin API
        - Cloud Functions API
    - Alternatively, go to Cloud Functions
        - On the right, start Create HTTP function tutorial
        - Click enable API's. 
        - You do do not need to complete the quick start. We just need the APIs enabled.
1. Go to Cloud Storage
    - Click **Create**
    - Name your bucket. Note this has to be globally unique.
    - Keep defaults and select **Next** through all the prompts and **Create**.
1. Go to Cloud Functions
    - Select **Create Function**
    - Set function name to **oaken-shipping**
    - Ensure **Require authentication** is selected
    - Click **Next**
    - For Runtime, select the dropdown and choose Python 3.11
    - Entry point, change name to **shipping_http**
    - Select main.py
        - Copy and paste the code from `src/production/analytics/dashboard/cloudFunction.py` into the main.py. Be sure to clear any data that was in it first.
            - Edit these fields:
                - project_name = "your project id"
                - bucket_name = "name you chose for the bucket"
                - (at line 22) location = "US" # change if you are using a different location.
    - Select requirements.txt
        - Copy contents from `src/production/analytics/dashboard/requirements.txt`
    - Click **Deploy**
    - The job will fail
    - select the **Permissions** tab.
    - Under **VIEW BY PRINCIPLE**
        - check the box for the **Principle** that has the nane **Google cloud Functions Service Agent**.
        - Select **GRANT ACCESS**
        