DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    item TEXT NOT NULL,
    description TEXT NOT NULL,
    occurdate DATE,
    time TIME,
    photo BLOB NOT NULL
);
