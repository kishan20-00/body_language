from flask import Flask, request, jsonify, send_file
import os
import cv2
import numpy as np
import pickle
import tensorflow
from ultralytics import YOLO
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.applications.mobilenet import preprocess_input

app = Flask(__name__)

# Load the trained classifier
model_path = 'mobilenet_svm_4.pkl'  # Update with your model path
with open(model_path, 'rb') as model_file:
    classifier = pickle.load(model_file)

# Initialize YOLO model
facemodel = YOLO('yolov8n-face.pt')  # Update with your YOLO model path
base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

def face_recognition(video_path, output_path, expand_ratio=0.3):
    os.makedirs(output_path, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    trackers = {}
    track_id_counter = 0

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
                detected_faces.append((x1, y1, x2, y2))

        for track_id, tracker_info in list(trackers.items()):
            tracker, bbox, inactive_frames = tracker_info
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                trackers[track_id] = (tracker, (x, y, x + w, y + h), 0)
            else:
                inactive_frames += 1
                if inactive_frames > 5:
                    del trackers[track_id]
                else:
                    trackers[track_id] = (tracker, bbox, inactive_frames)

        for bbox in detected_faces:
            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = y2 - y1
            bbox = (x1, y1, x2 - x1, y2 - y1)
            best_iou = 0
            best_tracker_id = None
            for tracker_id, (_, last_bbox, _) in trackers.items():
                lx1, ly1, lx2, ly2 = last_bbox
                intersection_area = max(0, min(x2, lx2) - max(x1, lx1)) * max(0, min(y2, ly2) - max(y1, ly1))
                box_area = (x2 - x1) * (y2 - y1)
                tracker_area = (lx2 - lx1) * (ly2 - ly1)
                iou = intersection_area / float(box_area + tracker_area - intersection_area)
                if iou > best_iou:
                    best_iou = iou
                    best_tracker_id = tracker_id
            if best_iou > 0.5 and best_tracker_id is not None:
                tracker = trackers[best_tracker_id][0]
                tracker.init(frame, bbox)
                trackers[best_tracker_id] = (tracker, (x1, y1, x2, y2), 0)
            else:
                new_tracker = cv2.TrackerCSRT_create()
                new_tracker.init(frame, bbox)
                trackers[track_id_counter] = (new_tracker, (x1, y1, x2, y2), 0)
                track_id_counter += 1

        for tracker_id, (_, bbox, _) in trackers.items():
            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = y2 - y1
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 1)
            face_crop = frame[y1:y2, x1:x2]
            face_resized = cv2.resize(face_crop, (224, 224))
            face_resized = np.expand_dims(face_resized, axis=0)
            face_resized = preprocess_input(face_resized)
            face_features = base_model.predict(face_resized)
            face_features_flat = np.reshape(face_features, (1, -1))
            person_id = classifier.predict(face_features_flat)[0]
            confidence_score = classifier.decision_function(face_features_flat)[0]
            cv2.putText(frame, f'ID: {person_id} ({confidence_score[0]:.2f})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            track_folder = os.path.join(output_path, str(person_id))
            os.makedirs(track_folder, exist_ok=True)
            face_filename = os.path.join(track_folder, f'face_{tracker_id}_{len(os.listdir(track_folder))}.png')
            cv2.imwrite(face_filename, face_crop)

        output_frame_path = os.path.join(output_path, 'output_video.mp4')
        if 'out' not in locals():
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_frame_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    video_path = 'input_video.mp4'
    output_path = 'output'
    file.save(video_path)

    face_recognition(video_path, output_path)

    output_video_path = os.path.join(output_path, 'output_video.mp4')
    return send_file(output_video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
