import sys
sys.path.append('..')

import os
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import random
import datetime
import mysql.connector
import boto3
from logging.handlers import RotatingFileHandler

# env
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
INVOICES_TOPIC = os.getenv('INVOICES_TOPIC')
MYSQL_TOPIC = os.getenv('MYSQL_TOPIC')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_LOG_BUCKET = os.getenv('MYSQL_LOG_BUCKET')
LOG_FOLDER = os.getenv('LOG_FOLDER')

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Create a file handler to log errors
file_handler = RotatingFileHandler('MYSQL.log', maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Custom logging handler to upload logs to S3
class S3Handler(logging.StreamHandler):
    def __init__(self, bucket_name, folder, key): 
        super().__init__()
        self.bucket_name = bucket_name
        self.folder = folder
        self.key = key
        self.s3_client = boto3.client('s3')

    def emit(self, record):
        log_entry = self.format(record) + '\n'
        self.upload_log(log_entry)

    def upload_log(self, log_entry):
        # Construct the full key including the folder
        full_key = f"{self.folder}/{self.key}"
        self.s3_client.put_object(Body=log_entry, Bucket=self.bucket_name, Key=full_key)

# Create an instance of the S3Handler with folder parameter
s3_handler = S3Handler(bucket_name=MYSQL_LOG_BUCKET, folder=LOG_FOLDER, key='accounting.log')
s3_handler.setLevel(logging.ERROR)
logger.addHandler(s3_handler)

# MySQL connection
mysql_conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
mysql_cursor = mysql_conn.cursor()

# Kafka
mysql_consumer = KafkaConsumer(
    MYSQL_TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    value_deserializer=lambda x: loads(x.decode('utf-8')))

mysql_consumer.subscribe(topics=[MYSQL_TOPIC])

invoice_producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))


for message in mysql_consumer:
    try:
        data=message.value
        # Customer
        storNumber = data.get('StoreNumber','')
        if storNumber is None:
            logger.error("StoreNumber is null. Skipping insertion.")
            continue
        storeName = data.get('StoreName','')
        address = data.get('Address','')
        city = data.get('City','')
        countyNumber = data.get('CountyNumber','')
        county = data.get('County','')
        state = data.get('State','')
        zip = data.get('ZipCode','')
        # Vendor
        vendorNumber = data.get('VendorNumber','')
        if vendorNumber is None:
            logger.error("VendorNumber is null. Skipping insertion.")
            continue
        vendorName = data.get('VendorName','')
        # Product
        itemNumber = data.get('ItemNumber','')
        if itemNumber is None:
            logger.error("ItemNumber is null. Skipping insertion.")
            continue
        category = data.get('CategoryNumber','')
        categoryName = ('CategoryName','')
        itemDescription = data.get('ItemDescription','')
        pack = data.get('Pack','')
        volume = data.get('BottleVolumeML','')
        cost = data.get('BottleCost','')
        retail = data.get('BottleRetail','')
        # Sales
        invoice = data.get('Invoice', '')
        if invoice is None:
            logger.error("Invoice is null. Skipping insertion.")
            continue
        date = data.get('Date', '')
        amountSold = data.get('BottlesSold','')
        totalLiters = data.get('VolumeSoldLiters','')
        sales = data.get('SaleDollars','')
        sales_amount = float(sales.replace('$', ''))

        invoice_date = datetime.datetime.strptime(date, '%m/%d/%Y')
        MYSQL_date = invoice_date + datetime.timedelta(days=random.randint(1, 4))

        # MySQL
        '''
        Multiple try/except blocks are used due to the simplistic invoicing
        application script.

        In a real world scenario, likely each of these blocks would be done
        as a truly separate process.

        The try/except prevents the duplicates failing to be added to the
        database from preventing the rest of the processes from competing.
        '''

        try:
            COUNTY_QUERY = '''
                INSERT INTO country (CountyNumber,CountyName)
                VALUES (%s,%s)
                '''
            county_data = (countyNumber,county)
            mysql_cursor.execute(COUNTY_QUERY, county_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

        try:
            CUSTOMER_QUERY = '''
                INSERT INTO customer (StoreNumber,StoreName,Address,City,CountyNumber,State,ZipCode)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                '''
            customer_data = (storNumber,storeName,address,city,countyNumber,state,zip)
            mysql_cursor.execute(CUSTOMER_QUERY, customer_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

        try:
            VENDOR_QUERY = '''
                INSERT INTO vendor (VendorNumber,VendorName)
                VALUES (%s,%s)
                '''
            vendor_data = (vendorNumber,vendorName)
            mysql_cursor.execute(VENDOR_QUERY,vendor_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

        try:
            CATEGORY_QUERY = '''
                INSERT INTO category (CategoryNumber,CategoryName)
                VALUES (%s,%s)
                '''
            category_data = (category,categoryName)
            mysql_cursor.execute(CATEGORY_QUERY, category_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

        try:
            PRODUCT_QUERY = '''
                INSERT INTO product (ItemNumber,CategoryNumber,ItemDescription,BottleVolumeML,
                Pack,BottleCost,BottleRetail)
                VALUES (%s,%s,%s,%s,%s,%s,%s,)
                '''
            product_data = (itemNumber,category,itemDescription,volume,pack,cost,retail)
            mysql_cursor.execute(PRODUCT_QUERY, product_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

        try:
            SALES_QUERY = '''
            INSERT INTO sales (Invoice,StoreNumber,VendorNumber,SaleDate,SaleDollars,
            ItemNumber,VolumeSoldLiters,BottlesSold)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            sales_data = (invoice,storNumber,vendorNumber,date,sales_amount,itemNumber,totalLiters,amountSold)
            mysql_cursor.execute(SALES_QUERY, sales_data)
            mysql_conn.commit()

            # Topic should post after MySQL processing to ensure data is in the database.
            INVOICES_info = {
                'Invoice': invoice,
                'SaleDate': date,
                'saleDollars': sales_amount
            }

            invoice_producer.send(INVOICES_TOPIC, value=INVOICES_info)
            invoice_producer.flush()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")

