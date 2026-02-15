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
        cursor.execute("CREATE TABLE stores (id INTEGER PRIMARY KEY, name TEXT, address TEXT, phone TEXT)")
        cursor.execute("CREATE TABLE salespeople (id INTEGER PRIMARY KEY, full_name TEXT, email TEXT, store_id INTEGER, FOREIGN KEY(store_id) REFERENCES stores(id))")
        cursor.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, email TEXT UNIQUE, phone TEXT, city TEXT, salesperson_id INTEGER, FOREIGN KEY(salesperson_id) REFERENCES salespeople(id))")
        cursor.execute("CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, category TEXT, sales_price REAL, stock_quantity INTEGER, wholesale_cost REAL)")
        cursor.execute("CREATE TABLE teams (id INTEGER PRIMARY KEY, name TEXT, number_of_players INTEGER, representative_customer_id INTEGER UNIQUE, FOREIGN KEY(representative_customer_id) REFERENCES customers(id))")
        cursor.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, total_amount REAL, customer_id INTEGER, FOREIGN KEY(customer_id) REFERENCES customers(id))")
        
        # Ενδεικτικά αρχικά δεδομένα για να λειτουργούν οι αναζητήσεις
        cursor.execute("INSERT INTO stores VALUES (1, 'Κεντρικό Κέρκυρα', 'Γ. Θεοτόκη 15', '2661012345')")
        cursor.execute("INSERT INTO salespeople VALUES (1, 'Νίκος Παπαδόπουλος', 'nikos@sports.gr', 1)")
        conn.commit()
    conn.close()

# --- 2. ΣΥΝΑΡΤΗΣΕΙΣ ΛΟΓΙΚΗΣ ---
def run_query(n):
    conn = sqlite3.connect('sport_store.db')
    cursor = conn.cursor()
    
    # Καθαρισμός παλιών δεδομένων στο Treeview
    for i in tree.get_children(): tree.delete(i)
    
    # Ορισμός ερωτημάτων και επικεφαλίδων βάσει PDF 
    if n == 0: # 1. Στοιχεία πελατών 
        headers = ["ID", "Ονοματεπώνυμο", "Email", "Τηλέφωνο", "Πόλη"]
        query = "SELECT id, full_name, email, phone, city FROM customers"

    elif n == 1: # 2. Στοιχεία ομάδων 
        headers = ["Όνομα Ομάδας", "Πλήθος Παικτών"]
        query = "SELECT name, number_of_players FROM teams"

    elif n == 2: # 3. Στοιχεία προϊόντων 
        headers = ["Προϊόν", "Περιγραφή", "Κατηγορία"]
        query = "SELECT name, description, category FROM products"

    elif n == 3: # 4. Προϊόντα 3.00 - 15.00€ 
        headers = ["Κωδικός", "Προϊόν", "Κόστος Χονδρ.", "Απόθεμα"]
        query = "SELECT id, name, wholesale_cost, stock_quantity FROM products WHERE sales_price BETWEEN 3.00 AND 15.00"

    elif n == 4: # 5. Πελάτες σε Starford ή Liverpool 
        headers = ["ID Πελάτη", "Ονοματεπώνυμο", "Πόλη"]
        query = "SELECT id, full_name, city FROM customers WHERE city IN ('Starford', 'Liverpool')"

    elif n == 5: # 6. Μέσος όρος πωλήσεων ανά πωλητή 
        headers = ["Πωλητής", "Μέσος Όρος (€)"]
        query = """SELECT s.full_name, ROUND(AVG(o.total_amount), 2) 
                   FROM salespeople s 
                   JOIN customers c ON s.id = c.salesperson_id 
                   JOIN orders o ON c.id = o.customer_id 
                   GROUP BY s.id"""
        
    elif n == 6: # 7. Μεγαλύτερη παραγγελία (Πωλητής & Πελάτης) 
        headers = ["Πωλητής", "Πελάτης", "Ποσό (€)"]
        query = """SELECT s.full_name, c.full_name, MAX(o.total_amount) 
                   FROM orders o 
                   JOIN customers c ON o.customer_id = c.id 
                   JOIN salespeople s ON c.salesperson_id = s.id"""

    # Ενημέρωση Treeview με τις στήλες της κάθε ερώτησης 
    tree["columns"] = headers
    for h in headers:
        tree.heading(h, text=h)
        tree.column(h, width=130, anchor="center")

    try:
        cursor.execute(query)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Σφάλμα SQL", f"Λεπτομέρειες: {e}")
    finally:
        conn.close()



def save_entry(table, columns, values):
    # Έλεγχος για κενά πεδία (Validation)
    if any(str(v).strip() == "" for v in values):
        messagebox.showwarning("Προσοχή", "Παρακαλώ συμπληρώστε όλα τα πεδία!")
        return
    # Έλεγχος αν το τηλέφωνο είναι αριθμός (πρόσθεσέ το μετά τον έλεγχο των προϊόντων)
    if table == "customers":
        if not values[2].isdigit() and values[2] != "":
            messagebox.showerror("Σφάλμα", "Το τηλέφωνο πρέπει να περιέχει μόνο ψηφία!")
            return

    # Έλεγχος αν οι τιμές/ποσότητες είναι αριθμοί (Validation)
    if table == "products":
        try:
            float(values[1]) # sales_price (Τιμή Πώλησης)
            int(values[3])   # stock_quantity (Απόθεμα) 
            float(values[4]) # wholesale_cost (Κόστος Χονδρικής) 
        except ValueError:
            messagebox.showerror("Σφάλμα", "Η τιμή και το απόθεμα πρέπει να είναι αριθμοί!")
            return

    try:
        conn = sqlite3.connect('sport_store.db')
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(values))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        messagebox.showinfo("Επιτυχία", "Η εγγραφή αποθηκεύτηκε!")
        refresh_combos()
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Αποτυχία αποθήκευσης: {e}")

def refresh_combos():
    try:
        conn = sqlite3.connect('sport_store.db')
        cursor = conn.cursor()
        
        # Γέμισμα Πωλητών
        cursor.execute("SELECT id, full_name FROM salespeople")
        cb_c_sales['values'] = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
        
        # Γέμισμα Πελατών
        cursor.execute("SELECT id, full_name FROM customers")
        cb_o_cust['values'] = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
        
        # Γέμισμα Καταστημάτων (Νέο)
        cursor.execute("SELECT id, name FROM stores")
        cb_o_store['values'] = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
        
        # Γέμισμα Προϊόντων (Νέο)
        cursor.execute("SELECT id, name FROM products")
        cb_o_prod['values'] = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
        
        conn.close()
    except: pass
        
    

# --- 3. UI SETUP ---
def save_order_logic():
    try:
        cust_id = cb_o_cust.get().split(" - ")[0]
        prod_id = cb_o_prod.get().split(" - ")[0]
        qty = int(en_o_qty.get())
        
        conn = sqlite3.connect('sport_store.db')
        cursor = conn.cursor()
        
        # Βρίσκουμε την τιμή του προϊόντος
        cursor.execute("SELECT sales_price FROM products WHERE id=?", (prod_id,))
        price = cursor.fetchone()[0]
        total = price * qty
        
        # Αποθήκευση στην SQL
        cursor.execute("INSERT INTO orders (customer_id, total_amount) VALUES (?, ?)", (cust_id, total))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Επιτυχία", f"Η παραγγελία καταχωρήθηκε!\nΣυνολικό ποσό: {total}€")
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Συμπληρώστε σωστά όλα τα πεδία: {e}")


init_db()
root = tk.Tk()
root.title("Sport Store Management v2.0")
root.geometry("700x550")

nb = ttk.Notebook(root)
nb.pack(pady=10, expand=True, fill="both")

# ΚΑΡΤΕΛΑ: ΠΕΛΑΤΕΣ
t_c = ttk.Frame(nb); nb.add(t_c, text=" Πελάτες ")
tk.Label(t_c, text="Ονοματεπώνυμο:").grid(row=0, column=0, padx=5, pady=5)
en_c_n = tk.Entry(t_c); en_c_n.grid(row=0, column=1)

tk.Label(t_c, text="Email:").grid(row=1, column=0)
en_c_e = tk.Entry(t_c); en_c_e.grid(row=1, column=1)

tk.Label(t_c, text="Τηλέφωνο:").grid(row=2, column=0) # Νέο πεδίο
en_c_p = tk.Entry(t_c); en_c_p.grid(row=2, column=1)

tk.Label(t_c, text="Πόλη:").grid(row=3, column=0)
en_c_t = tk.Entry(t_c); en_c_t.grid(row=3, column=1)

tk.Label(t_c, text="Υπεύθυνος Πωλητής:").grid(row=4, column=0)
cb_c_sales = ttk.Combobox(t_c); cb_c_sales.grid(row=4, column=1)

tk.Button(t_c, text="Αποθήκευση Πελάτη", bg="#e1f5fe", 
          command=lambda: save_entry("customers", 
                                     ["full_name","email","phone","city","salesperson_id"], 
                                     [en_c_n.get(), en_c_e.get(), en_c_p.get(), en_c_t.get(), cb_c_sales.get().split(" - ")[0]])
         ).grid(row=5, column=1, pady=10)

# ΚΑΡΤΕΛΑ: ΠΡΟΪΟΝΤΑ (Βελτιωμένη με wholesale & stock)
t_p = ttk.Frame(nb); nb.add(t_p, text=" Προϊόντα ")
tk.Label(t_p, text="Όνομα:").grid(row=0, column=0, padx=5, pady=5); en_p_n = tk.Entry(t_p); en_p_n.grid(row=0, column=1)
tk.Label(t_p, text="Τιμή Πώλησης:").grid(row=1, column=0); en_p_s = tk.Entry(t_p); en_p_s.grid(row=1, column=1)
tk.Label(t_p, text="Κατηγορία:").grid(row=2, column=0); en_p_c = tk.Entry(t_p); en_p_c.grid(row=2, column=1)
tk.Label(t_p, text="Απόθεμα:").grid(row=3, column=0); en_p_q = tk.Entry(t_p); en_p_q.grid(row=3, column=1)
tk.Label(t_p, text="Κόστος Χονδρικής:").grid(row=4, column=0); en_p_w = tk.Entry(t_p); en_p_w.grid(row=4, column=1)
tk.Button(t_p, text="Αποθήκευση Προϊόντος", bg="#e8f5e9", command=lambda: save_entry("products", ["name","sales_price","category","stock_quantity","wholesale_cost"], [en_p_n.get(), en_p_s.get(), en_p_c.get(), en_p_q.get(), en_p_w.get()])).grid(row=5, column=1, pady=10)

# ΚΑΡΤΕΛΑ: ΠΑΡΑΓΓΕΛΙΕΣ 
t_o = ttk.Frame(nb); nb.add(t_o, text=" Παραγγελίες ")

# Επιλογή Πελάτη
tk.Label(t_o, text="Πελάτης:").grid(row=0, column=0, padx=5, pady=5)
cb_o_cust = ttk.Combobox(t_o); cb_o_cust.grid(row=0, column=1)

# Επιλογή Καταστήματος (Νέο)
tk.Label(t_o, text="Κατάστημα:").grid(row=1, column=0, padx=5, pady=5)
cb_o_store = ttk.Combobox(t_o); cb_o_store.grid(row=1, column=1)

# Επιλογή Προϊόντος (Νέο)
tk.Label(t_o, text="Προϊόν:").grid(row=2, column=0, padx=5, pady=5)
cb_o_prod = ttk.Combobox(t_o); cb_o_prod.grid(row=2, column=1)

# Ποσότητα (Νέο)
tk.Label(t_o, text="Ποσότητα:").grid(row=3, column=0, padx=5, pady=5)
en_o_qty = tk.Entry(t_o); en_o_qty.grid(row=3, column=1)
en_o_qty.insert(0, "1") # Προεπιλεγμένη τιμή

# Κουμπί Καταχώρησης
tk.Button(t_o, text="Καταχώρηση Παραγγελίας", bg="#fff3e0", 
          command=lambda: save_order_logic()).grid(row=4, column=1, pady=10)

# ΚΑΡΤΕΛΑ: ΑΝΑΖΗΤΗΣΕΙΣ (Βελτιωμένο Treeview) 
t_s = ttk.Frame(nb); nb.add(t_s, text=" Αναζητήσεις/Queries ")

tk.Label(t_s, text="Επιλέξτε μια ερώτηση για να δείτε τα αποτελέσματα:", font=("Arial", 10, "bold")).pack(pady=10)

btn_frame = tk.Frame(t_s)
btn_frame.pack(side="top", fill="x", padx=5, pady=5)

# Δημιουργία των 7 κουμπιών 
for i in range(7):
    tk.Button(btn_frame, text=f"Ερώτηση {i+1}", width=12, 
              command=lambda idx=i: run_query(idx)).pack(side="left", padx=5)

tree = ttk.Treeview(t_s, show="headings")
tree.pack(expand=True, fill="both", padx=10, pady=10)


refresh_combos()
root.mainloop()
