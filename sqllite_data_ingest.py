import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("office_llm.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department_id INTEGER,
    hire_date TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS salaries (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    salary REAL NOT NULL,
    pay_date TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
)
""")

# Insert dummy data
cursor.executemany("INSERT INTO departments (id, name) VALUES (?, ?)", [
    (1, 'Engineering'),
    (2, 'Human Resources'),
    (3, 'Marketing'),
    (4, 'Finance'),
    (5, 'Sales')
])

cursor.executemany("INSERT INTO employees (id, name, email, department_id, hire_date) VALUES (?, ?, ?, ?, ?)", [
    (1, 'Alice Johnson', 'alice.johnson@example.com', 1, '2023-01-15'),
    (2, 'Bob Smith', 'bob.smith@example.com', 2, '2022-11-20'),
    (3, 'Charlie Brown', 'charlie.brown@example.com', 3, '2021-07-10'),
    (4, 'David Wilson', 'david.wilson@example.com', 4, '2020-05-25'),
    (5, 'Emma Davis', 'emma.davis@example.com', 5, '2019-03-30')
])

cursor.executemany("INSERT INTO salaries (id, employee_id, salary, pay_date) VALUES (?, ?, ?, ?)", [
    (1, 1, 75000.00, '2024-03-01'),
    (2, 2, 60000.00, '2024-03-01'),
    (3, 3, 55000.00, '2024-03-01'),
    (4, 4, 80000.00, '2024-03-01'),
    (5, 5, 70000.00, '2024-03-01')
])

# Commit and close connection
conn.commit()
conn.close()

print("Data successfully inserted into SQLite database.")
