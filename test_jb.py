import sqlite3
import os
import time

# Connect to the SQLite database (this will create a new file if it doesn't exist)
conn = sqlite3.connect('totally_not_my_privateKeys.db')
cursor = conn.cursor()

# Create the keys table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS keys (
        kid TEXT PRIMARY KEY,
        key BLOB NOT NULL,
        iv BLOB NOT NULL,
        exp INTEGER NOT NULL
    )
''')

# Insert a test key with random data for key and iv
cursor.execute('INSERT INTO keys (kid, key, iv, exp) VALUES (?, ?, ?, ?)',
               ('goodKID', sqlite3.Binary(b'somekey'), sqlite3.Binary(b'someiv'), int(time.time()) + 3600))

# Commit changes and close the connection
conn.commit()

# Verify the data was inserted
cursor.execute("SELECT * FROM keys")
rows = cursor.fetchall()
print("Database rows:", rows)

# Close the connection
conn.close()
