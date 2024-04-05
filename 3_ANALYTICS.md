# Airbyt

1. `cd src/production/analytics/airbyte`
1. `nohup ./run-ab-platform.sh &`
1. Create a login
    - enter an email = admin@oakenspirits.org
    - Organization name = Oaken Spirits
    - Select **Get started**
1. Select **Create your first connection** in the middle of the page
    - You can also select sources from the left window
1. Search for MySQL and select it.
1. Set up connection
    - Host = oaken-mysql
    - port = 3306
    - Database = oaken
    - Username = mysql
    - Password = mysql
    - Leave all other settings as default
    - Select **Set up source** at the very bottom
