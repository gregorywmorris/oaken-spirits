CREATE DATABASE IF NOT EXISTS oaken;
USE oaken;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS vendor;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS ledger;
DROP TABLE IF EXISTS county;

CREATE TABLE county (
    CountyNumber int not null,
    County varchar(255) not null,
    PRIMARY KEY(county)
);

CREATE TABLE customer (
    StoreNumber  int not null,
    StoreName varchar(255) not null,
    Address varchar(255) not null,
    City varchar(255) not null,
    State varchar(255) not null,
    CountyNumber int not null
    ZipCode int not null,
    PRIMARY KEY(StoreNumber),
    FOREIGN KEY (CountyNumber) REFERENCES county(cCountyNumber)
);

CREATE TABLE vendor (
    VendorNumber int not null,
    VendorName varchar(255) not null,
    PRIMARY KEY(StoreNumber)
);

CREATE TABLE category (
    Category int not null,
    CategoryName varchar(255) not null,
    PRIMARY KEY(Category)
);

CREATE TABLE product (
    ItemNumber int not null,
    Category int not null,
    ItemDescription varchar(255) not null,
    BottleVolume(ml)  int not null,
    Pack  int not null,
    BottleCost int not null,
    BottleRetail int not null,
    PRIMARY KEY(ItemNumber),
    FOREIGN KEY (Category) REFERENCES category(Category)
);

CREATE TABLE sales (
    Invoice varchar(255) not null,
    StoreNumber  int not null,
    VendorNumber int not null,
    SalesDate datetime not null,
    Sale(Dollars) float64 not null,
    ItemNumber int not null,
    BottlesSold int not null,
    VolumeSold(Liters) float64 not null,
    ShippingDate datetime,
    ShippingCost float64,
    PRIMARY KEY(invoice),
    FOREIGN KEY (StoreNumber) REFERENCES customer(StoreNumber),
    FOREIGN KEY (ItemNumber) REFERENCES product(ItemNumber),
    FOREIGN KEY (VendorNumber) REFERENCES vendor(VendorNumber)
);

CREATE TABLE salesLedger (
    Invoice varchar(255) not null,
    Credit int,
    Debit int,
    Note varchar(255),
    FOREIGN KEY (Invoice) REFERENCES sales(Invoice),
    PRIMARY KEY(Invoice)
);