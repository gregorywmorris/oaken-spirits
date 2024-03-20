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
    def __init__(self, bucket_name, key):
        super().__init__()
        self.bucket_name = bucket_name
        self.key = key
        self.s3_client = boto3.client('s3')

    def emit(self, record):
        log_entry = self.format(record) + '\n'
        self.upload_log(log_entry)

    def upload_log(self, log_entry):
        self.s3_client.put_object(Body=log_entry, Bucket=self.bucket_name, Key=self.key)

# Create an instance of the S3Handler
s3_handler = S3Handler(bucket_name=MYSQL_LOG_BUCKET, key='MYSQL.log')
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
        storNumber = data.get('store number','')
        storeName = data.get('Store Name','')
        address = data.get('Address','')
        city = data.get('City','')
        state = data.get('State','')
        zip = data.get('Zip Code','')
        county = data.get('Count','')
        # Vendor
        vendorNumber = data.get('Vendor Number','')
        vendorName = data.get('Vendor Name','')
        # Product
        itemNumber = data.get('Item Number','')
        itemDescription = data.get('Item Description','')
        pack = data.get('Pack','')
        volume = data.get('Bottle Volume (ml)','')
        cost = data.get('State Bottle Cost','')
        retail = data.get('State Bottle Retail','')
        # Sales
        invoice = data.get('Invoice/Item Number', '')
        date = data.get('Date', '')
        amountSold = data.get('Bottles Sold','')
        totalLiters = data.get('Volume Sold (Liters)','')
        totalGallons = data.get('Volume Sold (Gallons)','')
        sales = data.get('Sale (Dollars)','')
        sales_amount = float(sales.replace('$', ''))

        invoice_date = datetime.datetime.strptime(date, '%m/%d/%Y')
        MYSQL_date = invoice_date + datetime.timedelta(days=random.randint(1, 4))

        # MySQL
        
        try:
        CUSTOMER_QURY = '''
            INSERT INTO customer (Store Number, )
            VALUES (%s, %s, %s)
        '''
        except Exception as e:
            logger.error(f"Error processing message: {e}")
        
        UPDATE_QUERY = """
            UPDATE sales
            SET MYSQLDate = %s, MYSQLCost = %s
            WHERE InvoiceItemNumber = %s
        """

        update_data = (MYSQL_date.strftime('%Y-%m-%d'), MYSQL_cost, invoice)
        mysql_cursor.execute(UPDATE_QUERY, update_data)

        mysql_conn.commit()

        # Topic should post after MySQL processing to ensure data is in the database.
        INVOICES_info = {
            'Invoice/Item Number': invoice,
            'Date': date,
            'sales': sales,
            'MYSQL Date': MYSQL_date.strftime('%m/%d/%Y'),
        }

        invoice_producer.send(INVOICES_TOPIC, value=INVOICES_info)
        invoice_producer.flush()

    except Exception as e:
        logger.error(f"Error processing message: {e}")

# Close MySQL connection
mysql_cursor.close()
mysql_conn.close()
