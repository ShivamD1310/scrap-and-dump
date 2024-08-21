import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from bs4 import BeautifulSoup

def login(username, password):
    """Log in to the website and return cookies."""
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
    """Scrape profit and loss data from the website and return as a DataFrame."""
    reliance_url = 'https://www.screener.in/company/RELIANCE/consolidated/'
    response = requests.get(reliance_url, cookies=cookies)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract headers
        headers = [header.text.strip() for header in soup.select('body main section:nth-of-type(5) div:nth-of-type(3) thead th')]
        headers[0] = 'year'
        
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
            
            # Clean data: remove '%', ',' and handle empty strings
            df = df.replace('%', '', regex=True)
            df = df.replace(',', '', regex=True)
            df['TTM'] = df['TTM'].replace('', '0')
            
            # Transpose DataFrame to match the desired format
            df = df.transpose()
            df.columns = df.iloc[0]
            df = df[1:]
            
            # Convert columns to float
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Fill NaN values with 0
            df = df.fillna(0)
            
            print("Processed DataFrame:")
            print(df)
            print(df.columns)
            
            return df
        else:
            print("No data to insert.")
            return None
    else:
        print(f"Failed to access Reliance page. Status Code: {response.status_code}")
        return None

def load_csv_to_postgres():
    """Load data from CSV into PostgreSQL."""
    # PostgreSQL connection details
    user = os.getenv('POSTGRES_USER', 'user')
    password = os.getenv('POSTGRES_PASSWORD', 'test123')
    host = os.getenv('POSTGRES_HOST', '192.168.3.116')  # Updated to the new IP address
    port = os.getenv('POSTGRES_PORT', '5432')
    database = os.getenv('POSTGRES_DB', 'task')
    
    # Create an engine instance
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    
    # Read CSV into DataFrame
    df = pd.read_csv('profit_loss.csv')
    
    # Insert data into PostgreSQL
    df.to_sql('profit_loss', engine, if_exists='replace', index=False)
    print("Data has been inserted into PostgreSQL.")

def main():
    """Main function to execute the workflow."""
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    
    cookies = login(username, password)
    if cookies:
        df = scrape_profit_loss(cookies)
        if df is not None:
            # Save the DataFrame to CSV
            df.to_csv('profit_loss.csv', index=False)
            
            # Load the CSV into PostgreSQL
            load_csv_to_postgres()
        else:
            print("No DataFrame to save.")
    else:
        print("Failed to log in.")

if __name__ == "__main__":
    main()
