# import requests

# url = "https://indian-stock-exchange-api2.p.rapidapi.com/historical_data"

# querystring = {"stock_name":"tcs","period":"6m","filter":"ohlc"}

# headers = {
# 	"x-rapidapi-key": "514c978525mshc98e8dea4f6af6fp107651jsnb4d358bd5e56",
# 	"x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())


# import requests
# url = 'https://api.polygon.io/v2/aggs/ticker/TCS/range/1/day/2024-08-01/2024-09-06?adjusted=true&sort=asc&apiKey=3VvRdrCzKkRpdxsw0jQd0C8KoicQd9lg'

# response = requests.get(url)
# print(response.json())


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
    # print(df)
    # print('-------------------------------------------------------------------------------------')
    # print(df.info())

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

reading_data()
load_csv_to_postgres()