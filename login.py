import os
import requests
from bs4 import BeautifulSoup

def main():
    # Fetch the credentials from environment variables
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    # Print the credentials for debugging purposes
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")

    # Define the login URL
    login_url = 'https://www.screener.in/login/'

    # Send a GET request to the login page to obtain the CSRF token
    response = requests.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    # Define the payload
    payload = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }

    # Perform the login request
    response = requests.post(login_url, data=payload)

    # Check the status code and response text
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

if __name__ == "__main__":
    main()
