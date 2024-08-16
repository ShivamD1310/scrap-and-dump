import os
import requests
from bs4 import BeautifulSoup

def get_csrf_token(login_url):
    response = requests.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return csrf_token

def login(username, password):
    login_url = 'https://www.screener.in/login/'
    csrf_token = get_csrf_token(login_url)
    
    payload = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    
    headers = {
        'Referer': login_url,
        'X-CSRFToken': csrf_token
    }
    
    session = requests.Session()
    response = session.post(login_url, data=payload, headers=headers, cookies={'csrftoken': csrf_token})
    
    if "Core Watchlist feed" in response.text:
        print("Login successful!")
    else:
        print("Login failed.")
        return None
    
    return session

def access_reliance_page(session):
    reliance_url = 'https://www.screener.in/company/RELIANCE/consolidated/'
    response = session.get(reliance_url)
    
    # Print status code and first 500 characters of response text
    print(f"Status Code: {response.status_code}")
    print("Response Text (first 500 characters):")
    print(response.text[:500])  # Print the first 500 characters for brevity

def main():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")
    
    session = login(username, password)
    
    if session:
        access_reliance_page(session)

if __name__ == "__main__":
    main()
