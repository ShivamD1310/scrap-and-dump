import pandas as pd
from sqlalchemy import create_engine
import os

def load_csv_to_postgres():
    # PostgreSQL connection details
    user = os.getenv('POSTGRES_USER', 'user')
    password = os.getenv('POSTGRES_PASSWORD', 'test123')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')
    database = os.getenv('POSTGRES_DB', 'task')
    
    # Create an engine instance
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    
    # Read CSV into DataFrame
    df = pd.read_csv('profit_loss.csv')
    
    # Insert data into PostgreSQL
    df.to_sql('profit_loss', engine, if_exists='replace', index=False)
    print("Data has been inserted into PostgreSQL.")

if __name__ == "__main__":
    load_csv_to_postgres()
