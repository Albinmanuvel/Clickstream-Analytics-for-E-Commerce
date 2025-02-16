import random
import time
import uuid
import json
from datetime import datetime

# Define possible user actions
ACTIONS = ["search", "view", "add_to_cart", "purchase"]

# List of sample product IDs
PRODUCT_IDS = [f"product_{i}" for i in range(1, 101)]

# Simulate a clickstream event
def generate_event(user_id, session_id):
    action = random.choice(ACTIONS)
    event = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "session_id": session_id,
        "event_type": action,
    }

    # Add product_id for actions that involve products
    if action in ["view", "add_to_cart", "purchase"]:
        event["product_id"] = random.choice(PRODUCT_IDS)

    return event

# Generate and print events in real-time
def simulate_clickstream(num_users=10, delay=1):
    print("Simulating clickstream data...")
    user_sessions = {f"user_{i}": str(uuid.uuid4()) for i in range(1, num_users + 1)}

    while True:
        for user_id, session_id in user_sessions.items():
            event = generate_event(user_id, session_id)
            print(json.dumps(event))
            time.sleep(delay)  # Delay between events (in seconds)

if __name__ == "__main__":
    simulate_clickstream()
