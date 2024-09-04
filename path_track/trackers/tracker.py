from ultralytics import YOLO
import cv2
import pickle

class Tracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect_frames(self, frames, read_from_stub=False, stub_path=None):
        people_detections = []

        if read_from_stub and stub_path is not None:
            with open(stub_path, 'rb')as f:
                people_detections = pickle.load(f)
            return people_detections

        for frame in frames:
            people_dict = self.detect_frame(frame)
            people_detections.append(people_dict)

        if stub_path is not None:
            with open(stub_path, 'wb')as f:
                pickle.dump(people_detections, f)

        return people_detections

    def detect_frame(self, frame):
        results = self.model.track(frame, persist=True)[0]
        id_name_dict = results.names

        people_dict = {}
        for box in results.boxes:
            track_id = int(box.id.tolist()[0])
            result = box.xyxy.tolist()[0]
            object_cls_id = box.cls.tolist()[0]
            object_cls_name = id_name_dict[object_cls_id]
            if object_cls_name == "person":
                people_dict[track_id] = result
        return people_dict

    def draw_bboxes(self, video_frames, people_detections):
        output_video_frames = []
        for frame, people_dict in zip(video_frames, people_detections):
            for track_id, bbox in people_dict.items():
                x1, y1, x2, y2 = bbox
                cv2.putText(frame, f"Person ID: {track_id}", (int(bbox[0]), int(bbox[1] - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                frame = cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
            output_video_frames.append(frame)

        return output_video_frames
