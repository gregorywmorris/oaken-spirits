#!/usr/bin/env python3
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

# Kafka consumers
shipping_consumer = KafkaConsumer(
    'shipping',
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',  # Start consuming from the earliest offset
    enable_auto_commit=True,       # Automatically commit offsets
    group_id='oaken_accounting_group',  # Specify a consumer group
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    connections_max_idle_ms=10000000,
    request_timeout_ms=1000000, api_version_auto_timeout_ms=1000000)

shipping_consumer.subscribe(topics='shipping')

# Poll for messages
try:
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
                print(f"Error processing message: {e}")
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
                print(f"Error processing message: {e}")
                pass

        except Exception as e:
            print(f"Error processing message: {e}")
            pass

# Close MySQL connection
finally:
    shipping_consumer.close()
    mysql_cursor.close()
    mysql_conn.close()
    sleep(1)