from flask import Flask, request, Response
import cv2
import os
import io
import pickle
from ultralytics import YOLO
import tensorflow
from tensorflow.keras.applications.mobilenet import preprocess_input
import numpy as np
from keras.applications import MobileNet
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the trained classifier
model_path = 'mobilenet_svm_4.pkl'  # Path to your model
with open(model_path, 'rb') as model_file:
    classifier = pickle.load(model_file)

def generate_frames(video_stream):
    facemodel = YOLO('yolov8n-face.pt')  # Path to YOLO model
    base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    cap = cv2.VideoCapture(video_stream)
    trackers = {}
    track_id_counter = 0  # Counter for assigning unique track IDs

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform face detection using YOLOv8
        face_result = facemodel.predict(frame, conf=0.4)
        detected_faces = []

        for info in face_result:
            parameters = info.boxes
            for box in parameters:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Increase the size of the bounding box
                width = x2 - x1
                height = y2 - y1
                x1 = int(x1 - 0.3 * width)
                y1 = int(y1 - 0.3 * height)
                x2 = int(x2 + 0.3 * width)
                y2 = int(y2 + 0.3 * height)

                # Ensure the expanded coordinates are within the frame boundaries
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(frame.shape[1], x2)
                y2 = min(frame.shape[0], y2)

                detected_faces.append((x1, y1, x2, y2))

        # Process the detected faces as in your model
        for bbox in detected_faces:
            x1, y1, x2, y2 = bbox
            face_crop = frame[y1:y2, x1:x2]
            face_resized = cv2.resize(face_crop, (224, 224))
            face_resized = np.expand_dims(face_resized, axis=0)
            face_resized = preprocess_input(face_resized)

            face_features = base_model.predict(face_resized)
            face_features_flat = np.reshape(face_features, (1, -1))

            person_id = classifier.predict(face_features_flat)[0]
            confidence_score = classifier.decision_function(face_features_flat)[0]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 1)
            cv2.putText(frame, f'ID: {person_id} ({confidence_score[0]:.2f})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Encode the frame to bytes and yield as a response
        ret, buffer = cv2.imencode('.mp4', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: video/mp4\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/process_video', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return "No video part", 400

    video = request.files['video']
    filename = secure_filename(video.filename)

    # Read the video stream
    video_stream = io.BytesIO(video.read())

    # Generate and return the processed video frames
    return Response(generate_frames(video_stream), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
