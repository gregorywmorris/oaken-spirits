CREATE DATABASE oaken;

\c oaken

CREATE SCHEMA oaken;

CREATE TABLE oaken.customers (
    store_id INTEGER NOT NULL,
    Store_name VARCHAR(255) NOT NULL,
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    county VARCHAR(255) NOT NULL,
    us_state VARCHAR(255) NOT NULL,
    zip_code INTEGER NOT NULL,
    PRIMARY KEY (store_id)
);

CREATE TABLE oaken.vendors (
    vendor_id INTEGER NOT NULL,
    vendor_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (vendor_id)
);

CREATE TABLE oaken.categories (
    category_id INTEGER NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (category_id)
);

CREATE TABLE oaken.products (
    item_id INTEGER NOT NULL,
    category_id INTEGER,
    item_description VARCHAR(255) NOT NULL,
    bottle_volume_ml INTEGER NOT NULL,
    pack INTEGER NOT NULL,
    bottle_cost DECIMAL(11,2) NOT NULL,
    bottle_retail DECIMAL(11,2) NOT NULL,
    PRIMARY KEY (item_id),
    FOREIGN KEY (category_id) REFERENCES oaken.categories(category_id)
);

CREATE TABLE oaken.positions (
    title_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    PRIMARY KEY (title_id)
);

CREATE TABLE oaken.employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    title INTEGER,
    manager_id INTEGER,
    active BOOLEAN NOT NULL,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (title) REFERENCES oaken.positions(title_id),
    FOREIGN KEY (manager_id) REFERENCES oaken.employees(employee_id)
);

CREATE TABLE oaken.sales (
    invoice VARCHAR(255) NOT NULL,
    store_id INTEGER NOT NULL,
    vendor_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    sale_amount DECIMAL(11,2) NOT NULL,
    item_id INTEGER NOT NULL,
    bottle_count INTEGER NOT NULL,
    volume_liter DECIMAL(11,2)  NOT NULL,
    shipping_date DATE,
    shipping_cost DECIMAL(11,2),
    PRIMARY KEY (invoice),
    FOREIGN KEY (store_id) REFERENCES oaken.customers(store_id),
    FOREIGN KEY (item_id) REFERENCES oaken.products(item_id),
    FOREIGN KEY (vendor_id) REFERENCES oaken.vendors(vendor_id),
    FOREIGN KEY (employee_id) REFERENCES oaken.employees(employee_id)
);

CREATE TABLE oaken.sales_ledger (
    invoice VARCHAR(255) NOT NULL,
    credit DECIMAL(11,2),
    debit DECIMAL(11,2),
    note VARCHAR(255),
    PRIMARY KEY (invoice, Note),
    FOREIGN KEY (invoice) REFERENCES oaken.sales(invoice)
);

CREATE ROLE airbyte WITH LOGIN PASSWORD 'airbyte';
GRANT ALL PRIVILEGES ON DATABASE oaken TO airbyte;

INSERT INTO oaken.positions VALUES (100, 'CEO');
INSERT INTO oaken.positions VALUES (110, 'Vice President');
INSERT INTO oaken.positions VALUES (120, 'Regional Manager');
INSERT INTO oaken.positions VALUES (130, 'Branch Manager');
INSERT INTO oaken.positions VALUES (140, 'Secretary');
INSERT INTO oaken.positions VALUES (150, 'Sales Representative');
INSERT INTO oaken.positions VALUES (160, 'Accountant');
INSERT INTO oaken.positions VALUES (170, 'Inventory Specialist');
INSERT INTO oaken.positions VALUES (180, 'Human Resource Specialist');
INSERT INTO oaken.positions VALUES (190, 'Customer Service Representative');

INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (10000,'Alan','Brand',100,NULL,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (10001,'Jan','Levinson-Gould',110,10000,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (10002,'Nellie','Bertram',120,10001,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (10003,'Michael','Scott',130,10002,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (10004,'Pam','Beesly',140,10003,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (10005,'Oscar','Nunez',160,10002,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (10006,'Mindy','Kaling',190,10003,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (10007,'Tolby','Flenderson',180,10002,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (10008,'Darryl','Philbin',170,10003,true);
-- Sales
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (20001,'Dwight','Schrute',150,10003,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (20002,'Jim','Halpert',150,10003,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (20003,'Stanley','Hudson',150,10003,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (20004,'Phyllis','Vance',150,10003,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (20005,'Andy','Bernard',150,10003,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (20006,'Danny','Cordray',150,10003,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (20007,'Todd','Packer',150,10003,true);
INSERT INTO oaken.employees (employee_id, first_name, last_name, title, manager_id, active)
    VALUES (20008,'Karen','Filippell',150,10003,true);