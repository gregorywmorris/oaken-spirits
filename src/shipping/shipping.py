import sys
sys.path.append('..')

import json
import logging
from variables import KAFKA_SERVER, INVOICES_TOPIC, SHIPPING_TOPIC, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, LOG_BUCKET
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import random
import datetime
import mysql.connector
import boto3
from logging.handlers import RotatingFileHandler

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Create a file handler to log errors
file_handler = RotatingFileHandler('shipping.log', maxBytes=10*1024*1024, backupCount=5)
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
s3_handler = S3Handler(bucket_name= LOG_BUCKET, key='shipping.log')
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
sales_consumer = KafkaConsumer(
    INVOICES_TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    value_deserializer=lambda x: loads(x.decode('utf-8')))

shipping_producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

for message in sales_consumer:
    try:
        data = message.value
        date = data.get('Date', '')
        sales = data.get('Sale (Dollars)', '')
        invoice = data.get('Invoice/Item Number', '')

        sales_amount = float(sales.replace('$', ''))

        shipping_cost = sales_amount * 0.05

        invoice_date = datetime.datetime.strptime(date, '%m/%d/%Y')
        shipping_date = invoice_date + datetime.timedelta(days=random.randint(1, 4))

        shipping_info = {
            'Invoice/Item Number': invoice,
            'Date': date,
            'Shipping Date': shipping_date.strftime('%m/%d/%Y'),
            'Shipping Cost': shipping_cost
        }

        shipping_producer.send(SHIPPING_TOPIC, value=shipping_info)
        shipping_producer.flush()

        # MySQL
        UPDATE_QUERY = """
            UPDATE sales
            SET ShippingDate = %s, ShippingCost = %s
            WHERE InvoiceItemNumber = %s
        """

        update_data = (shipping_date.strftime('%Y-%m-%d'), shipping_cost, invoice)
        mysql_cursor.execute(UPDATE_QUERY, update_data)

        mysql_conn.commit()
    except Exception as e:
        logger.error(f"Error processing message: {e}")

# Close MySQL connection
mysql_cursor.close()
mysql_conn.close()
