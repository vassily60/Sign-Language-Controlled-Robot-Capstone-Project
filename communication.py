import cv2
import numpy as np
import requests
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import time
import socket

# Raspberry Pi's IP address
raspberry_pi_ip = 'http://10.10.10.10:5000/video'
print('hi')
# # Open the video stream
cap = cv2.VideoCapture(raspberry_pi_ip)
s = socket.socket()
host = "10.10.10.10"
port = 5000
model = load_model("model_v1test.keras")

def communication():
    s.connect((host, port))
    print('hello')
    # while True:
    ret, frame = cap.read()
    # frame = cv2.resize(frame, (150,150))
    # img_array=image.load_img(frame)
    # cv2.imshow("Live feed", frame)

    img_path = "test_image.jpg"
    img_size = (150, 150)  
    img = image.load_img(img_path, target_size=img_size)
    img_array = image.img_to_array(img)

    img_array = (img_array / 127.5) - 1.0  

# Expand dimensions to match model's expected input shape (batch size of 1)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    print(prediction)
    
    message=None
    max=0
    for count, prob in enumerate(prediction[0]):
        if prob > max:
            max = prob
            message = str(count)
    print(message)


    s.send(message.encode())
    data = s.recv(1024).decode()
    print(f"Info received: {data}")


    s.close()
    
    cap.release()
    cv2.destroyAllWindows() 


if __name__ == "__main__":
    communication()


