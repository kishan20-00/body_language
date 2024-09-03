import cv2
import numpy as np
import os 
import yaml 
from yaml.loader import SafeLoader

with open('data.yaml', mode='r') as f:
    data_yaml = yaml.load(f, Loader=SafeLoader)

labels = data_yaml['names']

yolo = cv2.dnn.readNetFromONNX('D:/Python/person_identify/best.onnx')
yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def process_frame(frame):
    row, col, d = frame.shape

    # get yolo predictions from the image
    max_rc = max(row, col)
    input_image = np.zeros((max_rc, max_rc, 3), dtype=np.uint8)
    input_image[0:row, 0:col] = frame
    INPUT_WH_YOLO = 640
    blob = cv2.dnn.blobFromImage(input_image, 1/255, (INPUT_WH_YOLO, INPUT_WH_YOLO), swapRB=True, crop=False)
    yolo.setInput(blob)
    preds = yolo.forward()  # detections or predictions from yolo

    detections = preds[0]

    boxes = []
    confidences = []
    classes = []

    image_w, image_h = input_image.shape[:2]
    x_factor = image_w / INPUT_WH_YOLO
    y_factor = image_h / INPUT_WH_YOLO

    for i in range(len(detections)):
        row = detections[i]
        confidence = row[4]  # confidence of detection of an object
        if confidence > 0.4:
            class_score = row[5:].max()
            class_id = row[5:].argmax()

            if class_score > 0.25:
                cx, cy, w, h = row[0:4]
                left = int((cx - 0.5*w) * x_factor)
                top = int((cy - 0.5*w) * x_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)

                box = np.array([left, top, width, height])
                confidences.append(confidence)
                boxes.append(box)
                classes.append(class_id)

    boxes_np = np.array(boxes).tolist()
    confidences_np = np.array(confidences).tolist()
    index = cv2.dnn.NMSBoxes(boxes_np, confidences_np, 0.25, 0.45)

    # draw boundings
    for ind in index:
        x, y, w, h = boxes_np[ind]
        bb_conf = int(confidences_np[ind] * 100)
        class_id = classes[ind]
        class_name = labels[class_id]

        text = f'{class_name} : {bb_conf}%'
        
        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Increase font size
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    return frame

cap = cv2.VideoCapture('D:/Python/person_identify/uploaded_video.mp4')  # Replace 'your_video.mp4' with the path to your video file
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        processed_frame = process_frame(frame)
        cv2.imshow('Processed Video', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
