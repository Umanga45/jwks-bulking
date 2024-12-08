import os

# Generate a random AES key of 256 bits (32 bytes)
key = os.urandom(32)  # 256 bits = 32 bytes
print(key.hex())  # Output the key in hexadecimal format
