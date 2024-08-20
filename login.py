import os
import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
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
        headers = [header.text.strip() for header in soup.select('body main section:nth-of-type(5) div:nth-of-type(3) thead th')]
        
        # Extract rows
        rows = soup.select('body main section:nth-of-type(5) div:nth-of-type(3) tbody tr')
        
        # Prepare data for DataFrame
        data = []
        for row in rows:
            cols = [col.text.strip() for col in row.find_all('td')]
            if len(cols) > 1:
                data.append(cols)
        
        # Create DataFrame
        if data:
            df = pd.DataFrame(data, columns=headers)
            return df
        else:
            print("No data to insert.")
            return None
    else:
        print(f"Failed to access Reliance page. Status Code: {response.status_code}")
        return None

def connect_to_db():
    try:
        engine = create_engine('postgresql+psycopg2://user:test123@localhost:5432/task')
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def connect_to_db():
    try:
        # Test connection
        engine = create_engine('postgresql+psycopg2://user:test123@localhost:5432/task')
        connection = engine.connect()
        print("Connection to PostgreSQL successful!")
        connection.close()
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def main():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")
    
    cookies = login(username, password)
    if cookies:
        df = scrape_profit_loss(cookies)
        if df is not None:
            print(df)
            # Save the DataFrame to PostgreSQL
            save_to_postgres(df, 'profit_loss')
        else:
            print("No DataFrame to save.")

if __name__ == "__main__":
    main()
