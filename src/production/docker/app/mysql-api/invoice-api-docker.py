import sys
sys.path.append('..')

import os
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import psycopg2


# PostgreSQL connection
postgres_conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    database=os.getenv('DATABASE')
)

postgres_cursor = postgres_conn.cursor()

# Create a consumer instance

# Get variable or use default values
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka1:9092,kafka2:9093,kafka3:9094')

# Kafka consumer
consumer = KafkaConsumer(
    'mysql',
    bootstrap_servers=bootstrap_servers.split(','),  # Convert string to list
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='oaken_mysql_group',
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    connections_max_idle_ms=10000000,
    request_timeout_ms=1000000,
    api_version_auto_timeout_ms=1000000
)

consumer.subscribe(topics=['mysql'])

schema_name=os.getenv('DATABASE')

# Kafka producer
invoice_producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers.split(','),  # Convert string to list
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)
logging.warning('set up complete')

# Poll for messages
try:
    for message in consumer:
        try:
            data = message.value
            # Customer
            storNumber = int(data.get('StoreNumber', ''))
            if not storNumber:
                logging.warning("StoreNumber is null or invalid. Skipping insertion.")

            storeName = data.get('StoreName', '')
            address = data.get('Address', '')
            city = data.get('City', '')
            county = data.get('County', '')
            state = data.get('State', '')
            zip_code = int(data.get('ZipCode', ''))

            # vendor
            vendorNumber = int(float(data.get('VendorNumber', '')))
            if not vendorNumber:
                logging.warning("VendorNumber is null or invalid. Skipping insertion.")

            vendorName = data.get('VendorName', '')

            # category
            category = int(float(data.get('Category','')))
            if not category:
                logging.warning("Category is null or invalid. Skipping insertion.")

            categoryName = (data.get('CategoryName',''))

            # product
            itemNumber = int(data.get('ItemNumber', ''))
            if not itemNumber:
                logging.warning("ItemNumber is null or invalid. Skipping insertion.")
            itemDescription = data.get('ItemDescription', '')
            pack = int(data.get('Pack', ''))
            volume = int(data.get('BottleVolumeML', ''))
            cost = float(data.get('BottleCost', '').replace('$', ''))
            retail = float(data.get('BottleRetail', '').replace('$', ''))

            # Sales
            invoice = data.get('Invoice', '')
            if not invoice:
                logging.warning("Invoice is null or invalid. Skipping insertion.")

            date_str = data.get('Date', '')
            if not date_str:
                logging.warning("Date is null or invalid. Skipping insertion.")

            amountSold = int(data.get('BottlesSold', ''))
            totalLiters = float(data.get('VolumeSoldLiters', ''))

            sales_str = data.get('SaleDollars', '').replace('$', '')
            sales = float(sales_str)

            employee = data.get('EmployeeID', '')
            if not employee:
                logging.warning("EmployeeID is null or invalid. Skipping insertion.")
        except ValueError as ve:
            logging.warning("Error processing message: %s", ve)
        except Exception as e:
            logging.warning("An unexpected error occurred: %s", e)

        # PostgreSQL
        try:
            CUSTOMER_QUERY = '''
                INSERT INTO {schema_name}.customers (store_id,store_name,street_address,city,county,us_state,zip_code)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                '''
            customer_data = (storNumber,storeName,address,city,county,state,zip_code)
            postgres_cursor.execute(CUSTOMER_QUERY.format(schema_name=schema_name), customer_data)
        except Exception as e:
            logging.warning("Error processing message: %s", e)
            postgres_conn.rollback()

        postgres_conn.commit()

        try:
            VENDOR_QUERY = '''
                INSERT INTO {schema_name}.vendors (vendor_id,vendor_name)
                VALUES (%s,%s)
                '''
            vendor_data = (vendorNumber,vendorName)
            postgres_cursor.execute(VENDOR_QUERY.format(schema_name=schema_name),vendor_data)
        except Exception as e:
            logging.warning("Error processing message: %s", e)
            postgres_conn.rollback()

        postgres_conn.commit()

        try:
            CATEGORY_QUERY = '''
                INSERT INTO {schema_name}.categories (category_id,category_name)
                VALUES (%s,%s)
                '''
            category_data = (category,categoryName)
            postgres_cursor.execute(CATEGORY_QUERY.format(schema_name=schema_name), category_data)
        except Exception as e:
            logging.warning("Error processing message: %s", e)
            postgres_conn.rollback()

        postgres_conn.commit()

        try:
            PRODUCT_QUERY = '''
                INSERT INTO {schema_name}.products (item_id,category_id,item_description,bottle_volume_ML,
                pack,bottle_cost,bottle_retail)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                '''
            product_data = (itemNumber,category,itemDescription,volume,pack,cost,retail)
            postgres_cursor.execute(PRODUCT_QUERY.format(schema_name=schema_name), product_data)
        except Exception as e:
            logging.warning("Error processing message: %s", e)
            postgres_conn.rollback()

        postgres_conn.commit()

        try:
            SALES_QUERY = '''
            INSERT INTO {schema_name}.sales (invoice,store_id,vendor_id,employee_id,sale_date,sale_amount_dollar,
            item_id,volume_liter,bottle_count)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            sales_data = (invoice,storNumber,vendorNumber,employee,date_str,sales,itemNumber,
                            totalLiters,amountSold)
            postgres_cursor.execute(SALES_QUERY.format(schema_name=schema_name), sales_data)
        except Exception as e:
            logging.warning("Error processing message: %s", e)
            postgres_conn.rollback()

        postgres_conn.commit()

        # Topic should post after PostgreSQL processing to ensure data is in the database.
        try:
            INVOICES_info = {
                "Invoice": invoice,
                "SaleDate": date_str,
                "saleDollars": sales_str
            }

            invoice_producer.send('invoices', value=INVOICES_info)
        except Exception as e:
            logging.warning("Error processing message: %s", e)
except Exception as e:
    logging.warning("Error processing message: %s", e)

finally:
    consumer.close()
    invoice_producer.flush()
    invoice_producer.close()
    postgres_cursor.close()
    postgres_conn.close()
