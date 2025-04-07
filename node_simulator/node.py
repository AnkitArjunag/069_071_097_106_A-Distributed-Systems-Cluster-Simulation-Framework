import os
import time
import requests

API_SERVER_URL = os.environ.get("API_SERVER_URL", "http://localhost:5000")
NODE_ID = os.environ.get("NODE_ID")

def send_heartbeat():
    while True:
        try:
            requests.post(f"{API_SERVER_URL}/heartbeat", json={"node_id": NODE_ID})
        except Exception as e:
            print(f"Heartbeat failed: {e}")
        time.sleep(5)

if __name__ == "__main__":
    send_heartbeat()
