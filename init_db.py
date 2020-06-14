import sqlite3
import os

# Convert digital data to binary format
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insert(category, item, description, occurdate, time, photo):
    try:
        connection = sqlite3.connect('database.db')
        with open("schema.sql") as f:
            connection.executescript(f.read())
        cur = connection.cursor()
        sqlite_insert = """ INSERT INTO items (category, item, description, occurdate, time, photo) VALUES (?, ?, ?, ?, ?, ?)"""
        empPhoto = convertToBinaryData(photo)
        data_tuple = (category, item, description, occurdate, time, empPhoto)
        cur.execute(sqlite_insert, data_tuple)
        connection.commit()
        cur.close()
    
    except sqlite3.Error as error:
        print('Failed to insert blob data into sqlite table', error)
    
    finally:
        if (connection):
            connection.close()

walletpath = os.path.join(os.getcwd(), 'images', 'wallet.png')
sleevepath = os.path.join(os.getcwd(), 'images', 'sleeve.jpg')
insert('Valuable', 'Wallet', 'Found at utown Starbucks', '14/02/2020', '15:45:57', walletpath)
insert('Accessories', 'Laptop Sleeve', 'Found at the deck', '15/02/2020', '16:00:00', sleevepath)
