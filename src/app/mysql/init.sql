USE oaken;

CREATE TABLE customer (
    StoreNumber MEDIUMINT NOT NULL,
    StoreName VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    CountyName VARCHAR(255) NOT NULL,
    State VARCHAR(255) NOT NULL,
    ZipCode TINYINT NOT NULL,
    PRIMARY KEY (StoreNumber)
);

CREATE TABLE vendor (
    VendorNumber MEDIUMINT NOT NULL,
    VendorName VARCHAR(255) NOT NULL,
    PRIMARY KEY (VendorNumber)
);

CREATE TABLE category (
    CategoryNumber MEDIUMINT NOT NULL,
    CategoryName VARCHAR(255) NOT NULL,
    PRIMARY KEY (CategoryNumber)
);

CREATE TABLE product (
    ItemNumber MEDIUMINT NOT NULL,
    CategoryNumber MEDIUMINT,
    ItemDescription VARCHAR(255) NOT NULL,
    BottleVolumeML INT NOT NULL,
    Pack MEDIUMINT NOT NULL,
    BottleCost DECIMAL(11,2) NOT NULL,
    BottleRetail DECIMAL(11,2) NOT NULL,
    PRIMARY KEY (ItemNumber),
    FOREIGN KEY (CategoryNumber) REFERENCES category(CategoryNumber)
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
    FOREIGN KEY (StoreNumber) REFERENCES customer(StoreNumber),
    FOREIGN KEY (ItemNumber) REFERENCES product(ItemNumber),
    FOREIGN KEY (VendorNumber) REFERENCES vendor(VendorNumber)
);

CREATE TABLE salesLedger (
    ID MEDIUMINT NOT NULL AUTO_INCREMENT,
    Invoice VARCHAR(255) NOT NULL,
    Credit DECIMAL(11,2),
    Debit DECIMAL(11,2),
    Note VARCHAR(255),
    PRIMARY KEY (ID),
    FOREIGN KEY (Invoice) REFERENCES sales(Invoice)
);
