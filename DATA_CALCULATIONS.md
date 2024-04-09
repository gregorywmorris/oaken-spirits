# Data volume calculations

## MySQl Database

These calculations give an estimate of the storage requirements per row for each table. Keep in mind that actual storage may vary due to factors such as row overhead, indexes, and actual data lengths.

### customer table

- StoreNumber (MEDIUMINT): 3 bytes
- StoreName, Address, City, CountyName, State, ZipCode (VARCHAR(255)): - - Each character takes 1 byte, so let's assume the average length of each field is 50 characters (to be conservative). So, 50 bytes for each field.
    - **Total bytes** = 3 + 50 * 6 + 3 = 303 bytes per row

### vendor table

- VendorNumber (MEDIUMINT): 3 bytes
- VendorName (VARCHAR(255)): Assumed average length of 50 characters.
    - **Total bytes** = 3 + 50 = 53 bytes per row

### category table

- CategoryNumber (MEDIUMINT): 3 bytes
- CategoryName (VARCHAR(255)): Assumed average length of 50 characters.
    - **Total bytes** = 3 + 50 = 53 bytes per row

## product table

- ItemNumber, CategoryNumber (MEDIUMINT): 3 bytes each
- ItemDescription (VARCHAR(255)): Assumed average length of 50 characters.
- BottleVolumeML, Pack (INT, MEDIUMINT): 4 bytes, 3 bytes
- BottleCost, BottleRetail (DECIMAL(11,2)): 8 bytes each
    - **Total bytes** = 3 + 3 + 50 + 4 + 3 + 8 + 8 = 79 bytes per row

### sales table

- Invoice (VARCHAR(255)): Assumed average length of 50 characters.
- StoreNumber, VendorNumber, ItemNumber (MEDIUMINT): 3 bytes each
- SaleDate, ShippingDate (DATE): 3 bytes each
- SaleDollars, VolumeSoldLiters (DECIMAL(11,2)): 8 bytes each
- BottlesSold (MEDIUMINT): 3 bytes
- ShippingCost (DECIMAL(11,2)): 8 bytes
    - **Total bytes** = 50 + 3 + 3 + 3 + 3 + 8 + 8 + 3 + 8 = 89 bytes per row

### salesLedger table

- Invoice (VARCHAR(255)): Assumed average length of 50 characters.
- Credit, Debit (DECIMAL(11,2)): 8 bytes each
- Note (VARCHAR(255)): Assumed average length of 50 characters.
    - **Total bytes** = 50 + 8 + 8 + 50 = 116 bytes per row

### Totals and estimates

#### Totals by table and row

- customer: 303 bytes per row
- vendor: 53 bytes per row
- category: 53 bytes per row
- product: 79 bytes per row
- sales: 89 bytes per row
- salesLedger: 116 bytes per row
    - **Total per row** = 693 bytes

#### Estimates

- customer: Assuming 10,000 rows -> 303 bytes/row * 10,000 rows = 3,030,000 bytes
- vendor: Assuming 1,000 rows -> 53 bytes/row * 1,000 rows = 53,000 bytes
- category: Assuming 100 rows -> 53 bytes/row * 100 rows = 5,300 bytes
- product: Assuming 5,000 rows -> 79 bytes/row * 5,000 rows = 395,000 bytes
- sales: Assuming 50,000 rows -> 89 bytes/row * 50,000 rows = 4,450,000 bytes
- salesLedger: Assuming 100,000 rows -> 116 bytes/row * 100,000 rows = 11,600,000 bytes
    - **Total storage** = 19,533,300 bytes
