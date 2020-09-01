CREATE DATABASE urllookupservice;
use urllookupservice;

CREATE TABLE lookup (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(255) UNIQUE NOT NULL,
    safe BOOLEAN NOT NULL,
    details TEXT
);