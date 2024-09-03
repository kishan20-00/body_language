from flask import Flask, request, send_file
import cv2
import numpy as np
import os
import yaml
from yaml.loader import SafeLoader
from flask_cors import CORS
import zipfile

app = Flask(__name__)
CORS(app)

# Load YOLO model and labels
with open('data.yaml', mode='r') as f:
    data_yaml = yaml.load(f, Loader=SafeLoader)

labels = data_yaml['names']

yolo = cv2.dnn.readNetFromONNX('D:/Python/person_identify/best.onnx')
yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def process_frame(frame):
    row, col, d = frame.shape
    max_rc = max(row, col)
    input_image = np.zeros((max_rc, max_rc, 3), dtype=np.uint8)
    input_image[0:row, 0:col] = frame
    INPUT_WH_YOLO = 640
    blob = cv2.dnn.blobFromImage(input_image, 1/255, (INPUT_WH_YOLO, INPUT_WH_YOLO), swapRB=True, crop=False)
    yolo.setInput(blob)
    preds = yolo.forward()

    detections = preds[0]

    boxes = []
    confidences = []
    classes = []

    image_w, image_h = input_image.shape[:2]
    x_factor = image_w / INPUT_WH_YOLO
    y_factor = image_h / INPUT_WH_YOLO

    for i in range(len(detections)):
        row = detections[i]
        confidence = row[4]
        if confidence > 0.4:
            class_score = row[5:].max()
            class_id = row[5:].argmax()
            if class_score > 0.25:
                cx, cy, w, h = row[0:4]
                left = int((cx - 0.5 * w) * x_factor)
                top = int((cy - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                confidences.append(confidence)
                boxes.append(box)
                classes.append(class_id)

    boxes_np = np.array(boxes).tolist()
    confidences_np = np.array(confidences).tolist()
    index = cv2.dnn.NMSBoxes(boxes_np, confidences_np, 0.25, 0.45)

    for ind in index:
        x, y, w, h = boxes_np[ind]
        bb_conf = int(confidences_np[ind] * 100)
        class_id = classes[ind]
        class_name = labels[class_id]
        text = f'{class_name} : {bb_conf}%'
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    return frame

@app.route('/process_video', methods=['POST'])
def process_video():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    # Save uploaded file to a temporary location
    input_video_path = 'uploaded_video.mp4'
    file.save(input_video_path)

    # Prepare output video paths
    output_video_path = 'output_video.mp4'
    processed_video_path = 'processed_output_video.mp4'
    
    cap = cv2.VideoCapture(input_video_path)
    
    # Use 'avc1' codec for H.264, more compatible with most players
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = None
    out_processed = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = process_frame(frame)
        if out is None:
            # Define the codec and create VideoWriter object for both videos
            out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
            out_processed = cv2.VideoWriter(processed_video_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))

        out.write(processed_frame)
        out_processed.write(processed_frame)  # Duplicate video for demonstration

    cap.release()
    out.release()
    out_processed.release()

    # Create a zip file containing both videos
    zip_path = 'videos.zip'
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(output_video_path)
        zipf.write(processed_video_path)

    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
