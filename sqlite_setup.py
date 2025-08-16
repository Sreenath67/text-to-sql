import sqlite3

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# Drop tables if exist
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("DROP TABLE IF EXISTS products;")
cursor.execute("DROP TABLE IF EXISTS orders;")

# Create tables
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    phone_number TEXT
)
''')

cursor.execute('''
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    price REAL
)
''')

cursor.execute('''
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    order_date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
''')

# Insert sample data
cursor.execute('''INSERT INTO users VALUES (1, 'Alice', 30, '1234567890')''')
cursor.execute('''INSERT INTO users VALUES (2, 'Bob', 25, '9876543210')''')
cursor.execute('''INSERT INTO users VALUES (3, 'Charlie', 35, '5555555555')''')

cursor.execute('''INSERT INTO products VALUES (1, 'Laptop', 800.0)''')
cursor.execute('''INSERT INTO products VALUES (2, 'Phone', 500.0)''')
cursor.execute('''INSERT INTO products VALUES (3, 'Tablet', 300.0)''')

cursor.execute('''INSERT INTO orders VALUES (1, 1, 2, '2024-01-10')''')
cursor.execute('''INSERT INTO orders VALUES (2, 2, 1, '2024-02-15')''')
cursor.execute('''INSERT INTO orders VALUES (3, 3, 3, '2024-03-20')''')

conn.commit()
conn.close()
