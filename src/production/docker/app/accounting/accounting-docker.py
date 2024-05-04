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

schema_name = os.getenv('DATABASE')

# Kafka consumers
shipping_consumer = KafkaConsumer(
    'shipping',
    bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'],
    auto_offset_reset='earliest',  # Start consuming from the earliest offset
    enable_auto_commit=True,        # Automatically commit offsets
    group_id='oaken_accounting_group',  # Specify a consumer group
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    connections_max_idle_ms=10000000,
    request_timeout_ms=1000000,
    api_version_auto_timeout_ms=1000000
)

shipping_consumer.subscribe(topics='shipping')

# Poll for messages
try:
    for shipping_message in shipping_consumer:
        try:
            shipping_data = shipping_message.value

            invoice = shipping_data.get('Invoice')

            shipping_expense = float(shipping_data.get('ShippingCost', '0'))

            sales = float(shipping_data.get('SaleDollars', '0'))

            # PostgreSQL - Insert with note
            try:
                LEDGER_ENTRY = """
                    INSERT INTO {schema_name}.sales_ledger (invoice, credit, debit, note)
                    VALUES (%s, %s, %s, %s)
                """.format(schema_name=schema_name)

                NOTE = 'Sale and shipping'
                ledger_data = (invoice, sales,shipping_expense,NOTE)
                postgres_cursor.execute(LEDGER_ENTRY, ledger_data)
                postgres_conn.commit()

            except Exception as e:
                logging.warning("Error processing message: %s", e)

        except ValueError as ve:
            logging.warning("Error processing message: %s", ve)
        except Exception as e:
            logging.warning("An unexpected error occurred: %s", e)

except Exception as e:
    logging.warning("Error processing message: %s", e)

finally:
    shipping_consumer.close()
    postgres_cursor.close()
    postgres_conn.close()
