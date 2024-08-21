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
            
            # print(df)
            
            # Replace any empty column names with 'column'
            #df.columns = [col if col.strip() != '' else 'year' for col in df.columns]
            #df1 = df.set_index('year')
            #print(df1)
            print('---------------------------------------------------------------------')
            df = df.replace('%','',regex=True)
            df = df.replace(',','',regex=True)
            #print(df1)
            print('---------------------------------------------------------------------')
            # print(df1.info())

            print('--------------------------')
            #print(df1.transpose())
            df['TTM'] = df['TTM'].replace('','0')
            df = df.transpose()
            df = df.reset_index()
            df.iloc[0,0]='year'
            print(df)
            df.columns = df.iloc[0]
            df = df[1:]
            print(df)
            print(df.columns)
            # df['new_col'] = range(1, len(df) + 1)






            for cols in df.columns[1:]:
                df[cols] = df[cols].astype(float)

            print('-------------------------')
            print(df)

            print(df.value_counts())
            print('-------------')

            #     df[cols] = df[cols].fillna(0)
            # print(df)
            #df.iloc[0,0] = 'year'

            # df = df.rename_axis('year').reset_index()
            # df = df.set_index('year')
            # df = df.reset_index()
            # print(df)
            # df.columns.values[0] = 'year'
            # print(df.columns)
            # print(df['index'])
            # df.rename()

            # df1['TTM'] = df1['TTM'].replace('','0')

            # for cols in df1.columns:
            #     df1[cols] = df1[cols].astype(float)

            # print(df1)
            # print('-----------------------------------------------------------------------------')
            # print(df1.info())

            # # Transpose DataFrame
            # df_transpose = df1.transpose()
            # print(df_transpose)
            # print('-----------------------------------------------------------------------------')
            # df_transpose = df_transpose.reset_index()
            # print(df_transpose)
            
            
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

def load_csv_to_postgres():
    """Load data from CSV into PostgreSQL."""
    # PostgreSQL connection details
    user = os.getenv('POSTGRES_USER', 'user')
    password = os.getenv('POSTGRES_PASSWORD', 'test123')
    host = os.getenv('POSTGRES_HOST', '192.168.0.165')  # Updated to the new IP address
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
