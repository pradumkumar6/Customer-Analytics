from confluent_kafka import Consumer
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
from datetime import datetime
import logging

# Kafka Configuration
kafka_config = {
    'bootstrap.servers': 'pkc-619z3.us-east1.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'OQRJN62YJNTKLUT6',
    'sasl.password': 'MBqs6ADVQtYWS8EyDPDCPSC6jOiOUCSItUBoZ+0kQtk8K5UhXalx4FVIQBhw1o4p',
    'group.id': 'sentiment_analysis_group',
    'auto.offset.reset': 'earliest'
}

KAFKA_TOPIC = "customer_click_data"

# MongoDB Configuration
uri = "mongodb+srv://pradumkumar0612:7U1D94HdvSi4lGIC@cluster0.lg8iw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
def connect_mongo():
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client

# Process Kafka messages
def process_message():
    consumer = Consumer(kafka_config)
    consumer.subscribe([KAFKA_TOPIC])

    mongo_client = connect_mongo()
    db = mongo_client["customer_click_behaviour"]  # ✅ Fixed typo in DB name
    event_collection = db["click_data"]

    try:
        while True:
            msg = consumer.poll(1.0)
            
            if msg is None:
                continue
            if msg.error():
                print(f"Kafka error: {msg.error()}")
                continue
            
            try:
                value = json.loads(msg.value().decode('utf-8'))

                # ✅ Convert Unix timestamp to datetime before inserting
                if 'timestamp' in value:
                    value['timestamp'] = datetime.fromtimestamp(value['timestamp'])

                # Add Kafka metadata
                value["kafka_metadata"] = {
                    'topic': msg.topic(),
                    "partition": msg.partition(),
                    "offset": msg.offset(),
                    "processed_at": datetime.now().isoformat()
                }

                # Insert into MongoDB
                result = event_collection.insert_one(value)
                print("Inserted:", result.inserted_id)

            except Exception as e:
                print("Insertion error:", e)

    except Exception as e:
        print("Consumer error:", e)

if __name__ == "__main__":
    process_message()
