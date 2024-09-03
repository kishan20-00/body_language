from flask import Flask, request, send_file, jsonify, make_response
import os
from ultralytics import YOLO
import cv2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Directories for storing uploaded and processed videos
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Load YOLO model
model = YOLO("runs/detect/train/weights/best.pt")  # replace with your model path
threshold = 0.5
class_name_dict = {0: 'Hidden Face', 1: 'Face'}

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(video_path)
    
    processed_path = process_video(video_path)
    if processed_path.startswith("Error"):
        return jsonify({"error": processed_path}), 400
    
    return jsonify({"message": "Video processed successfully", "filename": os.path.basename(processed_path)})

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return 'Error: video file not found.'

    ret, frame = cap.read()
    if frame is None:
        return 'Error: no frames.'

    H, W, _ = frame.shape
    video_path_out = os.path.join(PROCESSED_FOLDER, os.path.basename(video_path))
    video_path_out = video_path_out.replace('.mp4', '_out.mp4')
    
    out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

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
    cv2.destroyAllWindows()
    return video_path_out

@app.route('/download/<filename>', methods=['GET'])
def download_video(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(file_path):
        response = make_response(send_file(file_path, mimetype='video/mp4'))
        response.headers['Content-Disposition'] = f'inline; filename={filename}'
        return response
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
    app.run(debug=False)  # Set debug=False to avoid auto-reloading
