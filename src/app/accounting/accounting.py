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

# Kafka consumers
shipping_consumer = KafkaConsumer(
    'shipping',
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',  # Start consuming from the earliest offset
    enable_auto_commit=True,       # Automatically commit offsets
    group_id='oaken_accounting_group',  # Specify a consumer group
    value_deserializer=lambda x: loads(x.decode('utf-8')))

shipping_consumer.subscribe(topics='shipping')

for shipping_message in shipping_consumer:
    try:
        shipping_data = shipping_message.value

        invoice = shipping_data.get('Invoice', '')

        shipping_expense = float(shipping_data.get('ShippingCost')) * -1

        sales = float(shipping_data.get('SaleDollars'))

        # MySQL
        try:
            LEDGER_CREDIT = """
                INSERT INTO salesLedger (Invoice, Credit, Note)
                VALUES (%s, %s, 'Sale')
            """
            credit_data = (invoice, sales)
            mysql_cursor.execute(LEDGER_CREDIT, credit_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            pass

        try:
            LEDGER_DEBIT = """
                INSERT INTO salesLedger (Invoice, Debit, Note)
                VALUES (%s, %s, 'Shipping')
            """
            debit_data = (invoice, shipping_expense)
            mysql_cursor.execute(LEDGER_DEBIT, debit_data)
            mysql_conn.commit()
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            pass

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        pass

mysql_cursor.close()
mysql_conn.close()