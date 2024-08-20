import pandas as pd
from sqlalchemy import create_engine
from confluent_kafka import Producer
import json

# PostgreSQL connection parameters
db_user = 'user'
db_password = 'test123'
db_host = 'localhost'
db_port = '5432'
db_name = 'task'

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': 'localhost:19092',  # Replace with your Kafka broker address
}

# Create Kafka producer
producer = Producer(kafka_conf)

# PostgreSQL connection string
db_conn_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create a database engine
engine = create_engine(db_conn_str)

# Define the query to fetch data from PostgreSQL
query = 'SELECT * FROM profit_loss;'  # Replace with your actual table name

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
