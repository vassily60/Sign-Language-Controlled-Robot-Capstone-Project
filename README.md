# Sign-Language-Controlled-Robot-Capstone-Project
This repository contains the files produced towards my capstone project, creating a robot controlled by sign language.

The notebook main_client.ipynb is the script to run on your nearby laptop and main_server.py is meant to run on the raspberry pi controlling the GoPiGo robot. First run the server script to open the communication port and then run the client script from a local laptop to establish the connection.
The notebook fusion_model.ipynb contains the code for the fusion model with the pre trained model vgg16 and denseNet201. You will need to download the trained model to run main_client.ipynb as it uses the model to predict the image sent.
