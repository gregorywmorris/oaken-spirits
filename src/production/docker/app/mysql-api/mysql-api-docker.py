import sys
sys.path.append('..')

import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from json import loads
from datetime import datetime
import psycopg2


# PostgreSQL connection
postgres_conn = psycopg2.connect(
    host='oaken-postgres',
    user='postgres',
    password='postgres',
    database='oaken'
)

postgres_cursor = postgres_conn.cursor()

# Create a consumer instance
consumer = KafkaConsumer(
    'mysql',
    bootstrap_servers=['kafka1:9092','kafka2:9093','kafka3:9094'],
    auto_offset_reset='earliest',  # Start consuming from the earliest offset
    enable_auto_commit=True,       # Automatically commit offsets
    group_id='oaken_mysql_group',  # Specify a consumer group
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    connections_max_idle_ms=10000000,
    request_timeout_ms=1000000, api_version_auto_timeout_ms=1000000)

consumer.subscribe(topics=['mysql'])

invoice_producer = KafkaProducer(
                        bootstrap_servers=['kafka1:9092','kafka2:9093','kafka3:9094'],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))

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

            # PostgreSQL
            try:
                CUSTOMER_QUERY = '''
                    INSERT INTO customers (store_id,store_name,street_address,city,county,us_state,zip_code)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    '''
                customer_data = (storNumber,storeName,address,city,county,state,zip_code)
                postgres_cursor.execute(CUSTOMER_QUERY, customer_data)
                postgres_conn.commit()
            except Exception as e:
                logging.warning("Error processing message: %s", e)

            try:
                VENDOR_QUERY = '''
                    INSERT INTO vendors (vendor_id,vendor_name)
                    VALUES (%s,%s)
                    '''
                vendor_data = (vendorNumber,vendorName)
                postgres_cursor.execute(VENDOR_QUERY,vendor_data)
                postgres_conn.commit()
            except Exception as e:
                logging.warning("Error processing message: %s", e)

            try:
                CATEGORY_QUERY = '''
                    INSERT INTO categories (category_id,category_name)
                    VALUES (%s,%s)
                    '''
                category_data = (category,categoryName)
                postgres_cursor.execute(CATEGORY_QUERY, category_data)
                postgres_conn.commit()
            except Exception as e:
                logging.warning("Error processing message: %s", e)

            try:
                PRODUCT_QUERY = '''
                    INSERT INTO products (item_id,category_id,item_description,bottle_volume_ML,
                    pack,bottle_cost,bottle_retail)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    '''
                product_data = (itemNumber,category,itemDescription,volume,pack,cost,retail)
                postgres_cursor.execute(PRODUCT_QUERY, product_data)
                postgres_conn.commit()
            except Exception as e:
                logging.warning("Error processing message: %s", e)

            try:
                SALES_QUERY = '''
                INSERT INTO sales (invoice,store_id,vendor_id,employee_id,sale_date,sale_amount,
                item_id,volume_sold_liters,bottles_sold)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                '''
                sales_data = (invoice,storNumber,vendorNumber,employee,date_str,sales,itemNumber,
                                totalLiters,amountSold)
                postgres_cursor.execute(SALES_QUERY, sales_data)
                postgres_conn.commit()
            except Exception as e:
                logging.warning("Error processing message: %s", e)

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
