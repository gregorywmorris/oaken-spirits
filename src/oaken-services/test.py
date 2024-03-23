mysql_conn = mysql.connector.connect(
    host='localhost',
    user='mysql',
    password='mysql',
    database='oaken'
)
mysql_cursor = mysql_conn.cursor()

# Create a consumer instance
consumer = KafkaConsumer(
    'mysql',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start consuming from the earliest offset
    enable_auto_commit=True,       # Automatically commit offsets
    group_id='my_consumer_group',  # Specify a consumer group
    value_deserializer=lambda x: loads(x.decode('utf-8')))

consumer.subscribe(topics=['mysql'])

# Poll for messages
try:
    for message in consumer:
        try:
            data = message.value
            # Customer
            storNumber = data.get('StoreNumber','')
            if storNumber is None:
                logger.error("StoreNumber is null. Skipping insertion.")
                continue
            storeName = data.get('StoreName','')
            address = data.get('Address','')
            city = data.get('City','')
            countyNumber = data.get('CountyNumber','')
            county = data.get('County','')
            state = data.get('State','')
            zip = data.get('ZipCode','')
            # Vendor
            vendorNumber = data.get('VendorNumber','')
            if vendorNumber is None:
                logger.error("VendorNumber is null. Skipping insertion.")
                continue
            vendorName = data.get('VendorName','')
            # Product
            itemNumber = data.get('ItemNumber','')
            if itemNumber is None:
                logger.error("ItemNumber is null. Skipping insertion.")
                continue
            category = data.get('CategoryNumber','')
            categoryName = ('CategoryName','')
            itemDescription = data.get('ItemDescription','')
            pack = data.get('Pack','')
            volume = data.get('BottleVolumeML','')
            cost = data.get('BottleCost','')
            retail = data.get('BottleRetail','')
            # Sales
            invoice = data.get('Invoice', '')
            if invoice is None:
                logger.error("Invoice is null. Skipping insertion.")
                continue
            date = data.get('Date', '')
            amountSold = data.get('BottlesSold','')
            totalLiters = data.get('VolumeSoldLiters','')
            sales = data.get('SaleDollars','')
            sales_amount = float(sales.replace('$', ''))

            invoice_date = datetime.datetime.strptime(date, '%m/%d/%Y')
            MYSQL_date = invoice_date + datetime.timedelta(days=random.randint(1, 4))

            # MySQL
            '''
            Multiple try/except blocks are used due to the simplistic invoicing
            application script.

            In a real world scenario, likely each of these blocks would be done
            as a truly separate process.

            The try/except prevents the duplicates failing to be added to the
            database from preventing the rest of the processes from competing.
            '''

            try:
                COUNTY_QUERY = '''
                    INSERT INTO county (CountyNumber,CountyName)
                    VALUES (%s,%s)
                    '''
                county_data = (countyNumber,county)
                mysql_cursor.execute(COUNTY_QUERY, county_data)
                mysql_conn.commit()
            except Exception as e:
                print(f"Error processing message: {e}")
                continue

            try:
                CUSTOMER_QUERY = '''
                    INSERT INTO customer (StoreNumber,StoreName,Address,City,CountyNumber,State,ZipCode)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    '''
                customer_data = (storNumber,storeName,address,city,countyNumber,state,zip)
                mysql_cursor.execute(CUSTOMER_QUERY, customer_data)
                mysql_conn.commit()
            except Exception as e:
                print(f"Error processing message: {e}")
                continue

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
                continue

        # Handle KeyboardInterrupt to gracefully close the consumer
        except KeyboardInterrupt:
            print("Consumer terminated by user")

# Close the consumer
finally:
    consumer.close()