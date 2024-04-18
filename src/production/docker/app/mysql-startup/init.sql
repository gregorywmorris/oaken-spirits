USE oaken;

CREATE TABLE customers (
    StoreNumber MEDIUMINT NOT NULL,
    StoreName VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    CountyName VARCHAR(255) NOT NULL,
    State VARCHAR(255) NOT NULL,
    ZipCode MEDIUMINT NOT NULL,
    PRIMARY KEY (StoreNumber)
);

CREATE TABLE vendors (
    VendorNumber MEDIUMINT NOT NULL,
    VendorName VARCHAR(255) NOT NULL,
    PRIMARY KEY (VendorNumber)
);

CREATE TABLE categories (
    CategoryNumber MEDIUMINT NOT NULL,
    CategoryName VARCHAR(255) NOT NULL,
    PRIMARY KEY (CategoryNumber)
);

CREATE TABLE products (
    ItemNumber MEDIUMINT NOT NULL,
    CategoryNumber MEDIUMINT,
    ItemDescription VARCHAR(255) NOT NULL,
    BottleVolumeML INT NOT NULL,
    Pack MEDIUMINT NOT NULL,
    BottleCost DECIMAL(11,2) NOT NULL,
    BottleRetail DECIMAL(11,2) NOT NULL,
    PRIMARY KEY (ItemNumber),
    FOREIGN KEY (CategoryNumber) REFERENCES categories(CategoryNumber)
);

CREATE TABLE sales (
    Invoice VARCHAR(255) NOT NULL,
    StoreNumber MEDIUMINT NOT NULL,
    VendorNumber MEDIUMINT NOT NULL,
    SaleDate DATE NOT NULL,
    SaleDollars DECIMAL(11,2) NOT NULL,
    ItemNumber MEDIUMINT NOT NULL,
    BottlesSold MEDIUMINT NOT NULL,
    VolumeSoldLiters DECIMAL(11,2)  NOT NULL,
    ShippingDate DATE,
    ShippingCost DECIMAL(11,2),
    PRIMARY KEY (Invoice),
    FOREIGN KEY (StoreNumber) REFERENCES customers(StoreNumber),
    FOREIGN KEY (ItemNumber) REFERENCES products(ItemNumber),
    FOREIGN KEY (VendorNumber) REFERENCES vendors(VendorNumber)
);

CREATE TABLE salesLedger (
    Invoice VARCHAR(255) NOT NULL,
    Credit DECIMAL(11,2),
    Debit DECIMAL(11,2),
    Note VARCHAR(255),
    PRIMARY KEY (Invoice, Note),
    FOREIGN KEY (Invoice) REFERENCES sales(Invoice)
);

CREATE USER 'airbyte'@'%' IDENTIFIED BY 'airbyte';
GRANT RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'airbyte'@'%';
GRANT ALL PRIVILEGES ON oaken.* TO 'airbyte'@'%';
FLUSH PRIVILEGES;