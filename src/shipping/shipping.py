import sys
sys.path.append('..')

import json
from variables import KAFKA_SERVER, INVOICES_TOPIC, SHIPPING_TOPIC, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import random
import datetime
import mysql.connector

#Kafka
consumer = KafkaConsumer(
    INVOICES_TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    value_deserializer=lambda x: loads(x.decode('utf-8')))

producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

for message in consumer:
    data = message.value
    date = data.get('Date', '')
    sales = data.get('Sale (Dollars)', '')
    invoice = data.get('Invoice/Item Number', '')

    sales_amount = float(sales.replace('$', ''))

    shipping_cost = sales_amount * 0.05

    invoice_date = datetime.datetime.strptime(date, '%m/%d/%Y')
    # Made random to add variance
    shipping_date = invoice_date + datetime.timedelta(days=random.randint(1, 4)) 

    shipping_info = {
        'Invoice/Item Number': invoice,
        'Shipping Date': shipping_date.strftime('%m/%d/%Y'),
        'Shipping Cost': shipping_cost
    }

    producer.send(SHIPPING_TOPIC, value=shipping_info)
    producer.flush()

    # Update MySQL table with shipping information
    update_query = """
        UPDATE your_table_name
        SET ShippingDate = %s, ShippingCost = %s 
        WHERE InvoiceItemNumber = %s
    """
    update_data = (shipping_date.strftime('%Y-%m-%d'), shipping_cost, invoice)
    mysql_cursor.execute(update_query, update_data)
    mysql_conn.commit()
