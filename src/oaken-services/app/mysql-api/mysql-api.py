import sys
import os
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import random
from datetime import datetime
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

try:
    for message in mysql_consumer:
        try:
            data = message.value
            # Customer
            storNumber = int(data.get('StoreNumber', ''))
            if not storNumber:
                logger.error("StoreNumber is null or invalid. Skipping insertion.")
                continue

            storeName = data.get('StoreName', '')
            address = data.get('Address', '')
            city = data.get('City', '')
            county = data.get('County', '')
            state = data.get('State', '')
            zip_code = int(data.get('ZipCode', ''))

            # vendor
            vendorNumber = int(float(data.get('VendorNumber', '')))
            if not vendorNumber:
                logger.error("VendorNumber is null or invalid. Skipping insertion.")
                continue

            vendorName = data.get('VendorName', '')

            # category
            category = int(float(data.get('Category','')))
            if not category:
                logger.error("Category is null or invalid. Skipping insertion.")
                continue

            categoryName = (data.get('CategoryName',''))

            # product
            itemNumber = int(data.get('ItemNumber', ''))
            if not itemNumber:
                logger.error("ItemNumber is null or invalid. Skipping insertion.")
                continue
            itemDescription = data.get('ItemDescription', '')
            pack = int(data.get('Pack', ''))
            volume = int(data.get('BottleVolumeML', ''))
            cost = float(data.get('BottleCost', '').replace('$', ''))
            retail = float(data.get('BottleRetail', '').replace('$', ''))

            # Sales
            invoice = data.get('Invoice', '')
            if not invoice:
                logger.error("Invoice is null or invalid. Skipping insertion.")
                continue

            date_string = data.get('Date', '')
            if not date_string:
                logger.error("Date is null or invalid. Skipping insertion.")
                continue

            sales_date = datetime.datetime.strptime(date_string, '%m/%d/%Y').date()

            amountSold = int(data.get('BottlesSold', ''))
            totalLiters = float(data.get('VolumeSoldLiters', ''))

            sales = float(data.get('SaleDollars', '').replace('$', ''))

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
                CUSTOMER_QUERY = '''
                    INSERT INTO customer (StoreNumber,StoreName,Address,City,County,State,ZipCode)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    '''
                customer_data = (storNumber,storeName,address,city,county,state,zip_code)
                mysql_cursor.execute(CUSTOMER_QUERY, customer_data)
                mysql_conn.commit()
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                continue

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
                continue

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
                continue

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
                continue

            try:
                SALES_QUERY = '''
                INSERT INTO sales (Invoice,StoreNumber,VendorNumber,SaleDate,SaleDollars,
                ItemNumber,VolumeSoldLiters,BottlesSold)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                '''
                sales_data = (invoice,storNumber,vendorNumber,sales_date,sales,itemNumber,
                              totalLiters,amountSold)
                mysql_cursor.execute(SALES_QUERY, sales_data)
                mysql_conn.commit()

                # Topic should post after MySQL processing to ensure data is in the database.
                INVOICES_info = {
                    'Invoice': invoice,
                    'SaleDate': sales_date,
                    'saleDollars': sales
                }

                invoice_producer.send(INVOICES_TOPIC, value=INVOICES_info)
                invoice_producer.flush()
            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)
                continue

        except Exception as e:
            logger.error(f"Error in Kafka consumer: {e}", exc_info=True)
            continue

finally:
    mysql_cursor.close()
    mysql_conn.close()
