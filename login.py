import os
import requests
from bs4 import BeautifulSoup

def get_csrf_token(login_url):
    # Make a GET request to retrieve the login page
    response = requests.get(login_url)
    
    # Parse the page to find the CSRF token
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the CSRF token from the HTML (e.g., in a meta tag or input field)
    # Modify the selector based on the actual HTML structure
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    return csrf_token

def login(username, password):
    login_url = 'https://www.screener.in/login/'
    
    # Get CSRF token
    csrf_token = get_csrf_token(login_url)
    
    # Define the payload with CSRF token
    payload = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    
    # Define headers including the CSRF token
    headers = {
        'Referer': login_url,
        'X-CSRFToken': csrf_token
    }
    
    # Perform the login request
    response = requests.post(login_url, data=payload, headers=headers, cookies={'csrftoken': csrf_token})
    
    # Check the status code and response text
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

def main():
    # Fetch the credentials from environment variables
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    
    # Print the credentials for debugging purposes
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")
    
    # Perform login
    login(username, password)

if __name__ == "__main__":
    main()
