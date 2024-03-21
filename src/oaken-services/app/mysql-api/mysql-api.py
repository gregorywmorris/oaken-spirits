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
    def __init__(self, bucket_name, folder, key):  # Update S3Handler to accept folder parameter
        super().__init__()
        self.bucket_name = bucket_name
        self.folder = folder  # Store folder name
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
        category = data.get('Category','')
        categoryName = ('CategoryName','')
        itemDescription = data.get('ItemDescription','')
        pack = data.get('Pack','')
        volume = data.get('BottleVolume(ml)','')
        cost = data.get('BottleCost','')
        retail = data.get('BottleRetail','')
        # Sales
        invoice = data.get('Invoice', '')
        if invoice is None:
            logger.error("Invoice is null. Skipping insertion.")
            continue
        date = data.get('Date', '')
        amountSold = data.get('BottlesSold','')
        totalLiters = data.get('VolumeSold(Liters)','')
        totalGallons = data.get('VolumeSold(Gallons)','')
        sales = data.get('Sale(Dollars)','')
        sales_amount = float(sales.replace('$', ''))

        invoice_date = datetime.datetime.strptime(date, '%m/%d/%Y')
        MYSQL_date = invoice_date + datetime.timedelta(days=random.randint(1, 4))

        # MySQL
        '''
        Multiple try/except blocks are used due to the simplistic invoicing application script.
        In a real world scenario, likely each of these blocks would be done as a truly separate process.
        The try/except prevents the duplicates failing to be added to the database preventing the rest of the processes from competing.
        '''

        try:
            CUSTOMER_QUERY = '''
                INSERT INTO customer (StoreNumber,StoreName,Address,City,County,State,ZipCode)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                '''
            customer_data = (storNumber,storeName,address,city,county,state,zip)
            mysql_cursor.execute(CUSTOMER_QUERY, customer_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

        try:
            VENDOR_QUERY = '''
                INSERT INTO vendor (VendorNumber,VendorName)
                VALUES (%s,%s)
                '''
            vendor_data = (storNumber,storeName,address,city,county,state,zip)
            mysql_cursor.execute(VENDOR_QUERY,vendor_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

        try:
            PRODUCT_QUERY = '''
                INSERT INTO product (ItemNumber,Category,CategoryName,ItemDescription,Pack,
                BottleVolume(ml),BottleCost,BottleRetail)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                '''
            product_data = (itemNumber,category,categoryName,itemDescription,pack,volume,cost,retail)
            mysql_cursor.execute(PRODUCT_QUERY, product_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

        try:
            SALES_QUERY = '''
            INSERT INTO sales (Invoice,date,amountSold,totalLiters,sales)
            VALUES (%s,%s,%s,%s,%s)
            '''
            sales_data = (invoice,date,amountSold,totalLiters,sales_amount)
            mysql_cursor.execute(SALES_QUERY, sales_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")

        # Topic should post after MySQL processing to ensure data is in the database.
        INVOICES_info = {
            'Invoice/Item Number': invoice,
            'Date': date,
            'sales': sales_amount,
            'MYSQL Date': MYSQL_date.strftime('%m/%d/%Y')
        }

        invoice_producer.send(INVOICES_TOPIC, value=INVOICES_info)
        invoice_producer.flush()

    except Exception as e:
        logger.error(f"Error processing message: {e}")

# Close MySQL connection
mysql_cursor.close()
mysql_conn.close()
