# Cloud Beaver

Cloud Beaver community edition is a free product from [DBeaver](https://dbeaver.com/download/cloudbeaver/). DBeaver allows connection to multiple databases though one interface.

The GitHub repository is [here](https://github.com/dbeaver/cloudbeaver) and you can find the docker image [here](https://hub.docker.com/r/dbeaver/cloudbeaver).

1. In your browser go to `localhost:8978`
1. Select the **Next** button
1. Internal Server Configuration page
    - In **ADMINISTRATOR CREDENTIALS** enter desired login credentials
1. Select **Next** and then **Finish**
1. Login
1. Select the cbeaver icon in the upper left
1. Select the **+** icon and choose MySQL from the list
1. Enter the information shown here
    - Enter either **Host** name or IP address)
    - Enter **Port** 3306
    - Select **DRIVER PROPERTIES** from the top menu
        - for **allowPublicKeyRetrieval** select **TRUE** from the drop down list
    - Select **Test** and in the bottom right you should get pop up with a green check and **Connection is Established**
    - Select **Create**
1. create tables
    - Select the connection on the left
    - Select the **oaken** database
    - Select **SQL** button above.
    - Note: You must select the connection on the left and the database else the SQL editor will not associate with the connection. The tool is designed for multiple connections, so one must be selected. Alternatively the database can be chose from the option above.
    - From `app/mysql/` open `init.sql` and copy into the SQL editor
    - In the SQL editor highlight each `CREATE TABLE` statement and select the orange arrow on the left or selecting the orange document icon on the left will run the entire script.
1. MySQl is ready for data ingestion
