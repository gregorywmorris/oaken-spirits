import sys
sys.path.append('..')

import os
import sys
import json
import logging
from kafka import KafkaConsumer
from json import loads
import psycopg2
from logging.handlers import RotatingFileHandler

# PostgreSQL connection
postgres_conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    database=os.getenv('DATABASE')
)

postgres_cursor = postgres_conn.cursor()

schema_name=os.getenv('DATABASE')

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
for shipping_message in shipping_consumer:
    try:
        shipping_data = shipping_message.value

        invoice = shipping_data.get('Invoice', '')

        shipping_expense = float(shipping_data.get('ShippingCost')) * -1

        sales = float(shipping_data.get('SaleDollars'))
    except ValueError as ve:
        logging.warning("Error processing message: %s", ve)
        continue
    except Exception as e:
        logging.warning("An unexpected error occurred: %s", e)
        continue
    # PostgreSQL
    try:
        LEDGER_CREDIT = """
            INSERT INTO {schema_name}.salesLedger (invoice, credit, note)
            VALUES (%s, %s, 'Sale')
            ON CONFLICT (invoice) DO UPDATE SET credit = %s
        """
        credit_data = (invoice, sales)
        postgres_cursor.execute(LEDGER_CREDIT.format(schema_name=schema_name), credit_data)
        postgres_conn.commit()
    except Exception as e:
        logging.warning("Error processing message: %s", e)
        continue

    try:
        LEDGER_DEBIT = """
            INSERT INTO {schema_name}.salesLedger (invoice, debit, note)
            VALUES (%s, %s, 'Shipping')
            ON CONFLICT (invoice) DO UPDATE SET debit = %s
        """
        debit_data = (invoice, shipping_expense)
        postgres_cursor.execute(LEDGER_DEBIT.format(schema_name=schema_name), debit_data)
        postgres_conn.commit()
    except Exception as e:
        logging.warning("Error processing message: %s", e)
        continue


shipping_consumer.close()
postgres_cursor.close()
postgres_conn.close()
