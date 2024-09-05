import requests
import pandas as pd
from sqlalchemy import create_engine
import os

def fetch_job_salary_data():
    url = "https://job-salary-data.p.rapidapi.com/job-salary"
    querystring = {"job_title": "nodejs developer", "location": "new york, usa", "radius": "200"}
    headers = {
        "x-rapidapi-key": "514c978525mshc98e8dea4f6af6fp107651jsnb4d358bd5e56",
        "x-rapidapi-host": "job-salary-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data.get('data', [])

def save_to_csv(df):
    df.to_csv('us_salaries.csv', index=False)
    print("Data has been saved to 'us_salaries.csv'.")

def load_csv_to_postgres():
    user = os.getenv('POSTGRES_USER', 'user')
    password = os.getenv('POSTGRES_PASSWORD', 'test123')
    host = os.getenv('POSTGRES_HOST', '192.168.3.116')
    port = os.getenv('POSTGRES_PORT', '5432')
    database = os.getenv('POSTGRES_DB', 'task')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    
    df = pd.read_csv('us_salaries.csv')
    df.to_sql('us_salaries', engine, if_exists='replace', index=False)
    print("Data has been inserted into PostgreSQL.")

def main():
    data_list = fetch_job_salary_data()
    
    df = pd.DataFrame(data_list)
    print(df)
    
    save_to_csv(df)

    load_csv_to_postgres()

if __name__ == "__main__":
    main()
