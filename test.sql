CREATE DATABASE atm_db;
USE atm_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    pin VARCHAR(4) NOT NULL
);

CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    account_number VARCHAR(20) UNIQUE,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    type ENUM('WITHDRAW', 'DEPOSIT', 'TRANSFER', 'BALANCE_CHECK'),
    amount DECIMAL(10, 2),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);


INSERT INTO users (name, email, pin) VALUES 
('John Doe', 'john@example.com', '1234'),
('Jane Smith', 'jane@example.com', '5678');

INSERT INTO accounts (user_id, account_number, balance) VALUES 
(1, '1234567890', 1000.00),
(2, '0987654321', 500.00);
USE atm_db;
SELECT * FROM users;
SELECT * FROM accounts;
-- Add to your existing SQL script or run in MySQL console
INSERT INTO users (name, email, pin) VALUES 
('Alice Johnson', 'alice@example.com', '4321');

INSERT INTO accounts (user_id, account_number, balance) VALUES 
(3, '1122334455', 1500.00);