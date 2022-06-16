-- admins
DROP TABLE IF EXISTS admins;

CREATE TABLE admins
(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    user_type TEXT NOT NULL,
    credits INTEGER
);

INSERT INTO admins (username, password, first_name, last_name, user_type, credits)
VALUES
    ("hughjeegoh", "pbkdf2:sha256:260000$PWBqysgRgwZu29FI$c55cb445d03264b0977807abba784523ce7e26963174750ef61649512008b363", "Hugh", "Jeegoh", "Admin", 1000000)
;

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


INSERT INTO customers (username, password, first_name, last_name, phone, dob, gender, address_line, address_line2, city, country, credits)
VALUES
    ("sampleuser", "pbkdf2:sha256:260000$PWBqysgRgwZu29FI$c55cb445d03264b0977807abba784523ce7e26963174750ef61649512008b363", "sample", "user", "0831234567", '2003-02-26', "m", "14 Sunway drive", "Main Street Avenue", "Dublin", "Ireland", 50)
;

-- products
DROP TABLE IF EXISTS products;

CREATE TABLE products
(
    sku INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    origin TEXT,
    description TEXT,
    price DECIMAL NOT NULL,
    availability INTEGER NOT NULL
);

INSERT INTO products (product_name, origin, description, price, availability)
VALUES
    ("Arabica", "Ethiopia", "Arabica can be sweet with fruity notes but can also have nutty flavours. They tend to have a higher acidity than Robusta beans which gives them a winey tone.", 12.99, 16),
    ("Robusta", "Congo", "Robusta beans can be deep in flavour with a more distinct woody and nutty taste. Robusta coffee tastes bitter and has higher caffeine content.", 15.49, 10),
    ("Liberica", "Malaysia", "Liberica has a rich unique flavour with a smokey and chocolatey taste, many peopel particularly like this because the taste is accompanied by floral and spicy undertones.", 9.99, 50),
    ("Espresso", "Kenya", "Espresso can be rich with subtle and complex flavors. Fruity and floral aromas, fascinating spice and pine notes, pleasant citrus acidity", 22.49, 50),
    ("French Roast", "Indonesia", "The French roast is generally going to be more intense and smoky, with a thin body.", 30.49, 40),
    ("Italian Roast", "Italy", "Italian roast is the darkest and oiliest of all the roasts, so much so that the beans tend to look almost black and have a slightly burnt taste.", 22.49, 25),
    ("Dark Roast", "Columbia", "Dark roasted beans are oilier, which sometimes leads to a bittersweet or toasty taste, as well as decadent chocolaty flavor.", 30.49, 30),
    ("Mystery Coffee", "Unknown", "This is a not so special, extra special coffee. These is no other coffee like this... or maybe there is...who knows?", 499.99, 1)
    ;

-- giftcards
DROP TABLE IF EXISTS giftcards;

CREATE TABLE giftcards
(
    code TEXT PRIMARY KEY,
    value REAL NOT NULL,
    uses INTEGER NOT NULL
);

INSERT INTO giftcards (code, value, uses)
VALUES
    ('card1', 50, 10)
;

-- discounts
DROP TABLE IF EXISTS discounts;

CREATE TABLE discounts
(
    code TEXT PRIMARY KEY,
    value REAL NOT NULL,
    uses INTEGER NOT NULL
);

INSERT INTO discounts (code, value, uses)
VALUES
    ('10OFF', 10, 5),
    ('50OFF', 50, 5)
;

SELECT *
FROM giftcards;

SELECT *
FROM discounts;

SELECT *
FROM admins;

SELECT *
FROM customers;

SELECT *
FROM products;

SELECT *
FROM orders;

SELECT *
FROM orderdetails;

SELECT credits FROM customers WHERE username = 'sampleuser';