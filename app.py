import os
import sqlite3
import time
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from argon2 import PasswordHasher
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import base64

# Flask app initialization
app = Flask(__name__)
app.config['DEBUG'] = True  # Enable debug mode

# AES Key Setup (for encryption, not used for JWT here)
AES_KEY = os.getenv("NOT_MY_KEY", "f54c860abc57fa0876adad69b7b4e75ea4ac2028a48b44852d9b3dd17b48b93a")  # Example AES key
AES_KEY = bytes.fromhex(AES_KEY)

# JWT Secret Key (ensure it's stored securely in a real app)
SECRET_KEY = "your_secret_key"  # You should store this securely!

# Password hasher setup
ph = PasswordHasher()

# Database connection function
def get_db_connection():
    conn = sqlite3.connect("totally_not_my_privateKeys.db")
    conn.row_factory = sqlite3.Row  # Allow column access by name
    return conn

# Initialize Flask-Limiter for Rate Limiting
limiter = Limiter(get_remote_address, app=app)

# Create tables if they don't exist
def init_db():
    cursor = get_db_connection().cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keys (
            kid TEXT PRIMARY KEY,
            key BLOB,
            iv BLOB,
            exp INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE,
            date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            success INTEGER,
            request_ip TEXT,
            request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.connection.commit()

init_db()

# Function to log authentication requests
def log_authentication(username, success):
    user_ip = request.remote_addr  # Capture the IP address of the user
    cursor = get_db_connection().cursor()
    cursor.execute(
        "INSERT INTO auth_logs (username, success, request_ip) VALUES (?, ?, ?)",
        (username, success, user_ip)  # Log the username, success status, and IP address
    )
    cursor.connection.commit()

# AES encryption key
def encrypt_private_key(private_key):
    iv = os.urandom(16)  # Generate a random IV (16 bytes for AES)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the private key to be a multiple of 16 bytes (AES block size)
    padding_length = 16 - (len(private_key) % 16)
    padded_private_key = private_key + (chr(padding_length) * padding_length).encode('utf-8')
    
    encrypted_key = encryptor.update(padded_private_key) + encryptor.finalize()
    
    # Return the encrypted key and IV (both encoded in base64 for storage)
    return base64.b64encode(encrypted_key).decode('utf-8'), base64.b64encode(iv).decode('utf-8')

def decrypt_private_key(encrypted_key, iv):
    encrypted_key = base64.b64decode(encrypted_key)
    iv = base64.b64decode(iv)
    
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_key = decryptor.update(encrypted_key) + decryptor.finalize()

    # Remove padding from the decrypted key
    padding_length = decrypted_key[-1]
    decrypted_key = decrypted_key[:-padding_length]

    return decrypted_key.decode('utf-8')

# User Registration Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400

    try:
        # Generate a secure UUIDv4 password
        password = str(uuid.uuid4())
        hashed_password = ph.hash(password)  # Hash the password using Argon2
        
        # Insert user details into the database
        cursor = get_db_connection().cursor()
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, hashed_password))
        cursor.connection.commit()

        # Return the generated password (for user to know)
        return jsonify({"password": password}), 201
    except Exception as e:
        return jsonify({"error": f"Registration failed: {e}"}), 500

# Authentication Route with JWT
@app.route('/auth', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit to 5 requests per minute
def auth():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        cursor = get_db_connection().cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "User not found"}), 404

        stored_password_hash = row[0]

        try:
            ph.verify(stored_password_hash, password)  # Argon2 password verification

            # Log authentication request
            log_authentication(username, 1)

            # Generate JWT Token
            payload = {
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({"message": "Authentication successful", "token": token}), 200
        except Exception as e:
            # Log failed authentication attempt
            log_authentication(username, 0)
            return jsonify({"error": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"error": f"Authentication failed: {e}"}), 500

# Secured Endpoint
@app.route('/secure-endpoint', methods=['GET'])
def secure_endpoint():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"error": "Token is missing!"}), 403
    
    token = token.split(" ")[1]  # Remove the "Bearer " part
    print(f"Received Token: {token}")  # Debugging output
    
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "Secure data", "user": decoded_token['username']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

# Start the Flask app
if __name__ == "__main__":
    app.run(port=8080)
