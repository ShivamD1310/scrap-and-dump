import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

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
            df.columns = [col if col.strip() != '' else 'column' for col in df.columns]
            
            # List of columns that may contain percentages
            percentage_columns = ['OPM', 'Tax', 'Dividend Payout']
            
            # Remove '%' sign from specific columns and convert to numeric
            for col in df.columns:
                if col in percentage_columns:
                    df[col] = df[col].astype(str).replace('%', '', regex=True).str.strip()
                
                # Convert the remaining columns to numeric (except percentage columns)
                if col not in percentage_columns:
                    df[col] = df[col].astype(str).replace({',': '', '\$': ''}, regex=True).str.strip()
            
            # Convert columns to numeric where possible
            df = df.apply(pd.to_numeric, errors='ignore')
            
            # Fill NaN values with 0
            df = df.fillna(0)
            
            # Calculate the mean for each row
            df_mean = df.mean(axis=1)

            # Print the DataFrame and the calculated means
            print("Original DataFrame:")
            print(df)
            print('------------------------')
            print('Row-wise Mean:')
            print(df_mean)
            
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
