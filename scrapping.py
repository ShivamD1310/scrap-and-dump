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
            
            # Replace NaN values with 0
            df = df.fillna(0)
            
            # Transpose the DataFrame
            df_transposed = df.transpose()
            
            # Reset index and drop the old index column
            df_transposed.reset_index(drop=True, inplace=True)
            
            # Check for percentage values in the rows and convert to integer
            for index, row in df_transposed.iterrows():
                for col in df_transposed.columns:
                    if isinstance(row[col], str) and '%' in row[col]:
                        df_transposed.at[index, col] = row[col].replace('%', '').strip()
                        
            # Convert to numeric and handle errors (e.g., empty strings)
            df_transposed = df_transposed.apply(pd.to_numeric, errors='ignore')
            
            # Fill NaN values with 0
            df_transposed = df_transposed.fillna(0)

            for cols in df.columns:
                df[cols] = df[cols].fillna(0)
            
            # Print the DataFrame and transformed DataFrame
            print("Original DataFrame:")
            print(df)
            print('------------------------')
            df = df.fillna(0)
            print('updated df')
            print(df)
            
            #print('Transformed DataFrame:')
            #print(df_transposed)
            
            return df_transposed
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
