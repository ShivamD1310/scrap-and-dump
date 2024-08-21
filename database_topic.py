import pandas as pd
from sqlalchemy import create_engine
from confluent_kafka import Producer
import json

# PostgreSQL connection parameters
db_user = 'user'
db_password = 'test123'
db_host = '192.168.3.116'
db_port = '5432'
db_name = 'task'

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': '192.168.3.116:19092',  # Replace with your Kafka broker address
}

# Create Kafka producer
producer = Producer(kafka_conf)

# PostgreSQL connection string
db_conn_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create a database engine
engine = create_engine(db_conn_str)

# Define the query to fetch data from PostgreSQL
query = """
SELECT
    "column", "Mar 2013", "Mar 2014", "Mar 2015", "Mar 2016", "Mar 2017", "Mar 2018", "Mar 2019",
    "Mar 2020", "Mar 2021", "Mar 2022", "Mar 2023", "Mar 2024", "TTM"
FROM profit_loss;
"""

def send_to_kafka(producer, topic, df):
    for index, row in df.iterrows():
        # Convert row to a JSON string
        row_str = row.to_json()
        
        # Produce message
        producer.produce(topic, key=str(index), value=row_str)
        producer.flush()
        print(f"Sent: {row_str}")

def main():
    # Fetch data from PostgreSQL
    df = pd.read_sql(query, engine)
    
    # Kafka topic name
    topic = 'task7'  # Replace with your Kafka topic name
    
    # Send data to Kafka
    send_to_kafka(producer, topic, df)

if __name__ == "__main__":
    main()
