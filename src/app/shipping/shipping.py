import sys
sys.path.append('..')

import os
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import random
from datetime import datetime
import mysql.connector
from logging.handlers import RotatingFileHandler

# env
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Create a logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Create a RotatingFileHandler
file_handler = RotatingFileHandler('example.log', maxBytes=10000, backupCount=5)
file_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Attach the handler to the logger
logger.addHandler(file_handler)

# Log messages
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')

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
    'invoices',
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',  # Start consuming from the earliest offset
    enable_auto_commit=True,       # Automatically commit offsets
    group_id='oaken_shipping_group',  # Specify a consumer group
    value_deserializer=lambda x: loads(x.decode('utf-8')))

sales_consumer.subscribe(topics='invoices')

shipping_producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))

for message in sales_consumer:
    try:
        data = message.value
        invoice = data.get('Invoice', '')

        date_str = data.get('SaleDate')
        sales_date = datetime.datetime.strptime(date_str, '%m/%d/%Y').date()

        sales = data.get('saleDollars')

        shipping_cost = round(float(sales) * 0.05,2)

        random_days = random.randint(0, 4)
        shipping_date = sales_date + datetime.timedelta(days=random_days)

        sales_consumer.commit()
        # MySQL
        UPDATE_QUERY = """
            UPDATE sales
            SET ShippingDate = %s, ShippingCost = %s
            WHERE Invoice = %s
        """

        update_data = (shipping_date, shipping_cost, invoice)
        mysql_cursor.execute(UPDATE_QUERY, update_data)

        mysql_conn.commit()
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        pass

    try:
        # Kafka topic
        shipping_cost = str(shipping_cost)
        shipping_date = str(shipping_date)
        shipping_info = {
            'Invoice': invoice,
            'SalesDate': date_str,
            'SaleDollars': sales,
            'ShippingDate': shipping_date,
            'ShippingCost': shipping_cost
        }

        shipping_producer.send('shipping', value=shipping_info)
        shipping_producer.flush()
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        pass

# Close MySQL connection
mysql_cursor.close()
mysql_conn.close()