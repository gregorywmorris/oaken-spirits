# Cloud Beaver

Cloud Beaver community edition is a free product from [DBeaver](https://dbeaver.com/download/cloudbeaver/). DBeaver allows connection to multiple databases though one interface.

The GitHub repository is [here](https://github.com/dbeaver/cloudbeaver) and you can find the docker image [here](https://hub.docker.com/r/dbeaver/cloudbeaver).

1. In your browser go to `localhost:8978`
1. Select the **Next** button
1. Internal Server Configuration page
    - In the bottom right, enter desired login credentials
1. Select **Next** and then **Finish**
1. Login
1. Select the cbeaver icon in the upper left
1. Select the **+** icon and choose MySQL from the list
1. Enter the information shown here
    - Note: User name and User password have been defined in the .env file. You would have to change them there before running docker-compose to change them here
    - Select **Test** and in the bottom right you should get pop up with a green check and **Connection is Established**
    - Select **Create**
1. Select the connection on the right then select the **SQL** button above.
    - Note: You must select the connection on the right else the SQL editor will not associate with the connection. The tool is meant for multiple connections, so one must be selected.
1. create tables
    - From `app/mysql/` open `init.sql`
    - You must highlight each `CREATE TABE` statement and select the orange arrow on the left
    - Note: script is written to be run all at once but at this time it will fail. So just run each statement
1. MySQl is ready for data ingestion
