-- customers
DROP TABLE IF EXISTS customers;

CREATE TABLE customers 
(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    dob TEXT,
    gender TEXT,
    address_line TEXT,
    address_line2 TEXT,
    city TEXT,
    country TEXT,
    credits REAL
);


INSERT INTO customers (username, password, first_name, last_name, phone, dob, gender, address_line, address_line2, city, country, admin)
VALUES
    ("sampleuser", "pbkdf2:sha256:260000$PWBqysgRgwZu29FI$c55cb445d03264b0977807abba784523ce7e26963174750ef61649512008b363", "sample", "user", "0831234567", '2003-02-26', "m", "14 Sunway drive", "Main Street Avenue", "Dublin", "Ireland", 50)
;