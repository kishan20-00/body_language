from flask import Flask, request, Response
import torch
import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model
from io import BytesIO
import tempfile

app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Load the gait recognition model
gait_model = load_model('resnet50_model.h5')

@app.route('/process_video', methods=['POST'])
def process_video():
    # Check if video file is in the request
    if 'video' not in request.files:
        return {"error": "No video file provided"}, 400

    # Get video from request
    video_file = request.files['video']

    # Create a temporary file to store the video
    temp_video_file = tempfile.NamedTemporaryFile(delete=False)
    temp_video_file.write(video_file.read())
    temp_video_file.close()

    # Open the video file with OpenCV
    cap = cv2.VideoCapture(temp_video_file.name)

    # Initialize the video writer
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Output video stream
    output_video_stream = BytesIO()

    # Video writer with MJPEG format
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output.avi', fourcc, output_fps, (frame_width, frame_height))

    trackers = {}
    track_id_counter = 0
    frame_counter = 0
    person_ids = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform detection using YOLOv5
        results = model(frame)
        persons = results.pred[0][results.pred[0][:, 5] == 0]  # Filter class 0 (person)

        # Update all existing trackers
        for tracker_id, (tracker, last_bbox, inactive_frames) in list(trackers.items()):
            ok, bbox = tracker.update(frame)
            if ok:
                x, y, w, h = [int(v) for v in bbox]
                trackers[tracker_id] = (tracker, (x, y, x + w, y + h), 0)
            else:
                inactive_frames += 1
                if inactive_frames > 5:
                    del trackers[tracker_id]
                else:
                    trackers[tracker_id] = (tracker, last_bbox, inactive_frames)

        # Match detections to existing trackers using IoU
        for person in persons:
            box = person[:4].detach().cpu().numpy().astype(int)
            x1, y1, x2, y2 = box
            bbox = (x1, y1, x2 - x1, y2 - y1)

            best_iou = 0
            best_tracker_id = None

            for tracker_id, (_, last_bbox, _) in trackers.items():
                lx1, ly1, lx2, ly2 = last_bbox
                intersection_area = max(0, min(x2, lx2) - max(x1, lx1)) * max(0, min(y2, ly2) - max(y1, ly1))
                box_area = (x2 - x1) * (y2 - y2)
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

                person_crop = frame[y1:y2, x1:x2]
                person_crop = cv2.resize(person_crop, (128, 128))
                person_crop = person_crop / 255.0
                person_crop = np.expand_dims(person_crop, axis=0)

                prediction = gait_model.predict(person_crop)
                predicted_id = np.argmax(prediction)
                confidence = np.max(prediction)

                person_ids[track_id_counter] = (predicted_id, confidence)
                track_id_counter += 1

        # Drawing boxes and adding text
        for tracker_id, (_, bbox, _) in trackers.items():
            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = y2 - y1

            predicted_id, confidence = person_ids.get(tracker_id, (None, None))
            if predicted_id is not None:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)
                cv2.putText(frame, f'ID: {predicted_id}, Conf: {confidence:.2f}', (x1, y1 - 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        out.write(frame)

        frame_counter += 1

    cap.release()
    out.release()

    with open('output.avi', 'rb') as f:
        output_video_stream.write(f.read())

    os.remove(temp_video_file.name)

    return Response(output_video_stream.getvalue(), mimetype='video/x-msvideo')

if __name__ == '__main__':
    app.run(debug= True, port=5002)
