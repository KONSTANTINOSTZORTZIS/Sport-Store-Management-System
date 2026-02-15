-- Αρχικά δεδομένα για το Σύστημα Διαχείρισης Αθλητικού Καταστήματος
-- Συμβατά με το τελικό σχήμα (Schema)

-- 1. Καταστήματα
INSERT INTO stores (id, name, address, phone) 
VALUES (1, 'Sport Store Corfu', 'Γ. Θεοτόκη 15', '2661012345');
INSERT INTO stores (id, name, address, phone) 
VALUES (2, 'Cosmos Store Corfu', 'Ακαδημίας 33', '2661067290');

-- 2. Πωλητές
INSERT INTO salespeople (id, full_name, email, store_id) 
VALUES (1, 'Νίκος Παπαδόπουλος', 'nikos@sports.gr', 1);
INSERT INTO salespeople (id, full_name, email, store_id) 
VALUES (2, 'Άννα Παππά', 'anna@sports.gr', 1);
INSERT INTO salespeople (id, full_name, email, store_id) 
VALUES (3, 'Αλέξανδρος Τσουβέλας', 'alex@store.gr', 2);
INSERT INTO salespeople (id, full_name, email, store_id) 
VALUES (4, 'Ιωάννα Αντωνίου', 'ioanna@store.gr', 2);

-- 3. Προϊόντα (Συμπεριλαμβάνει wholesale_cost & stock_quantity)
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Μπάλα Ποδοσφαίρου', 'FIFA Quality 1', 'Εξοπλισμός', 45.00, 50, 25.00);
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Αθλητικές Κάλτσες', 'Κάλτσες προπόνησης', 'Ένδυση', 5.50, 100, 2.00);
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Χρονόμετρο Διαιτητή', 'Ψηφιακό', 'Εξοπλισμός', 14.00, 15, 8.00);
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Φανέλα Ομάδας', 'Dry-fit υλικό', 'Ένδυση', 35.00, 20, 14.00);
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Επικαλαμίδες','Υαλοβάμβακας', 'Εξοπλισμός', 7.00, 15, 3.00);
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Σορτς Ομάδας','Dry-fit υλικό', 'Ένδυση', 20.00, 20, 10.00);
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Γάντια Τερματοφύλακα','Ethylene Vinyl Acetate', 'Εξοπλισμός', 17.00, 10, 10.00);
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Παγούρι Νερού','Ανοξείδωτο Ατσάλι', 'Εξοπλισμός', 10.00, 8, 4.00);

-- 4. Πελάτες 
INSERT INTO customers (full_name, email, phone, city, salesperson_id) 
VALUES ('Γιώργος Γεωργίου', 'george@mail.com', '6987778888', 'Liverpool', 1);
INSERT INTO customers (full_name, email, phone, city, salesperson_id) 
VALUES ('Μαρία Οικονόμου', 'maria@mail.com', '6944445555', 'Starford', 2);
INSERT INTO customers (full_name, email, phone, city, salesperson_id) 
VALUES ('Κώστας Νικολάου', 'kostas@mail.com', '6933332222', 'Liverpool', 1);

-- 5. Ομάδες
INSERT INTO teams (id, name, number_of_players, representative_customer_id) 
VALUES (1, 'Κεραυνός FC', 22, 1);
INSERT INTO teams (id, name, number_of_players, representative_customer_id) 
VALUES (2, 'Μπαμ FC', 22, 2);

-- 6. Παραγγελίες
INSERT INTO orders (total_amount, customer_id) VALUES (55.00, 1);
INSERT INTO orders (total_amount, customer_id) VALUES (120.00, 2);
INSERT INTO orders (total_amount, customer_id) VALUES (30.00, 3);
