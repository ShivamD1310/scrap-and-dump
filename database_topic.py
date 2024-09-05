import pandas as pd
from sqlalchemy import create_engine
from confluent_kafka import Producer
import json

db_user = 'user'
db_password = 'test123'
db_host = '192.168.3.116'
db_port = '5432'
db_name = 'task'

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': '192.168.3.116:19092',  
}


producer = Producer(kafka_conf)


db_conn_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


engine = create_engine(db_conn_str)

# Define the query to fetch data from PostgreSQL
query = """
SELECT
    *
FROM nifty_companies;
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
    topic = 'nifty'  
    
    # Send data to Kafka
    send_to_kafka(producer, topic, df)

if __name__ == "__main__":
    main()
