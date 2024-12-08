from invoke import task
import requests
import uuid  # Ensure uuid module is imported

# Task to register a new user
@task
def register_user(c):
    url = "http://127.0.0.1:8080/register"
    unique_username = f"unique_test_user_{uuid.uuid4()}"  # Ensure unique username with UUID
    data = {
        "username": unique_username,  # Unique username for testing
        "email": f"{unique_username}@example.com"  # Unique email for testing
    }

    # Send POST request to register the user
    response = requests.post(url, json=data)

    # Check if registration is successful
    if response.status_code == 201:
        print(f"Registration successful: {response.json()}")
        # Save the password returned from the response
        password = response.json().get("password")
        print(f"Password generated: {password}")
        
        # Log the username that was used to register the user for debugging
        print(f"Username used: {unique_username}")
        
        # You can save the username and password to a text file (or environment variable) for later use in auth-user
        with open('user_info.txt', 'w') as file:
            file.write(f"Username: {unique_username}\n")
            file.write(f"Password: {password}\n")
        
        return unique_username, password
    else:
        print(f"Registration failed. Status code: {response.status_code}, Error: {response.text}")
        return None, None

# Task to authenticate the user
@task
def auth_user(c):
    # Read the username and password from the file where it was saved during registration
    try:
        with open('user_info.txt', 'r') as file:
            user_info = file.readlines()
            username = user_info[0].strip().split(": ")[1]
            password = user_info[1].strip().split(": ")[1]
            print(f"Using username: {username} and password: {password}")
    except FileNotFoundError:
        print("No user information found. Please register the user first.")
        return

    # Send POST request to authenticate the user
    url = "http://127.0.0.1:8080/auth"
    data = {
        "username": username,  # Dynamically use the correct username
        "password": password    # Dynamically use the correct password
    }

    response = requests.post(url, json=data)

    # Check if authentication is successful
    if response.status_code == 200:
        print("Authentication successful:", response.json())
    else:
        print(f"Authentication failed. Status code: {response.status_code}, Error: {response.text}")
