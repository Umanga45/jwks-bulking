# jwks-server-bulking

This repository implements a JSON Web Key Set (JWKS) server with functionality for managing and storing cryptographic keys securely. The server supports endpoints for authentication, key management, and providing JWKS in a secure manner. Features include user authentication (users can register, authenticate, and generate JWT tokens), JWKS endpoints (provides a JWKS endpoint (/.well-known/jwks.json) for clients to fetch the public keys used for JWT validation), key management (supports generating, storing, and deleting keys from the database), and rate limiting (uses Flask-Limiter to limit the rate of requests to prevent abuse).
Setup and Installation
Prerequisites
•	Python 3.x
•	SQLite database (local file-based)
Installation
1.	Clone the repository:
git clone https://github.com/Umanga45/jwks-bulking.git
cd jwks-bulking
2.	Install dependencies:
pip install -r requirements.txt
3.	Set up the database (if not already set up):
python app.py # This initializes the database
Running the Application
1.	Start the Flask application:
python app.py
2.	The server will run locally on port 8080. You can access the API endpoints at http://127.0.0.1:8080.
Available Endpoints
•	POST /register: Registers a new user.
Body: {"username": "your_username", "email": "your_email"}
Response: Returns a generated password.
•	POST /auth: Authenticates a user and generates a JWT token.
Body: {"username": "your_username", "password": "your_password"}
Response: Returns a JWT token.
•	GET /.well-known/jwks.json: Returns the JSON Web Key Set (JWKS) for key validation.
•	GET /secure-endpoint: A secured endpoint that requires a valid JWT token for access.
Tests
The repository includes a test suite using pytest. To run the tests:
1.	Ensure you have the required dependencies installed:
pip install -r requirements.txt
2.	Run the tests with coverage:
python -m pytest --cov=app --cov-report term-missing
This will run the test suite and show the coverage report.




