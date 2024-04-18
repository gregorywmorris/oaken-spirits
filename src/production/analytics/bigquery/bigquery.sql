CREATE TABLE oaken_spirits.customers (
    StoreNumber NUMERIC NOT NULL,
    StoreName STRING NOT NULL,
    Address STRING NOT NULL,
    City STRING NOT NULL,
    CountyName STRING NOT NULL,
    State STRING NOT NULL,
    ZipCode NUMERIC NOT NULL
);

CREATE TABLE oaken_spirits.vendors (
    VendorNumber NUMERIC NOT NULL,
    VendorName STRING NOT NULL
);

CREATE TABLE oaken_spirits.categories (
    CategoryNumber NUMERIC NOT NULL,
    CategoryName STRING NOT NULL
);

CREATE TABLE oaken_spirits.products (
    ItemNumber NUMERIC NOT NULL,
    CategoryNumber NUMERIC,
    ItemDescription STRING NOT NULL,
    BottleVolumeML NUMERIC NOT NULL,
    Pack NUMERIC NOT NULL,
    BottleCost FLOAT64 NOT NULL,
    BottleRetail FLOAT64 NOT NULL
);

CREATE TABLE oaken_spirits.sales (
    Invoice STRING NOT NULL,
    StoreNumber NUMERIC NOT NULL,
    VendorNumber NUMERIC NOT NULL,
    SaleDate DATE NOT NULL,
    SaleDollars FLOAT64 NOT NULL,
    ItemNumber NUMERIC NOT NULL,
    BottlesSold NUMERIC NOT NULL,
    VolumeSoldLiters FLOAT64 NOT NULL,
    ShippingDate DATE,
    ShippingCost FLOAT64
);

CREATE TABLE oaken_spirits.salesLedger (
    Invoice STRING NOT NULL,
    Credit FLOAT64,
    Debit FLOAT64,
    Note STRING
);

-- -- Create unique indexes for primary key enforcement
-- CREATE UNIQUE INDEX idx_customers_storenumber ON oaken_spirits.customers(StoreNumber);
-- CREATE UNIQUE INDEX idx_vendors_vendornumber ON oaken_spirits.vendors(VendorNumber);
-- CREATE UNIQUE INDEX idx_categories_categorynumber ON oaken_spirits.categories(CategoryNumber);
-- CREATE UNIQUE INDEX idx_products_itemnumber ON oaken_spirits.products(ItemNumber);
-- CREATE UNIQUE INDEX idx_sales_invoice ON oaken_spirits.sales(Invoice);
-- CREATE UNIQUE INDEX idx_salesledger_invoice_note ON oaken_spirits.salesLedger(Invoice, Note);
