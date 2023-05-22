CREATE DATABASE IF NOT EXISTS your_database;

USE your_database;

CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(12) NOT NULL,
    topic_of_discussion VARCHAR(255) NOT NULL,
    follow_up_date DATE NOT NULL
);
