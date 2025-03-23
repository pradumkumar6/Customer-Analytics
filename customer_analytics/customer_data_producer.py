import json
import streamlit as st 
import time 
from  confluent_kafka import Producer

kafka_config = {
    'bootstrap.servers': 'pkc-619z3.us-east1.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'OQRJN62YJNTKLUT6',
    'sasl.password': 'MBqs6ADVQtYWS8EyDPDCPSC6jOiOUCSItUBoZ+0kQtk8K5UhXalx4FVIQBhw1o4p',
    'group.id': 'sentiment_analysis_group',
    'auto.offset.reset': 'earliest'
}

KAFKA_TOPIC  = "customer_click_data"
producer = Producer(kafka_config)

st.title("Euron Big data Custormer click Analytics")
user_id = st.number_input("user id" , min_value = 1 , max_value = 1000000 , step = 1 )
activity = st.selectbox("activity", ["view_product" ,"add_to_cart" ,"checkout" , "search" , "whishlist"])
product = st.selectbox("product" , ["Laptop" , "mobile" , "headphone" ,"smartwatch" , "camera","tablet"])

def send_event():
    event = {
        "user_id" :user_id,
        "activity" : activity,
        "product" : product,
        "timestamp" : int(time.time())
    }
    
    producer.produce(KAFKA_TOPIC,key=str(user_id) , value = json.dumps(event))
    producer.flush()
    st.success(f"send this event:{event}")
    
if st.button("send data"):
    send_event()


