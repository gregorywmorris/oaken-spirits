.
├── 1A_KAFKA_AWS.md
├── 2A_AWS.md
├── 2B_LOCAL_DOCKER.md
├── 3_ANALYTICS.md
├── AWS_S3.md
├── CLOUD_BEAVER.md
├── DAEMON.md
├── EC2.md
├── ENV_VARIABLE.md
├── OAKEN_TECHNICAL_DESIGN.md
├── README.md
├── TERRAFORM.md
├── images
│   ├── oaken-service-diagram.png
│   └── oaken-spirits-logo.png
└── src
    ├── __pycache__
    │   └── variables.cpython-311.pyc
    ├── archive
    │   └── old-dockerfile.yml
    ├── data
    │   ├── Iowa_Liquor_Sales.csv
    │   ├── Iowa_Liquor_Sales_dirty.csv
    │   └── iowa-liquor-sales.zip
    ├── non-production
    │   ├── aws-dev
    │   │   └── s3.py
    │   ├── data-preprocessing
    │   │   └── data-cleaning.ipynb
    │   └── test
    │       ├── mysql-api.log
    │       ├── test-accounting.ipynb
    │       ├── test-mysql-api.ipynb
    │       ├── test-shipping.ipynb
    │       └── test.py
    └── production
        ├── accounting.yml
        ├── accounting_runner.sh
        ├── app
        │   ├── accounting
        │   │   ├── accounting.py
        │   │   └── accounting_kafka_processor.service
        │   ├── mysql
        │   │   ├── delete.sql
        │   │   └── init.sql
        │   ├── mysql-api
        │   │   ├── mysql-api.py
        │   │   └── mysql_kafka_processor.service
        │   ├── shipping
        │   │   ├── shipping.py
        │   │   └── shipping_kafka_processor.service
        │   └── steaming-invoice
        │       └── streaming-invoice.ipynb
        ├── aws
        │   ├── app -> ../app
        │   ├── main.tf
        │   ├── provider.tf
        │   └── terraform.tfstate
        ├── create-topics.sh
        ├── docker-compose.yml
        ├── docker.env.template
        ├── env_variables.sh
        ├── mysql-kafka-processor.yml
        ├── mysql_api_runner.sh
        ├── shipping.yml
        └── shipping_runner.sh