import sqlite3
import os

# Convert digital data to binary format
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


walletpath = os.path.join(os.getcwd(), 'images', 'wallet.png')
walletphoto = convertToBinaryData(walletpath)
cur.execute("INSERT INTO items (item, description, occurdate, time, photo) VALUES (?, ?, ?, ?, ?)",
            ('Wallet', 'Found at utown Starbucks', '14/02/2020', '15:45:00', walletphoto)
            )

sleevepath = os.path.join(os.getcwd(), 'images', 'sleeve.jpg')
sleevephoto = convertToBinaryData(sleevepath)
cur.execute("INSERT INTO items (item, description, occurdate, time, photo) VALUES (?, ?, ?, ?, ?)",
            ('Laptop Sleeve', 'Found at the deck', '15/02/2020', '16:00:00', sleevephoto)
            )
        

connection.commit()
connection.close()

