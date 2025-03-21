from flask import Flask, Response, request, jsonify
import cv2
import time
import easygopigo3 as easy

# Instance of the robot
my_gopigo = easy.EasyGoPiGo3()

app = Flask(__name__)

# Open video stream
cap = cv2.VideoCapture(0) 

# Define video size and output file for saving the video
frame_width = 150
frame_height = 150
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Output video file
output_filename = 'output_video.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame to a video file
        out.write(frame)

        # Encode the frame to JPEG format for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break

        # Convert to byte format and return the frame for streaming
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Endpoint to receive the message
@app.route('/update', methods=['POST'])
def update_message():
    # Get JSON data
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid request"})

    message = str(data['message'])
    print(f"Received message: {message}")

    # Movement logic
    if message == '0':
        print("Turning -90 degrees and moving forward 10 inches")
        my_gopigo.turn_degrees(-90)
        my_gopigo.drive_cm(10)

    elif message == '1':
        print("Moving forward 10 inches")
        my_gopigo.drive_cm(10)

    elif message == '2':
        print("Turning 90 degrees and moving forward 10 inches")
        my_gopigo.turn_degrees(90)
        my_gopigo.drive_cm(10)

    elif message == '3':
        print("Moving backward 10 inches")
        my_gopigo.turn_degrees(180)
        my_gopigo.drive_cm(10)

    else:
        print("Unknown command received")
        return jsonify({"error": "Invalid command"})

    return jsonify({"message": message, "status": "success"}), 200

if __name__ == '__main__':
    # Run the Flask server on the desired IP and port
    app.run(host='10.10.10.10', port=5001, threaded=True)

