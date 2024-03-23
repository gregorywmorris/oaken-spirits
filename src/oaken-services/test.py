try:
    data = message.value
    # Customer
    storNumber = int(data.get('StoreNumber',''))
    if storNumber is None or 0:
        print("StoreNumber is null or invalid. Skipping insertion.")
        continue
    storeName = data.get('StoreName','')
    address = data.get('Address','')
    city = data.get('City','')
    countyNumber = data.get('CountyNumber','') # no longer in use
    county = data.get('County','')
    state = data.get('State','')
    zip_code = int(data.get('ZipCode',''))
    # Vendor
    vendorNumber = int(data.get('VendorNumber',''))
    if vendorNumber is None or 0:
        print("VendorNumber is null or invalid. Skipping insertion.")
        continue
    vendorName = data.get('VendorName','')
    # Product
    itemNumber = int(data.get('ItemNumber',''))
    if itemNumber is None:
        print("ItemNumber is null or invalid. Skipping insertion.")
        continue
    category = int(data.get('Category',''))
    categoryName = ('CategoryName','')
    itemDescription = data.get('ItemDescription','')
    pack = int(data.get('Pack',''))
    volume = int(data.get('BottleVolumeML',''))
    cost = float(data.get('BottleCost','').replace('$', ''))
    retail = float(data.get('BottleRetail','').replace('$', ''))
    # Sales
    invoice = data.get('Invoice', '')
    if invoice is None or 0:
        print("Invoice is null or invalid. Skipping insertion.")
        continue
    date_string = data.get('Date', '')
    sales_date = datetime.strptime(date_string,'%m/%d/%Y').date()
    amountSold = int(data.get('BottlesSold',''))
    totalLiters = float(data.get('VolumeSoldLiters',''))
    sales = float(data.get('SaleDollars','').replace('$', ''))

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
        CUSTOMER_QUERY = '''
            INSERT INTO customer (StoreNumber,StoreName,Address,City,County,State,ZipCode)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            '''
        customer_data = (storNumber,storeName,address,city,county,state,zip_code)
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
        continue

    try:
        PRODUCT_QUERY = '''
            INSERT INTO product (ItemNumber,CategoryNumber,ItemDescription,BottleVolumeML,
            Pack,BottleCost,BottleRetail)
            VALUES (%s,%s,%s,%s,%s,%s,%s,)
            '''
        product_data = (itemNumber,category,itemDescription,volume,pack,cost,retail)
        mysql_cursor.execute(PRODUCT_QUERY, product_data)
        mysql_conn.commit()
    except Exception as e:
        print(f"Error processing message: {e}")
        continue

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

        # Topic should post after MySQL processing to ensure data is in the database.
        INVOICES_info = {
            'Invoice': invoice,
            'SaleDate': sales_date,
            'saleDollars': sales
        }

        invoice_producer.send(INVOICES_TOPIC, value=INVOICES_info)
        invoice_producer.flush()
    except Exception as e:
        print(f"Error processing message: {e}", exc_info=True)
        continue

except Exception as e:
print(f"Error in Kafka consumer: {e}", exc_info=True)
continue