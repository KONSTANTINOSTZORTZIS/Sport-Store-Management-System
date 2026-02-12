import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os

# --- 1. ΑΥΤΟΜΑΤΗ ΔΗΜΙΟΥΡΓΙΑ ΒΑΣΗΣ & ΔΕΔΟΜΕΝΩΝ ---
def init_db():
    db_name = 'sport_store.db'
    db_exists = os.path.exists(db_name)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    if not db_exists:
        # Δημιουργία Πινάκων βάσει του σχεδιασμού 
        cursor.execute("CREATE TABLE stores (id INTEGER PRIMARY KEY, name TEXT, address TEXT, phone TEXT)")
        cursor.execute("CREATE TABLE salespeople (id INTEGER PRIMARY KEY, full_name TEXT, email TEXT, store_id INTEGER, FOREIGN KEY(store_id) REFERENCES stores(id))")
        cursor.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, email TEXT UNIQUE, phone TEXT, city TEXT, salesperson_id INTEGER, FOREIGN KEY(salesperson_id) REFERENCES salespeople(id))")
        cursor.execute("CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, category TEXT, sales_price REAL, stock_quantity INTEGER, wholesale_cost REAL)")
        cursor.execute("CREATE TABLE teams (id INTEGER PRIMARY KEY, name TEXT, number_of_players INTEGER, representative_customer_id INTEGER UNIQUE, FOREIGN KEY(representative_customer_id) REFERENCES customers(id))")
        cursor.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, total_amount REAL, customer_id INTEGER, FOREIGN KEY(customer_id) REFERENCES customers(id))")
        
        # Εισαγωγή αρχικών δεδομένων
        cursor.execute("INSERT INTO stores VALUES (1, 'Sport Store Corfu', 'Γ. Θεοτόκη 15', '2661012345')")
        cursor.execute("INSERT INTO salespeople VALUES (1, 'Νίκος Παπαδόπουλος', 'nikos@sports.gr', 1)")
        cursor.execute("INSERT INTO salespeople VALUES (2, 'Άννα Παππά', 'anna@sports.gr', 1)")
        cursor.execute("INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) VALUES ('Μπάλα Ποδοσφαίρου', 'FIFA Quality', 'Εξοπλισμός', 45.00, 50, 25.00)")
        cursor.execute("INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) VALUES ('Αθλητικές Κάλτσες', 'Κάλτσες προπόνησης', 'Ένδυση', 5.50, 100, 2.00)")
        cursor.execute("INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) VALUES ('Χρονόμετρο Διαιτητή', 'Ψηφιακό', 'Διάφορα', 14.00, 15, 8.00)")
        cursor.execute("INSERT INTO customers (full_name, email, phone, city, salesperson_id) VALUES ('Γιώργος Γεωργίου', 'george@mail.com', '6987778888', 'Liverpool', 1)")
        cursor.execute("INSERT INTO customers (full_name, email, phone, city, salesperson_id) VALUES ('Μαρία Οικονόμου', 'maria@mail.com', '6989998888', 'Starford', 2)")
        cursor.execute("INSERT INTO teams VALUES (1, 'Κεραυνός FC', 22, 1)")
        cursor.execute("INSERT INTO orders (total_amount, customer_id) VALUES (55.00, 1)")
        cursor.execute("INSERT INTO orders (total_amount, customer_id) VALUES (120.00, 2)")
        conn.commit()
    conn.close()

# --- 2. ΒΟΗΘΗΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ---
def get_db_connection():
    return sqlite3.connect('sport_store.db')

def update_combos():
    # Ενημέρωση των drop-down menus με τις τρέχουσες τιμές 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name FROM customers")
    custs = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
    cursor.execute("SELECT id, full_name FROM salespeople")
    sales = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
    conn.close()
    cb_c_sales['values'] = sales
    cb_o_cust['values'] = custs

def save_entry(table, cols, vals):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join(['?']*len(vals))})", vals)
        conn.commit()
        conn.close()
        update_combos()
        messagebox.showinfo("Επιτυχία", "Η εγγραφή αποθηκεύτηκε!")
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Αποτυχία εισαγωγής: {e}")

# --- 3. ΕΚΤΕΛΕΣΗ ΕΡΩΤΗΣΕΩΝ  ---
def run_query(n):
    conn = get_db_connection()
    cursor = conn.cursor()
    search = entry_query.get()
    for i in tree_res.get_children(): tree_res.delete(i)
    
    if n == 1: # Πελάτης Χ [cite: 18]
        cursor.execute("SELECT id, full_name, email, phone FROM customers WHERE id=? OR full_name LIKE ?", (search, f"%{search}%"))
    elif n == 2: # Ομάδα Χ [cite: 19]
        cursor.execute("SELECT name, number_of_players, 'N/A', 'N/A' FROM teams WHERE id=? OR name LIKE ?", (search, f"%{search}%"))
    elif n == 3: # Προϊόν Χ [cite: 20]
        cursor.execute("SELECT name, description, category, 'N/A' FROM products WHERE id=? OR name LIKE ?", (search, f"%{search}%"))
    elif n == 4: # Τιμή 3-15 [cite: 21]
        cursor.execute("SELECT id, wholesale_cost, stock_quantity, name FROM products WHERE sales_price BETWEEN 3.00 AND 15.00")
    elif n == 5: # Cities [cite: 22]
        cursor.execute("SELECT id, city, full_name, 'N/A' FROM customers WHERE city IN ('Starford', 'Liverpool')")
    elif n == 6: # Average Sales [cite: 23]
        cursor.execute("SELECT s.full_name, AVG(o.total_amount), 'N/A', 'N/A' FROM salespeople s JOIN customers c ON s.id=c.salesperson_id JOIN orders o ON c.id=o.customer_id GROUP BY s.id")
    elif n == 7: # Max Order [cite: 24]
        cursor.execute("SELECT s.full_name, c.full_name, MAX(o.total_amount), 'N/A' FROM orders o JOIN customers c ON o.customer_id=c.id JOIN salespeople s ON c.salesperson_id=s.id")
    
    for row in cursor.fetchall(): tree_res.insert("", "end", values=row)
    conn.close()

# --- 4. ΣΧΕΔΙΑΣΗ GUI ---
init_db()
root = tk.Tk(); root.title("Εφαρμογή Φοιτητολογίου - Ομάδα 99"); root.geometry("1000x800")
nb = ttk.Notebook(root); nb.pack(expand=True, fill="both")

# ΚΑΡΤΕΛΑ: ΠΕΛΑΤΕΣ 
t_c = ttk.Frame(nb); nb.add(t_c, text=" Πελάτες ")
tk.Label(t_c, text="Όνομα:").grid(row=0, column=0); en_c_n = tk.Entry(t_c); en_c_n.grid(row=0, column=1)
tk.Label(t_c, text="Email:").grid(row=1, column=0); en_c_e = tk.Entry(t_c); en_c_e.grid(row=1, column=1)
tk.Label(t_c, text="Πόλη:").grid(row=2, column=0); en_c_t = tk.Entry(t_c); en_c_t.grid(row=2, column=1)
tk.Label(t_c, text="Πωλητής (Dropdown):").grid(row=3, column=0)
cb_c_sales = ttk.Combobox(t_c); cb_c_sales.grid(row=3, column=1)
tk.Button(t_c, text="Αποθήκευση", command=lambda: save_entry("customers", ["full_name","email","city","salesperson_id"], [en_c_n.get(), en_c_e.get(), en_c_t.get(), cb_c_sales.get().split(" - ")[0]])).grid(row=4, column=1)

# ΚΑΡΤΕΛΑ: ΠΡΟΪΟΝΤΑ 
t_p = ttk.Frame(nb); nb.add(t_p, text=" Προϊόντα ")
tk.Label(t_p, text="Όνομα:").grid(row=0, column=0); en_p_n = tk.Entry(t_p); en_p_n.grid(row=0, column=1)
tk.Label(t_p, text="Τιμή:").grid(row=1, column=0); en_p_s = tk.Entry(t_p); en_p_s.grid(row=1, column=1)
tk.Label(t_p, text="Κατηγορία:").grid(row=2, column=0); en_p_c = tk.Entry(t_p); en_p_c.grid(row=2, column=1)
tk.Button(t_p, text="Αποθήκευση", command=lambda: save_entry("products", ["name","sales_price","category"], [en_p_n.get(), en_p_s.get(), en_p_c.get()])).grid(row=3, column=1)

# ΚΑΡΤΕΛΑ: ΠΑΡΑΓΓΕΛΙΕΣ 
t_o = ttk.Frame(nb); nb.add(t_o, text=" Παραγγελίες ")
tk.Label(t_o, text="Πελάτης (Dropdown):").grid(row=0, column=0)
cb_o_cust = ttk.Combobox(t_o); cb_o_cust.grid(row=0, column=1)
tk.Label(t_o, text="Ποσό:").grid(row=1, column=0); en_o_a = tk.Entry(t_o); en_o_a.grid(row=1, column=1)
tk.Button(t_o, text="Αποθήκευση", command=lambda: save_entry("orders", ["customer_id","total_amount"], [cb_o_cust.get().split(" - ")[0], en_o_a.get()])).grid(row=2, column=1)

# ΚΑΡΤΕΛΑ: ΕΡΩΤΗΣΕΙΣ 
t_q = ttk.Frame(nb); nb.add(t_q, text=" Αναζητήσεις ")
f_s = tk.Frame(t_q); f_s.pack(pady=10)
tk.Label(f_s, text="Αναζήτηση (ID ή Όνομα):").pack(side="left"); entry_query = tk.Entry(f_s); entry_query.pack(side="left", padx=5)
f_b = tk.Frame(t_q); f_b.pack()
for i in range(1, 8): tk.Button(f_b, text=f"Ερώτηση {i}", command=lambda n=i: run_query(n)).pack(side="left", padx=2)
tree_res = ttk.Treeview(t_q, columns=(1,2,3,4), show="headings")
for i, h in enumerate(["Στοιχείο Α", "Στοιχείο Β", "Στοιχείο Γ", "Στοιχείο Δ"], 1): tree_res.heading(i, text=h)
tree_res.pack(fill="both", expand=True, padx=10, pady=10)

update_combos(); root.mainloop()
