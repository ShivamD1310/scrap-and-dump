import os
import requests
import pandas as pd
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
        
        # Extract headers
        header_elements = soup.select_one('body main section:nth-of-type(5) div:nth-of-type(3) thead')
        headers = [th.text.strip() for th in header_elements.find_all('th')] if header_elements else []
        
        # Extract rows
        rows = soup.select_one('body main section:nth-of-type(5) div:nth-of-type(3)').find_all('tr')
        data_rows = []
        
        for row in rows:
            cols = [col.text.strip() for col in row.find_all('td')]
            if cols:  # Add non-empty rows
                data_rows.append(cols)
        
        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(data_rows, columns=headers)
        df.to_csv('profit_loss.csv', index=False, encoding='utf-8')
        
        print("Data has been written to profit_loss.csv")
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
