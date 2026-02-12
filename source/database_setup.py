import sqlite3

def setup_database():
    # Σύνδεση στη βάση (δημιουργεί το αρχείο sport_store.db)
    conn = sqlite3.connect('sport_store.db')
    cursor = conn.cursor()

    # Διαγραφή παλιών πινάκων 
    cursor.execute("DROP TABLE IF EXISTS order_items")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS teams")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("DROP TABLE IF EXISTS salespeople")
    cursor.execute("DROP TABLE IF EXISTS stores")

    # 1. Πίνακας Stores 
    cursor.execute("""CREATE TABLE stores (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT,
        operating_hours TEXT,
        phone TEXT
    )""")

    # 2. Πίνακας Salespeople 
    cursor.execute("""CREATE TABLE salespeople (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        address TEXT,
        phone TEXT,
        email TEXT UNIQUE,
        commission_rate REAL,
        total_commission REAL DEFAULT 0,
        store_id INTEGER,
        FOREIGN KEY (store_id) REFERENCES stores(id)
    )""")

    # 3. Πίνακας Customers 
    cursor.execute("""CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        address TEXT,
        city TEXT,
        phone TEXT,
        email TEXT UNIQUE,
        current_balance REAL DEFAULT 0,
        salesperson_id INTEGER,
        FOREIGN KEY (salesperson_id) REFERENCES salespeople(id)
    )""")

    # 4. Πίνακας Teams 
    cursor.execute("""CREATE TABLE teams (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        number_of_players INTEGER,
        discount_rate REAL,
        representative_customer_id INTEGER UNIQUE,
        FOREIGN KEY (representative_customer_id) REFERENCES customers(id)
    )""")

    # 5. Πίνακας Products 
    cursor.execute("""CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        sales_price REAL NOT NULL,
        wholesale_cost REAL,
        category TEXT,
        stock_quantity INTEGER DEFAULT 0,
        store_id INTEGER,
        FOREIGN KEY (store_id) REFERENCES stores(id)
    )""")

    # 6. Πίνακας Orders 
    cursor.execute("""CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT,
        total_amount REAL,
        customer_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )""")

    # 7. Πίνακας Order Items 
    cursor.execute("""CREATE TABLE order_items (
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        PRIMARY KEY (order_id, product_id),
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )""")

    # --- ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ ---
    # Stores
    cursor.execute("INSERT INTO stores VALUES (1, 'Sport Store Corfu', 'Γ. Θεοτόκη 15', '09:00-21:00', '2661012345')")

    # Salespeople 
    sales_data = [
        (1, 'Νίκος Παπαδόπουλος', 'Πατησίων 50', '2101234567', 'nikos@sports.gr', 0.10, 150.0, 1),
        (2, 'Άννα Παππά', 'Πανεπιστημίου 10', '2107654321', 'anna@sports.gr', 0.12, 300.0, 1),
        (3, 'Δημήτρης Λάμπρου', 'Βουλγάρεως 5', '2661099999', 'dimitris@sports.gr', 0.08, 50.0, 1)
    ]
    cursor.executemany("INSERT INTO salespeople VALUES (?,?,?,?,?,?,?,?)", sales_data)

    # Customers 
    cust_data = [
        (1, 'Γιώργος Γεωργίου', 'Κανόνι', 'Liverpool', '6987778888', 'george@mail.com', 0.0, 1),
        (2, 'Μαρία Οικονόμου', 'Σολωμού 4', 'Starford', '6944445555', 'maria@mail.com', 120.0, 2),
        (3, 'Κώστας Νικολάου', 'Λίνα 12', 'Liverpool', '6933332222', 'kostas@mail.com', 0.0, 1),
        (4, 'Ελένη Παππά', 'Πλ. Γεωργίου', 'Starford', '6977123456', 'eleni@mail.com', 50.0, 3),
        (5, 'Ιωάννης Φωκάς', 'Εσπλανάδα', 'Liverpool', '6911223344', 'fokas@mail.com', 0.0, 2)
    ]
    cursor.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)", cust_data)

    # Teams 
    teams_data = [
        (1, 'Κεραυνός FC', 22, 0.15, 1),
        (2, 'Αετός Κέρκυρας', 18, 0.10, 4)
    ]
    cursor.executemany("INSERT INTO teams VALUES (?,?,?,?,?)", teams_data)

    # Products 
    prod_data = [
        (1, 'Αθλητικές Κάλτσες', 'Κάλτσες προπόνησης', 5.50, 2.00, 'Ένδυση', 100, 1),
        (2, 'Μπάλα Ποδοσφαίρου', 'FIFA Quality 1', 45.00, 25.00, 'Εξοπλισμός', 50, 1),
        (3, 'Φανέλα Ομάδας', 'Dry-fit υλικό', 25.00, 12.00, 'Ένδυση', 40, 1),
        (4, 'Παπούτσια Ποδοσφαίρου', 'Για γρασίδι', 85.00, 45.00, 'Υπόδηση', 20, 1),
        (5, 'Χρονόμετρο', 'Ψηφιακό', 14.00, 7.00, 'Εξοπλισμός', 15, 1)
    ]
    cursor.executemany("INSERT INTO products VALUES (?,?,?,?,?,?,?,?)", prod_data)

    conn.commit()
    conn.close()
    print("Η βάση δημιουργήθηκε επιτυχώς με όλους τους πίνακες και δεδομένα!")

setup_database()
