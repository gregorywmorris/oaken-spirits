import sys
sys.path.append('..')

import os
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import random
from datetime import datetime, timedelta
import psycopg2


# PostgreSQL connection
postgres_conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    database=os.getenv('DATABASE')
)

postgres_cursor = postgres_conn.cursor()

schema_name=os.getenv('DATABASE')

# Kafka
invoice_consumer = KafkaConsumer(
    'invoices',
    bootstrap_servers=['kafka1:9092','kafka2:9093','kafka3:9094'],
    auto_offset_reset='earliest',  # Start consuming from the earliest offset
    enable_auto_commit=True,       # Automatically commit offsets
    group_id='oaken_shipping_group',  # Specify a consumer group
    value_deserializer=lambda x: loads(x.decode('utf-8')))

invoice_consumer.subscribe(topics='invoices')

shipping_producer = KafkaProducer(
                        bootstrap_servers=['kafka1:9092','kafka2:9093','kafka3:9094'],
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

            def shipping_cost(kwarg):
                """Determines shipping costs"""
                cost = round(float(kwarg) * 0.05, 2)
                if cost < 5:
                    return "5.00"
                else:
                    return str(cost)

            shipping_cost_str = shipping_cost(sales)

            random_days = random.randint(0, 4)
            shipping_date = sales_date + timedelta(days=random_days)
            shipping_date_str = str(shipping_date)

            invoice_consumer.commit()
        except ValueError as ve:
            logging.warning("Error processing message: %s", ve)
        except Exception as e:
            logging.warning("An unexpected error occurred: %s", e)
        try:
            # PostgreSQL
            UPDATE_QUERY = """
                UPDATE {schema_name}.sales
                SET shipping_date = %s, shipping_cost = %s
                WHERE Invoice = %s
            """

            update_data = (shipping_date, shipping_cost_str, invoice)
            postgres_cursor.execute(UPDATE_QUERY.format(schema_name=schema_name), update_data)

            postgres_conn.commit()

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
            logging.warning("Error processing message: %s", e)
except Exception as e:
    logging.warning("Error processing message: %s", e)

finally:
    invoice_consumer.close()
    shipping_producer.flush()
    shipping_producer.close()
    postgres_cursor.close()
    postgres_conn.close()
