import os
import requests

def main():
    # Fetch the credentials from environment variables
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    
    # Print the credentials for debugging purposes
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")
    
    # Define the login URL and payload
    login_url = 'https://www.screener.in/login/'
    payload = {
        'username': username,
        'password': password
    }
    
    # Perform the login request
    response = requests.post(login_url, data=payload)
    
    # Check the status code and response text
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

if __name__ == "__main__":
    main()
