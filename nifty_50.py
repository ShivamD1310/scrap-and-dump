import pandas as pd
from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
import os
import numpy as np


username = 'doddamani.shivam795@gmail.com'
password = 'shivamdoddamani13'

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
    company_list=['TCS','INFY','HCLTECH','WIPRO','LTIM','TECHM','PERSISTENT','LTTS','MPHASIS','COFORGE']#,'BHARTIARTL','ICICIBANK','INFY','SBIN','HINDUNILVR','ITC','LT']
    all_company = []
    for i in company_list:
        print(i)
        reliance_url = f'https://www.screener.in/company/{i}/consolidated/'
        response = requests.get(reliance_url, cookies=cookies)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract headers
            headers = [header.text.strip() for header in soup.select('body main section:nth-of-type(5) div:nth-of-type(3) thead th')]
            #print(headers)
            # headers[0] = 'year'
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
                
                print('---------------------------------------------------------------------')
                df = df.replace('%','',regex=True)
                df = df.replace(',','',regex=True)
                #print(df1)
                print('---------------------------------------------------------------------')
                # print(df1.info())

                print('--------------------------')
                #print(df1.transpose())
                # df['TTM'] = df['TTM'].replace('','0')
                df = df.drop(df.columns[-1],axis=1)
                #print(df)
                print('-----------------------------------------------------')
                df = df.transpose()
                df = df.reset_index()
                df.iloc[0,0]='year'
                # print(df)
                df.columns = df.iloc[0]
                df = df[1:]
                # print(df)
                # print(df.columns)
                # df['new_col'] = range(1, len(df) + 1)






                for cols in df.columns[1:]:
                    df[cols] = df[cols].astype(float)
                
                cleaned_colum = []
                for cols in df.columns:
                    cleaned_col = cols.replace(' ', '_').replace('+', '').strip()
                    if cleaned_col.endswith('_'):
                        cleaned = cleaned_col.rstrip('_')+'_%'
                        cleaned_colum.append(cleaned)
                    else:    
                        cleaned_colum.append(cleaned_col)
                cleaned_colum.append('Stock')
                # print(cleaned_colum)
                
                print('-------------------------')
                df['Stock'] = i
                df.columns = cleaned_colum
                # print(df)

                # print(df.columns)
                print('-------------')

                all_company.append(df)
                # print('----------------------------------------------------------------------------------')
                # print(all_company)
                # print(type(all_company))
                
            
                #return df
            else:
                print("No data to insert.")
                return None
        else:
            print(f"Failed to access Reliance page. Status Code: {response.status_code}")
            return None
    
    if all_company:
        combined_df = pd.concat(all_company, ignore_index=True)
        print("Combined DataFrame:")
        print(combined_df)
        #combined_df.to_csv('it_companies.csv',index=False)
        return combined_df
    else:
        print("No data collected.")
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
    df = pd.read_csv('nifty_companies.csv')
    
    # Insert data into PostgreSQL
    df.to_sql('nifty_companies', engine, if_exists='replace', index=False)
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
            df.to_csv('nifty_companies.csv', index=False)
            
            # Load the CSV into PostgreSQL
            load_csv_to_postgres()
        else:
            print("No DataFrame to save.")
    else:
        print("Failed to log in.")

if __name__ == "__main__":
    main()