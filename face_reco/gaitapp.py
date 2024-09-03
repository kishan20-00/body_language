from flask import Flask, request, send_file
import cv2
import numpy as np
import torch
from tensorflow.keras.models import load_model
import os

app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Load the gait recognition model
gait_model = load_model('resnet50_model.h5')  # Update path as needed

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    input_path = 'input_video.mp4'
    output_path = 'output_video.mp4'
    
    file.save(input_path)

    # Process the video
    process_video(input_path, output_path)

    return send_file(output_path, as_attachment=True)

def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    # Initialize an empty dictionary to store trackers and their last known bounding boxes
    trackers = {}
    track_id_counter = 0
    frame_counter = 0
    person_ids = {}

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform detection using YOLOv5
        results = model(frame)
        persons = results.pred[0][results.pred[0][:, 5] == 0]

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

                person_crop = frame[y1:y2, x1:x2]
                person_crop = cv2.resize(person_crop, (128, 128))
                person_crop = person_crop / 255.0
                person_crop = np.expand_dims(person_crop, axis=0)

                prediction = gait_model.predict(person_crop)
                predicted_id = np.argmax(prediction)
                confidence = np.max(prediction)

                person_ids[track_id_counter] = (predicted_id, confidence)
                track_id_counter += 1

        aspect_ratio_threshold = (0.3, 0.6)
        relative_area_threshold = 0.02

        frame_area = frame.shape[0] * frame.shape[1]

        for tracker_id, (_, bbox, _) in trackers.items():
            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = y2 - y1
            aspect_ratio = width / float(height)
            area = width * height
            relative_area = area / frame_area

            extend_pixels = 30
            x1 = max(0, x1 - extend_pixels)
            y1 = max(0, y1 - extend_pixels)
            x2 = min(frame.shape[1], x2 + extend_pixels)
            y2 = min(frame.shape[0], y2 + extend_pixels)

            if aspect_ratio_threshold[0] <= aspect_ratio <= aspect_ratio_threshold[1] and relative_area > relative_area_threshold:
                predicted_id, confidence = person_ids.get(tracker_id, (None, None))
                if predicted_id is not None:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)
                    cv2.putText(frame, f'ID: {predicted_id}, Conf: {confidence:.2f}', (x1, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                    person_crop = frame[y1:y2, x1:x2]
                    track_folder = os.path.join('output_frames', str(tracker_id))
                    os.makedirs(track_folder, exist_ok=True)
                    cv2.imwrite(os.path.join(track_folder, f'frame_{tracker_id}_{frame_counter}.png'), person_crop)

        out.write(frame)

        frame_counter += 1

    cap.release()
    out.release()

if __name__ == '__main__':
    app.run(debug=True)
