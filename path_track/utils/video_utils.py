import cv2


def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return []

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    print(f"Number of frames read: {len(frames)}")
    return frames


def save_video(output_video_frames, output_video_path):
    if not output_video_frames:
        print("No frames to save!")
        return

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    height, width, _ = output_video_frames[0].shape
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (width, height))

    for frame in output_video_frames:
        out.write(frame)

    out.release()
    print(f"Video saved to: {output_video_path}")
