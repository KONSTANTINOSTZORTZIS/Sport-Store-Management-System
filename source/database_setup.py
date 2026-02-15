import sqlite3
import os

def setup_database():
    db_name = 'sport_store.db'
    sql_file = 'insert_new.sql'
    
    # Σύνδεση στη βάση (αν δεν υπάρχει, τη δημιουργεί. Αν υπάρχει, την ανοίγει)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 1. Δημιουργία Πινάκων ΜΟΝΟ αν δεν υπάρχουν (IF NOT EXISTS)
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS stores (id INTEGER PRIMARY KEY, name TEXT, address TEXT, phone TEXT);
    CREATE TABLE IF NOT EXISTS salespeople (id INTEGER PRIMARY KEY, full_name TEXT, email TEXT, store_id INTEGER, FOREIGN KEY(store_id) REFERENCES stores(id));
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, email TEXT UNIQUE, phone TEXT, city TEXT, salesperson_id INTEGER, FOREIGN KEY(salesperson_id) REFERENCES salespeople(id));
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, category TEXT, sales_price REAL, stock_quantity INTEGER, wholesale_cost REAL);
    CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY, name TEXT, number_of_players INTEGER, representative_customer_id INTEGER UNIQUE, FOREIGN KEY(representative_customer_id) REFERENCES customers(id));
    CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, total_amount REAL, customer_id INTEGER, FOREIGN KEY(customer_id) REFERENCES customers(id));
    """)

    # 2. Εκτέλεση του insert_new.sql για προσθήκη νέων δεδομένων
    if os.path.exists(sql_file):
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_commands = f.read().split(';') # Χωρίζουμε τις εντολές
            for command in sql_commands:
                if command.strip():
                    try:
                        cursor.execute(command)
                    except sqlite3.IntegrityError:
                        # Αν το δεδομένο υπάρχει ήδη , το προσπερνάει
                        pass
                    except Exception as e:
                        print(f"Παράλειψη εντολής λόγω σφάλματος: {e}")
        print(f"Η επεξεργασία του {sql_file} ολοκληρώθηκε. Προστέθηκαν μόνο οι νέες εγγραφές.")
    else:
        print(f"Το αρχείο {sql_file} δεν βρέθηκε.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
