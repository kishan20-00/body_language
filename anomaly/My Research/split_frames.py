import cv2
import os
import shutil


def extract_frames(video_path, output_folder):
    # Load the video file
    cap = cv2.VideoCapture(video_path)

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate the frame interval to get one frame every 2 seconds
    frame_interval = int(fps * 2)

    # If the output folder already exists, delete it and create a new one
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    # Initialize variables for frame processing
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame every frame_interval frames
        if frame_count % frame_interval == 0:
            cv2.imwrite(os.path.join(output_folder, f'{frame_count}.jpg'), frame)

        frame_count += 1

    cap.release()


# Directory containing all video files
videos_directory = r'D:\SLIIT\Research Project\Videos\dataset\all'

# Output folder for saving frames from all videos
output_main_folder = r'D:\SLIIT\RP-Test\2\All_Video_Frames'

# Iterate over all video files in the directory
for filename in os.listdir(videos_directory):
    if filename.endswith(".mp4"):  # Adjust file extension as needed
        video_path = os.path.join(videos_directory, filename)
        output_folder = os.path.join(output_main_folder,
                                     os.path.splitext(filename)[0])  # Use video file name as folder name

        # Extract frames from the current video
        extract_frames(video_path, output_folder)
