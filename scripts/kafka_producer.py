import json
import random
import time
from confluent_kafka import Producer

# Kafka configuration
kafka_config = {
    'bootstrap.servers': 'localhost:9092'  # Kafka broker address
}

# Create a Kafka producer
producer = Producer(kafka_config)

# Function to deliver a callback for logging message success/failure
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Simulate clickstream data
def simulate_clickstream_data():
    events = ["click", "view", "purchase", "add_to_cart", "search"]
    products = ["product_1", "product_2", "product_3", "product_4", "product_5"]

    return {
        "user_id": f"user_{random.randint(1, 100)}",
        "event_type": random.choice(events),
        "product_id": random.choice(products),
        "timestamp": time.time()
    }

# Continuously send simulated data to Kafka
while True:
    clickstream_event = simulate_clickstream_data()
    producer.produce(
        "clickstream-data",
        key=str(clickstream_event["user_id"]),
        value=json.dumps(clickstream_event),
        callback=delivery_report
    )
    producer.flush()  # Ensure the message is sent
    time.sleep(1)  # Send data every second
