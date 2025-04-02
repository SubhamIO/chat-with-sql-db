# chat-with-sql-db

LINK : https://chat-with-sqldb.streamlit.app/



## Few required STEPS to perform before using the app:
- For my mac 12.7.6 monteray: mysqlserver: 8.0.41, and mysql workbench: 8.0.30

1. download my sql server: https://www.youtube.com/watch?v=ODA3rWfmzg8 
2. download my sql workbench: https://www.youtube.com/watch?v=vQPBNCvboSo
3. install both in sequence 
4. open workbench and click on localhost sql server

5. create schema student
CREATE SCHEMA `office_llm` ;

6.create table student - sqllite - code present here : sqllite_data_ingest.py

7. create table student - mysql server
use office_llm;

-- Create tables
CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INT,
    hire_date DATE NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE salaries (
    id INT PRIMARY KEY,
    employee_id INT,
    salary DECIMAL(10,2) NOT NULL,
    pay_date DATE NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Insert dummy data
INSERT INTO departments (id, name) VALUES 
(1, 'Engineering'),
(2, 'Human Resources'),
(3, 'Marketing'),
(4, 'Finance'),
(5, 'Sales');

INSERT INTO employees (id, name, email, department_id, hire_date) VALUES 
(1, 'Alice Johnson', 'alice.johnson@example.com', 1, '2023-01-15'),
(2, 'Bob Smith', 'bob.smith@example.com', 2, '2022-11-20'),
(3, 'Charlie Brown', 'charlie.brown@example.com', 3, '2021-07-10'),
(4, 'David Wilson', 'david.wilson@example.com', 4, '2020-05-25'),
(5, 'Emma Davis', 'emma.davis@example.com', 5, '2019-03-30');

INSERT INTO salaries (id, employee_id, salary, pay_date) VALUES 
(1, 1, 75000.00, '2024-03-01'),
(2, 2, 60000.00, '2024-03-01'),
(3, 3, 55000.00, '2024-03-01'),
(4, 4, 80000.00, '2024-03-01'),
(5, 5, 70000.00, '2024-03-01');

