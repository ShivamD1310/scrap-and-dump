import os
import requests

def main():
    # Fetch the credentials from environment variables
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    # Print the credentials for debugging purposes
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")

    # Define the login URL
    login_url = 'https://www.screener.in/login/'

    # Create a session object
    session = requests.Session()

    # Define the login payload with credentials from environment variables
    login_payload = {
        'username': username,
        'password': password
    }

    # Perform the login by sending a POST request
    login_response = session.post(login_url, data=login_payload)

    # Check if the login was successful
    if login_response.ok:
        print("Login successful!")
    else:
        print("Login failed.")
        print(f"Status Code: {login_response.status_code}")
        print(f"Response Text: {login_response.text[:500]}")  # Print first 500 characters

if __name__ == "__main__":
    main()
