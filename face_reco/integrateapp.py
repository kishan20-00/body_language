import os
import cv2
import pickle
import torch
import numpy as np
from flask import Flask, request, jsonify, send_file
from keras.applications.mobilenet import preprocess_input
from keras.applications import MobileNet
from ultralytics import YOLO
from tensorflow.keras.models import load_model
from PIL import Image
import matplotlib.pyplot as plt
from rembg import remove
from werkzeug.utils import secure_filename
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load models
model_path = 'mobilenet_svm_4.pkl'
with open(model_path, 'rb') as model_file:
    classifier = pickle.load(model_file)

facemodel = YOLO('yolov8n-face.pt')
base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
person_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
gait_model = load_model('resnet50_model.h5')

def bg_subtract_image(image):
    input_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    output_image = remove(input_image)
    output_image_cv = np.array(output_image)
    output_image_cv = cv2.cvtColor(output_image_cv, cv2.COLOR_RGB2BGR)
    return output_image_cv

def silhouette_extraction(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    return thresh

def crop_and_center_silhouette(binary_image):
    padded_image = cv2.copyMakeBorder(binary_image, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=0)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("Warning: No contours found.")
        return None

    contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(contour)
    max_dim = max(w, h)
    square_image = np.zeros((max_dim, max_dim), dtype=np.uint8)
    start_x = (max_dim - w) // 2
    start_y = (max_dim - h) // 2
    square_image[start_y:start_y+h, start_x:start_x+w] = binary_image[y:y+h, x:x+w]
    resized_image = cv2.resize(square_image, (128, 128))
    return resized_image

def save_image(image, path):
    if image is not None:
        cv2.imwrite(path, image)
    else:
        print("No image to save.")

def recognize_faces_from_video(video_path, output_path, expand_ratio=0.3):
    cap = cv2.VideoCapture(video_path)
    os.makedirs(output_path, exist_ok=True)
    frame_count = 0
    track_id_counter = 0
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create a VideoWriter object
    output_video_path = os.path.join(output_path, 'output_video.mp4')
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        face_result = facemodel.predict(frame, conf=0.4)
        detected_faces = []

        for info in face_result:
            parameters = info.boxes
            for box in parameters:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                width = x2 - x1
                height = y2 - y1
                x1 = int(x1 - expand_ratio * width)
                y1 = int(y1 - expand_ratio * height)
                x2 = int(x2 + expand_ratio * width)
                y2 = int(y2 + expand_ratio * height)

                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(frame.shape[1], x2)
                y2 = min(frame.shape[0], y2)

                detected_faces.append((x1, y1, x2, y2, box.conf[0]))

        for bbox in detected_faces:
            x1, y1, x2, y2, confidence = bbox
            face_crop = frame[y1:y2, x1:x2]
            face_resized = cv2.resize(face_crop, (224, 224))
            face_resized = np.expand_dims(face_resized, axis=0)
            face_resized = preprocess_input(face_resized)

            face_features = base_model.predict(face_resized)
            face_features_flat = np.reshape(face_features, (1, -1))

            person_id = classifier.predict(face_features_flat)[0]

            if confidence < 0.4:
                results = person_model(frame)
                persons = results.pandas().xyxy[0]

                for _, row in persons.iterrows():
                    x1_person, y1_person, x2_person, y2_person, conf_person, _ = row
                    x1_person, y1_person, x2_person, y2_person = int(x1_person), int(y1_person), int(x2_person), int(y2_person)

                    person_crop = frame[y1_person:y2_person, x1_person:x2_person]
                    bg_subtracted_person = bg_subtract_image(person_crop)
                    silhouette = silhouette_extraction(bg_subtracted_person)
                    centered_silhouette = crop_and_center_silhouette(silhouette)

                    if centered_silhouette is not None:
                        person_filename = os.path.join(output_path, f'person_{track_id_counter}.png')
                        save_image(centered_silhouette, person_filename)

                        asi_image = np.expand_dims(centered_silhouette, axis=(0, -1))
                        gait_prediction = gait_model.predict(asi_image)
                        class_index = np.argmax(gait_prediction)
                        confidence = gait_prediction[0][class_index]

                        print(f"Gait prediction for {person_filename}: Class {class_index} with confidence {confidence:.2f}")

                        plt.imshow(centered_silhouette, cmap='gray')
                        plt.title(f"Class {class_index} with confidence {confidence:.2f}")
                        plt.show()

                    cv2.rectangle(frame, (x1_person, y1_person), (x2_person, y2_person), (255, 0, 0), 2)
                    cv2.putText(frame, f'Person', (x1_person, y1_person - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    track_id_counter += 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f'ID: {person_id}'
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        out.write(frame)  # Write the processed frame to the output video
        frame_count += 1

    cap.release()
    out.release()  # Release the VideoWriter object

    return output_video_path

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No selected video file"}), 400

    filename = secure_filename(video_file.filename)
    video_path = os.path.join('uploads', filename)
    output_path = os.path.join('output', os.path.splitext(filename)[0])
    
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    video_file.save(video_path)
    
    output_video_path = recognize_faces_from_video(video_path, output_path)
    
    return send_file(output_video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
