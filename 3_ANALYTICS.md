# Analytics

## Airbyte

1. `cd src/production/analytics/airbyte`
1. Environment variables
    - Create a **.env** file
    - Copy **env-template** into **.env** file
    - In a single command: `cp env-template .env`
1. `nohup ./run-ab-platform.sh &`
1. Run `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' oaken-mysql` and note the IP address returned. This needed to setup the MySQL source.
1. Open browser and go to `localhost8000`
1. Create a login
    - enter an email = admin@oakenspirits.org
    - Organization name = Oaken Spirits
    - Select **Get started**
1. Select **Create your first connection** in the middle of the page
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
1. You will have the prompt to set up a destination. Search for BigQuery
    - Destination name = Oaken BigQuery
    - Project ID = Your Project ID
    - Dataset Location = Your location selected (US, EU, etc.)
    - Default Dataset ID = oaken_spirits
    - Loading Method = Standard Inserts
    - Service Account Key JSON = Copy and paste your key from `{` to `}`
        - How to get your key:
            - This will print the contents to your command line. Just copy and past into the above field.
            - `cat name-and-path-of-your-file.json`
            - You can also open the file and copy the data.

## DBT

1. 