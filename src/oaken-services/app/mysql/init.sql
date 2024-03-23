CREATE DATABASE IF NOT EXISTS oaken;
USE oaken;

DROP TABLE IF EXISTS salesLedger;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS vendor;
DROP TABLE IF EXISTS category;

CREATE TABLE customer (
    StoreNumber INT NOT NULL,
    StoreName VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    CountyName VARCHAR(255) NOT NULL,
    State VARCHAR(255) NOT NULL,
    ZipCode INT NOT NULL,
    PRIMARY KEY (StoreNumber),
);

CREATE TABLE vendor (
    VendorNumber INT NOT NULL,
    VendorName VARCHAR(255) NOT NULL,
    PRIMARY KEY (VendorNumber)
);

CREATE TABLE category (
    CategoryNumber INT NOT NULL,
    CategoryName VARCHAR(255) NOT NULL,
    PRIMARY KEY (CategoryNumber)
);

CREATE TABLE product (
    ItemNumber INT NOT NULL,
    CategoryNumber INT,
    ItemDescription VARCHAR(255) NOT NULL,
    BottleVolumeML INT NOT NULL,
    Pack INT NOT NULL,
    BottleCost INT NOT NULL,
    BottleRetail INT NOT NULL,
    PRIMARY KEY (ItemNumber),
    FOREIGN KEY (CategoryNumber) REFERENCES category(CategoryNumber)
);

CREATE TABLE sales (
    Invoice VARCHAR(255) NOT NULL,
    StoreNumber INT NOT NULL,
    VendorNumber INT NOT NULL,
    SaleDate DATETIME NOT NULL,
    SaleDollars FLOAT NOT NULL,
    ItemNumber INT NOT NULL,
    BottlesSold INT NOT NULL,
    VolumeSoldLiters FLOAT NOT NULL,
    ShippingDate DATETIME,
    ShippingCost FLOAT,
    PRIMARY KEY (Invoice),
    FOREIGN KEY (StoreNumber) REFERENCES customer(StoreNumber),
    FOREIGN KEY (ItemNumber) REFERENCES product(ItemNumber),
    FOREIGN KEY (VendorNumber) REFERENCES vendor(VendorNumber)
);

CREATE TABLE salesLedger (
    Invoice VARCHAR(255) NOT NULL,
    Credit INT,
    Debit INT,
    Note VARCHAR(255),
    PRIMARY KEY (Invoice),
    FOREIGN KEY (Invoice) REFERENCES sales(Invoice)
);
