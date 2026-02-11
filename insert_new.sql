-- Αρχικά δεδομένα για το Σύστημα Διαχείρισης Αθλητικού Καταστήματος

-- Καταστήματα
INSERT INTO stores VALUES (1, 'Sport Store Corfu', 'Γ. Θεοτόκη 15', '2661012345');

-- Πωλητές
INSERT INTO salespeople VALUES (1, 'Νίκος Παπαδόπουλος', 'nikos@sports.gr', 1);
INSERT INTO salespeople VALUES (2, 'Άννα Παππά', 'anna@sports.gr', 1);

-- Προϊόντα
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Μπάλα Ποδοσφαίρου', 'FIFA Quality', 'Εξοπλισμός', 45.00, 50, 25.00);
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Αθλητικές Κάλτσες', 'Κάλτσες προπόνησης', 'Ένδυση', 5.50, 100, 2.00);
INSERT INTO products (name, description, category, sales_price, stock_quantity, wholesale_cost) 
VALUES ('Χρονόμετρο Διαιτητή', 'Ψηφιακό', 'Διάφορα', 14.00, 15, 8.00);

-- Πελάτες
INSERT INTO customers (full_name, email, phone, city, salesperson_id) 
VALUES ('Γιώργος Γεωργίου', 'george@mail.com', '6987778888', 'Liverpool', 1);
INSERT INTO customers (full_name, email, phone, city, salesperson_id) 
VALUES ('Μαρία Οικονόμου', 'maria@mail.com', '6989998888', 'Starford', 2);

-- Ομάδες
INSERT INTO teams VALUES (1, 'Κεραυνός FC', 22, 1);

-- Παραγγελίες
INSERT INTO orders (total_amount, customer_id) VALUES (55.00, 1);
INSERT INTO orders (total_amount, customer_id) VALUES (120.00, 2);