from flask import Flask, request, send_file, after_this_request
import cv2
import numpy as np
import pickle
from ultralytics import YOLO
from tensorflow.keras.applications.mobilenet import preprocess_input
from keras.applications import MobileNet
from werkzeug.utils import secure_filename
from flask_cors import CORS
import tempfile
import os
import warnings
from sklearn.exceptions import InconsistentVersionWarning

# Suppress the InconsistentVersionWarning (optional)
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

app = Flask(__name__)
CORS(app)

# Load the trained classifier
model_path = 'mobilenet_svm_4.pkl'  # Path to your model
with open(model_path, 'rb') as model_file:
    classifier = pickle.load(model_file)

def process_video_file(input_video_path, output_video_path):
    facemodel = YOLO('yolov8n-face.pt')  # Path to YOLO model
    base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    cap = cv2.VideoCapture(input_video_path)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use 'XVID' or 'mp4v'
    out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

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
            if isinstance(confidence_score, np.ndarray):
                confidence_score = confidence_score[0]
                
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 1)
            cv2.putText(frame, f'ID: {person_id} ({confidence_score:.2f})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Write the frame to the output video
        out.write(frame)

    cap.release()
    out.release()

@app.route('/process_video', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return "No video part", 400

    video = request.files['video']
    filename = secure_filename(video.filename)

    # Save the video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        video.save(temp_video.name)

        # Process and save the output video to another temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as output_video:
            process_video_file(temp_video.name, output_video.name)

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(temp_video.name)
                    os.remove(output_video.name)
                except Exception as e:
                    print(f"Error removing temporary files: {e}")
                return response

            return send_file(output_video.name, as_attachment=True, download_name="processed_video.mp4")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
