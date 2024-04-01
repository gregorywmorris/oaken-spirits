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

# Create a consumer instance
consumer = KafkaConsumer(
    'mysql',
    bootstrap_servers=['kafka1:9092'],
    auto_offset_reset='earliest',  # Start consuming from the earliest offset
    enable_auto_commit=True,       # Automatically commit offsets
    group_id='oaken_mysql_group',  # Specify a consumer group
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    connections_max_idle_ms=10000000,
    request_timeout_ms=1000000, api_version_auto_timeout_ms=1000000)

consumer.subscribe(topics=['mysql'])

invoice_producer = KafkaProducer(
                        bootstrap_servers=['kafka1:19092'],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))

print('set up complete')
# Poll for messages
try:
    for message in consumer:
        try:
            data = message.value
            # Customer
            storNumber = int(data.get('StoreNumber', ''))
            if not storNumber:
                print("StoreNumber is null or invalid. Skipping insertion.")
                pass

            storeName = data.get('StoreName', '')
            address = data.get('Address', '')
            city = data.get('City', '')
            county = data.get('County', '')
            state = data.get('State', '')
            zip_code = int(data.get('ZipCode', ''))

            # vendor
            vendorNumber = int(float(data.get('VendorNumber', '')))
            if not vendorNumber:
                print("VendorNumber is null or invalid. Skipping insertion.")
                pass

            vendorName = data.get('VendorName', '')

            # category
            category = int(float(data.get('Category','')))
            if not category:
                print("Category is null or invalid. Skipping insertion.")
                pass

            categoryName = (data.get('CategoryName',''))

            # product
            itemNumber = int(data.get('ItemNumber', ''))
            if not itemNumber:
                print("ItemNumber is null or invalid. Skipping insertion.")
                pass
            itemDescription = data.get('ItemDescription', '')
            pack = int(data.get('Pack', ''))
            volume = int(data.get('BottleVolumeML', ''))
            cost = float(data.get('BottleCost', '').replace('$', ''))
            retail = float(data.get('BottleRetail', '').replace('$', ''))

            # Sales
            invoice = data.get('Invoice', '')
            if not invoice:
                print("Invoice is null or invalid. Skipping insertion.")
                pass

            date_str = data.get('Date', '')
            if not date_str:
                print("Date is null or invalid. Skipping insertion.")
                pass

            sales_date = datetime.strptime(date_str, '%m/%d/%Y').date()

            amountSold = int(data.get('BottlesSold', ''))
            totalLiters = float(data.get('VolumeSoldLiters', ''))

            sales_str = data.get('SaleDollars', '').replace('$', '')
            sales = float(sales_str)

            # MySQL
            '''
            Multiple try/except blocks are used due to the simplistic invoicing
            application script.

            In a real world scenario, likely each of these blocks would be done
            as a truly separate process.

            The try/except prevents the duplicates failing to be added to the
            database from preventing the rest of the processes from competing.
            '''

            print('customer')
            try:
                CUSTOMER_QUERY = '''
                    INSERT INTO customer (StoreNumber,StoreName,Address,City,CountyName,State,ZipCode)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    '''
                customer_data = (storNumber,storeName,address,city,county,state,zip_code)
                mysql_cursor.execute(CUSTOMER_QUERY, customer_data)
                mysql_conn.commit()
            except Exception as e:
                print(f"Error processing message: {e}")
                pass

            print('vendor')
            try:
                VENDOR_QUERY = '''
                    INSERT INTO vendor (VendorNumber,VendorName)
                    VALUES (%s,%s)
                    '''
                vendor_data = (vendorNumber,vendorName)
                mysql_cursor.execute(VENDOR_QUERY,vendor_data)
                mysql_conn.commit()
            except Exception as e:
                print(f"Error processing message: {e}")
                pass

            print(category)
            try:
                CATEGORY_QUERY = '''
                    INSERT INTO category (CategoryNumber,CategoryName)
                    VALUES (%s,%s)
                    '''
                category_data = (category,categoryName)
                mysql_cursor.execute(CATEGORY_QUERY, category_data)
                mysql_conn.commit()
            except Exception as e:
                print(f"Error processing message: {e}")
                pass

            print('product')
            try:
                PRODUCT_QUERY = '''
                    INSERT INTO product (ItemNumber,CategoryNumber,ItemDescription,BottleVolumeML,
                    Pack,BottleCost,BottleRetail)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    '''
                product_data = (itemNumber,category,itemDescription,volume,pack,cost,retail)
                mysql_cursor.execute(PRODUCT_QUERY, product_data)
                mysql_conn.commit()
            except Exception as e:
                print(f"Error processing message: {e}")
                pass

            print(sales)
            try:
                SALES_QUERY = '''
                INSERT INTO sales (Invoice,StoreNumber,VendorNumber,SaleDate,SaleDollars,
                ItemNumber,VolumeSoldLiters,BottlesSold)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                '''
                sales_data = (invoice,storNumber,vendorNumber,sales_date,sales,itemNumber,
                                totalLiters,amountSold)
                mysql_cursor.execute(SALES_QUERY, sales_data)
                mysql_conn.commit()
            except Exception as e:
                print(f"Error processing message: {e}")
                pass

            print('topic')
            # Topic should post after MySQL processing to ensure data is in the database.
            try:
                sales_date_str = str(sales_date)
                INVOICES_info = {
                    "Invoice": invoice,
                    "SaleDate": sales_date_str,
                    "saleDollars": sales_str
                }

                invoice_producer.send('invoices', value=INVOICES_info)
            except Exception as e:
                print(f"Error processing message: {e}")
                pass

        except Exception as e:
            print(f"Error processing message: {e}")
            pass

# Close MySQL connection
finally:
    consumer.close()
    invoice_producer.flush()
    invoice_producer.close()
    mysql_cursor.close()
    mysql_conn.close()
    sleep(3)
