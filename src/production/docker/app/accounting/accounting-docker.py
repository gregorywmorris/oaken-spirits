import sys
sys.path.append('..')

import sys
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


# MySQL connection
mysql_conn = mysql.connector.connect(
    host='oaken-mysql',
    user='mysql',
    password='mysql',
    database='oaken'
)

mysql_cursor = mysql_conn.cursor()

# Kafka consumers
shipping_consumer = KafkaConsumer(
    'shipping',
    bootstrap_servers=['kafka1:9092','kafka2:9093','kafka3:9094'],
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