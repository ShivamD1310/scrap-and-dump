import requests
import pandas as pd
from sqlalchemy import create_engine
import os

def reading_data():
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/historical_stats"
    stock_name = "ITC"
    stats = "yoy_results"

    querystring = {f"stock_name":{stock_name},"stats":{stats}}

    headers = {
        "x-rapidapi-key": "514c978525mshc98e8dea4f6af6fp107651jsnb4d358bd5e56",
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    df = pd.DataFrame(data)


    df = df.reset_index()
    df = df.rename(columns={'index': 'Year'})

    cleaned_colums = []
    for i in df.columns:
        cols = i.replace(' ','_')
        cleaned_colums.append(cols)

    df.columns = cleaned_colums
    #print(cleaned_colums)
    #print(len(df))
    df = df.iloc[:len(df)-1]
    df['Stock'] = stock_name
    #print(df)
    # print('-------------------------------------------------------------------------------------')
    # print(df.info())
    return df

def save_to_csv(df):
    df.to_csv('itc.csv', index=False)
    print("Data has been saved to 'itc.csv'.")

def load_csv_to_postgres():
    user = os.getenv('POSTGRES_USER', 'user')
    password = os.getenv('POSTGRES_PASSWORD', 'test123')
    host = os.getenv('POSTGRES_HOST', '192.168.3.116')
    port = os.getenv('POSTGRES_PORT', '5432')
    database = os.getenv('POSTGRES_DB', 'task')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    
    df = pd.read_csv('itc.csv')
    df.to_sql('us_salaries', engine, if_exists='replace', index=False)
    print("Data has been inserted into PostgreSQL.")

def main():
    df = reading_data()
    
    if not df.empty:
        print(df)
        save_to_csv(df)
        load_csv_to_postgres()

if __name__ == "__main__":
    main()
