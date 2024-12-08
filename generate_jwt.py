import jwt
import datetime
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Step 1: Generate an RSA private key (you should already have a private key)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Step 2: Serialize the private key to PEM format (you may already have this in your app)
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Step 3: Define JWT payload (user data)
payload = {
    "sub": "username",  # Subject (typically user identifier)
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiration time (1 hour from now)
}

# Step 4: Sign the JWT using the private key and RS256 algorithm
token = jwt.encode(payload, private_pem, algorithm="RS256")

# Print the generated JWT
print("Generated JWT:", token)
