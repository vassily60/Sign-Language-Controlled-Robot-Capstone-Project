import requests
import json

# Set the Raspberry Pi's IP address and port
raspberry_pi_ip = "http://10.10.10.10:5001"

# Example function to move the robot forward
def move_robot(direction, speed):
    url = f"{raspberry_pi_ip}/move"
    data = {
        "direction": direction,
        "speed": speed
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Robot is moving {direction} at speed {speed}.")
    else:
        print("Error:", response.json())

# Example function to stop the robot
def stop_robot():
    url = f"{raspberry_pi_ip}/stop"
    response = requests.post(url)
    if response.status_code == 200:
        print("Robot stopped.")
    else:
        print("Error:", response.json())

# Use the functions to control the robot
move_robot("forward", 200)
move_robot("backward", 150)
stop_robot()
