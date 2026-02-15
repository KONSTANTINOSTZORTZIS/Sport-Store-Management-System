-- Δημιουργία Πινάκων για SQLite (Τελικό Schema Εργασίας)

-- 1. Καταστήματα
CREATE TABLE IF NOT EXISTS stores (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    phone TEXT
);

-- 2. Πωλητές
CREATE TABLE IF NOT EXISTS salespeople (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    store_id INTEGER,
    FOREIGN KEY(store_id) REFERENCES stores(id)
);

-- 3. Πελάτες
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    city TEXT,
    salesperson_id INTEGER,
    FOREIGN KEY(salesperson_id) REFERENCES salespeople(id)
);

-- 4. Προϊόντα
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    sales_price REAL NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    wholesale_cost REAL
);

-- 5. Ομάδες
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    number_of_players INTEGER,
    representative_customer_id INTEGER UNIQUE,
    FOREIGN KEY(representative_customer_id) REFERENCES customers(id)
);

-- 6. Παραγγελίες
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL,
    customer_id INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);
