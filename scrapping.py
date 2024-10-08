import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import numpy as np

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
            
            # Replace any empty column names with 'column'
            df.columns = [col if col.strip() != '' else 'year' for col in df.columns]
            #df1 = df.set_index('year')
            #print(df1)
            print('---------------------------------------------------------------------')
            df1 = df1.replace('%','',regex=True)
            df1 = df1.replace(',','',regex=True)
            print(df1)
            print('---------------------------------------------------------------------')
            print(df1.info())

            df1['TTM'] = df1['TTM'].replace('','0')

            for cols in df1.columns:
                df1[cols] = df1[cols].astype(float)

            print(df1)
            print('-----------------------------------------------------------------------------')
            print(df1.info())

            # Transpose DataFrame
            df_transpose = df1.transpose()
            print(df_transpose)
            print('-----------------------------------------------------------------------------')
            df_transpose = df_transpose.reset_index()
            print(df_transpose)
            
            
            # Fill NaN values with 0
            #df_transpose = df_transpose.fillna(0)
            
            
            print('----------------------------------------------------------------------------------')
            #print(df_transpose.info())
            
            return df
        else:
            print("No data to insert.")
            return None
    else:
        print(f"Failed to access Reliance page. Status Code: {response.status_code}")
        return None

def main():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    
    cookies = login(username, password)
    if cookies:
        scrape_profit_loss(cookies)

if __name__ == "__main__":
    main()
