-- customers
DROP TABLE IF EXISTS users;

CREATE TABLE users; 
(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    verified BOOLEAN NOT NULL DEFAULT 0,
    admin BOOLEAN NOT NULL DEFAULT 0,
);


INSERT INTO customers (username, password, first_name, last_name, email)
VALUES
    ("sampleuser", "pbkdf2:sha256:260000$PWBqysgRgwZu29FI$c55cb445d03264b0977807abba784523ce7e26963174750ef61649512008b363", "sample", "user", "0831234567", '2003-02-26', "m", "14 Sunway drive", "Main Street Avenue", "Dublin", "Ireland", 50)
;