# %%

import cv2
import numpy as np
import requests
from tensorflow.keras.models import load_model
import time
from tensorflow.keras.preprocessing import image

# %%
# Raspberry Pi's IP address
raspberry_pi_ip = 'http://10.10.10.10:5001/video'

model = load_model("model_v1test.keras")

# Open the video strem
cap = cv2.VideoCapture(raspberry_pi_ip)

# Server endpoint to send the message back
host_url = 'http://10.10.10.10:5001/update'  # Modify this to match your server endpoint

# %%
a=0
while a<20:
    ready = input('Ready? ')
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow("Live feed", frame)

    # Resize the frame to 150x150 (if you plan to use this)
    frame = cv2.resize(frame, (150, 150))

    # Normalize the frame for model input
    img_array = (frame / 127.5) - 1.0  

    # Expand dimensions to match model's expected input shape (batch size of 1)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    print(f"Predictions: {prediction}")

    message=None
    max=0
    for count, prob in enumerate(prediction[0]):
        if prob > max:
            max = prob
            message = str(count)
    print(f"Final prediction: {message}")

    # Send the message back to the host if a valid message is detected
    if message is not None:
        response = requests.post(host_url, json={'message': message})
        if response.status_code == 200:
            print(f"Message sent to host: {message}")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    a+=1

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
