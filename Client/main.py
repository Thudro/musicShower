import requests
import time

PC_IP = "192.168.1.1"  # Replace with your PC's local IP address
URL = f"http://{PC_IP}:5000/now-playing"

while True:
    try:
        response = requests.get(URL)
        data = response.json()
        print(f"Now Playing: {data['now_playing']}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
