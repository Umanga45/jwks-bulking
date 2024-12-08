import requests

# The JWT token you received after authentication
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVuaXF1ZV90ZXN0X3VzZXJfZDdkY2RkZGUtN2JjZS00MWEyLWFjZTktODdkMjdkYTI4ODAzIiwiZXhwIjoxNzMzNjQyNDM0fQ.QlpIFPRdM0WOlgjR06gdLEiLjUz40bJ-p1FXaIiAEwA"  # Replace this with the JWT token you received

# Authorization header with Bearer token
headers = {
    "Authorization": f"Bearer {jwt_token}"
}

# Make a GET request to the secured endpoint
response = requests.get("http://127.0.0.1:8080/secure-endpoint", headers=headers)

# Check the response
if response.status_code == 200:
    print("Secure data:", response.json())  # Successfully received the secure data
else:
    print("Error:", response.json())  # Handle error response
