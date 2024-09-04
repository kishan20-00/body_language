from flask import Flask, request, Response
import cv2
import numpy as np
import io
import tempfile
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLO model
model_path = 'runs/detect/train/weights/best.pt'
model = YOLO(model_path)  # load a custom model
threshold = 0.5

class_name_dict = {
    0: 'Hidden Face',
    1: 'Face',
}

@app.route('/process_video', methods=['POST'])
def process_video():
    # Check if video file is in the request
    if 'video' not in request.files:
        return {"error": "No video file provided"}, 400

    video_file = request.files['video']

    # Create a temporary file to store the uploaded video
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    temp_input.write(video_file.read())
    temp_input.close()

    # Open video file
    cap = cv2.VideoCapture(temp_input.name)

    if not cap.isOpened():
        return {"error": "Error opening video file"}, 400

    # Get video properties
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return {"error": "Error reading video frames"}, 400

    H, W, _ = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_stream = io.BytesIO()
    out = cv2.VideoWriter(output_stream, fourcc, int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    while ret:
        results = model(frame)[0]
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > threshold:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame, class_name_dict[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        out.write(frame)
        ret, frame = cap.read()

    cap.release()
    out.release()
    output_stream.seek(0)

    # Return the processed video as a response
    return Response(output_stream, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
