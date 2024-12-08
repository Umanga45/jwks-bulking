import sqlite3
import os

# Connect to the SQLite database
conn = sqlite3.connect('totally_not_my_privateKeys.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS keys (
    kid TEXT PRIMARY KEY,
    key BLOB NOT NULL,
    iv BLOB NOT NULL,
    exp INTEGER NOT NULL
)
''')

# Generate a new key and IV for testing
kid = 'goodKID_' + str(os.urandom(4).hex())  # Unique kid each time
key = os.urandom(32)  # Random 32-byte key
iv = os.urandom(16)   # Random 16-byte IV
exp_time = 1733562825  # Example expiration time

# Insert a new row into the keys table
cursor.execute('INSERT INTO keys (kid, key, iv, exp) VALUES (?, ?, ?, ?)', 
               (kid, key, iv, exp_time))

# Commit the transaction
conn.commit()

# Query and print the inserted rows to confirm
cursor.execute('SELECT * FROM keys')
rows = cursor.fetchall()
print("Database rows:", rows)

# Close the connection
conn.close()
