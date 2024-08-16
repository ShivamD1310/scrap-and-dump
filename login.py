import os
import requests
from bs4 import BeautifulSoup

def login(username, password):
    login_url = 'https://www.screener.in/login/'
    response = requests.get(login_url)
    csrf_token = BeautifulSoup(response.text, 'html.parser').find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    payload = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    headers = {
        'Referer': login_url,
        'X-CSRFToken': csrf_token
    }
    response = requests.post(login_url, data=payload, headers=headers, cookies={'csrftoken': csrf_token})
    return response.cookies if response.status_code == 200 else None

def scrape_profit_loss(cookies):
    reliance_url = 'https://www.screener.in/company/RELIANCE/consolidated/'
    response = requests.get(reliance_url, cookies=cookies)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        headers = [th.text.strip() for th in soup.select('table thead tr th')]
        print("Headers:", headers)
        
        rows = soup.select_one('body main section:nth-of-type(5) div:nth-of-type(3)').find_all('tr')
        
        for row in rows:
            cols = [col.text.strip() for col in row.find_all('td')]
            print('\t'.join(cols))  # Print the row data separated by tabs
    else:
        print(f"Failed to access Reliance page. Status Code: {response.status_code}")

def main():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")
    
    cookies = login(username, password)
    if cookies:
        scrape_profit_loss(cookies)

if __name__ == "__main__":
    main()
