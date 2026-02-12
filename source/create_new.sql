-- Δημιουργία Πινάκων για SQLite (Schema)
-- Βασισμένο στις οντότητες του Μέρους Α 

CREATE TABLE stores (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    phone TEXT
);

CREATE TABLE salespeople (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    store_id INTEGER,
    FOREIGN KEY(store_id) REFERENCES stores(id)
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    city TEXT,
    salesperson_id INTEGER,
    FOREIGN KEY(salesperson_id) REFERENCES salespeople(id)
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    sales_price REAL,
    stock_quantity INTEGER,
    wholesale_cost REAL
);

CREATE TABLE teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    number_of_players INTEGER,
    representative_customer_id INTEGER UNIQUE,
    FOREIGN KEY(representative_customer_id) REFERENCES customers(id)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL,
    customer_id INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);
