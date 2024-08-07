#!/usr/bin/env python3
import sys
sys.path.append('..')

import os
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import random
from datetime import datetime, timedelta
import mysql.connector
from logging.handlers import RotatingFileHandler
from time import sleep
import boto3


# env
client = boto3.client('ssm')
KAFKA_SERVER = client.get_parameter('KAFKA_SERVER',WithDecryption=True)
MYSQL_HOST = client.get_parameter('MYSQL_HOST',WithDecryption=True)
MYSQL_USER = client.get_parameter('MYSQL_USER',WithDecryption=True)
MYSQL_PASSWORD = client.get_parameter('MYSQL_PASSWORD',WithDecryption=True)
MYSQL_DATABASE = client.get_parameter('MYSQL_DATABASE',WithDecryption=True)

# MySQL connection
mysql_conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

mysql_cursor = mysql_conn.cursor()

# Kafka
invoice_consumer = KafkaConsumer(
    'invoices',
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',  # Start consuming from the earliest offset
    enable_auto_commit=True,       # Automatically commit offsets
    group_id='oaken_shipping_group',  # Specify a consumer group
    value_deserializer=lambda x: loads(x.decode('utf-8')))

invoice_consumer.subscribe(topics='invoices')

shipping_producer = KafkaProducer(
                        bootstrap_servers=[KAFKA_SERVER],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Poll for messages
try:
    for message in invoice_consumer:
        try:
            data = message.value
            invoice = data.get('Invoice', '')

            date_str = data.get('SaleDate','')
            sales_date = datetime.strptime(date_str, '%Y-%m-%d').date()

            sales = data.get('saleDollars','')

            shipping_cost = round(float(sales) * 0.05,2)
            shipping_cost_str = str(shipping_cost)

            random_days = random.randint(0, 4)
            shipping_date = sales_date + timedelta(days=random_days)
            shipping_date_str = str(shipping_date)

            invoice_consumer.commit()
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
            print(f"Error processing message: {e}")

        try:
            # Kafka topic
            shipping_info = {
                'Invoice': invoice,
                'SalesDate': date_str,
                'SaleDollars': sales,
                'ShippingDate': shipping_date_str,
                'ShippingCost': shipping_cost_str
            }

            shipping_producer.send('shipping', value=shipping_info)
        except Exception as e:
            print(f"Error processing message: {e}")
            pass

# Close MySQL connection
finally:
    invoice_consumer.close()
    shipping_producer.flush()
    shipping_producer.close()
    mysql_cursor.close()
    mysql_conn.close()
    sleep(2)
