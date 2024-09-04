import streamlit as st
import os
import pickle
import cv2
import numpy as np
from collections import Counter


# Define function to load person tracks from pickle files
def load_person_tracks(folder_path):
    person_tracks = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.pkl'):
            with open(os.path.join(folder_path, filename), 'rb') as f:
                person_id = filename.split('_')[0]
                tracks = pickle.load(f)
                person_tracks[person_id] = tracks
    return person_tracks


# Function to generate heatmap from person tracks
def generate_heatmap(person_tracks, frame_shape):
    heatmap = np.zeros((frame_shape[0], frame_shape[1]))  # Assuming video resolution is frame_shape
    for person_id, tracks in person_tracks.items():
        for track in tracks:
            for bbox in track:
                x1, y1, x2, y2 = bbox
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                heatmap[y1:y2, x1:x2] += 1

    # Normalize the heatmap
    heatmap = heatmap / heatmap.max()  # Normalize to [0.0, 1.0]

    return heatmap


# Streamlit App
# Streamlit App
def main():
    st.title('People Path Analytics')

    # Load floor map image
    floor_map_path = os.path.join(os.path.dirname(__file__), 'floormap.png')
    floor_map_image = cv2.imread(floor_map_path)
    floor_map_image = cv2.cvtColor(floor_map_image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

    # Sidebar interactions
    st.sidebar.title("Interactive Options")
    option = st.sidebar.selectbox("Select Display Option",
                                  ["Heatmaps",
                                   "Show Paths", "Show Paths by Region"])

    if option == "Heatmaps":
        # Load first frame of the video as floor map image
        video_path = os.path.join(os.path.dirname(__file__), '18.03.2024_3 - 002.mp4')
        video_capture = cv2.VideoCapture(video_path)
        success, frame = video_capture.read()
        if success:
            video_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        # Display heatmap overlay on video
        st.subheader("Heatmap Overlay")
        person_tracks_folder = os.path.join(os.path.dirname(__file__), 'person_tracks')
        person_tracks = load_person_tracks(person_tracks_folder)
        heatmap_video = generate_heatmap(person_tracks, video_frame.shape)
        heatmap_video = cv2.applyColorMap(np.uint8(255 * heatmap_video), cv2.COLORMAP_HOT)
        heatmap_video = cv2.cvtColor(heatmap_video, cv2.COLOR_BGR2RGB)
        overlay_video = cv2.addWeighted(heatmap_video, 0.5, video_frame, 0.5, 0)
        st.image(overlay_video, caption='Heatmap Overlay', use_column_width=True)

        # Display heatmap overlay on floor map
        st.subheader("Heatmap Overlay on Floor Map")
        heatmap_floor_map = generate_heatmap(person_tracks, floor_map_image.shape)
        heatmap_floor_map = cv2.applyColorMap(np.uint8(255 * heatmap_floor_map), cv2.COLORMAP_HOT)
        heatmap_floor_map = cv2.cvtColor(heatmap_floor_map, cv2.COLOR_BGR2RGB)
        overlay_floor_map = cv2.addWeighted(heatmap_floor_map, 0.5, floor_map_image, 0.5, 0)
        st.image(overlay_floor_map, caption='Heatmap Overlay on Floor Map', use_column_width=True)

    elif option == "Show Paths":

        # Load first frame of the video

        video_path = os.path.join(os.path.dirname(__file__), '18.03.2024_3 - 002.mp4')

        video_capture = cv2.VideoCapture(video_path)

        success, frame = video_capture.read()

        if success:
            first_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        # Display trajectories overlay on the first frame

        st.subheader("Trajectories Overlay on First Frame")

        person_tracks_folder = os.path.join(os.path.dirname(__file__), 'person_tracks')

        person_tracks = load_person_tracks(person_tracks_folder)

        overlay_frame = first_frame.copy()

        num_people = len(person_tracks)  # Counting the number of people

        # Display the number of people detected above the image
        st.write(f'Number of People: {num_people}')

        for person_id, tracks in person_tracks.items():

            color = tuple(np.random.randint(0, 255, size=(3,)).tolist())  # Convert array to tuple

            for track in tracks:

                for i in range(len(track) - 1):

                    x1, y1, x2, y2 = track[i]

                    x1_next, y1_next, x2_next, y2_next = track[i + 1]

                    x_center, y_center = (x1 + x2) // 2, (y1 + y2) // 2

                    x_center_next, y_center_next = (x1_next + x2_next) // 2, (y1_next + y2_next) // 2

                    cv2.line(overlay_frame, (int(x_center), int(y_center)), (int(x_center_next), int(y_center_next)),
                             color, 2)

                    # Draw circles to make the line dotted

                    num_dots = int(
                        np.linalg.norm(np.array([x_center, y_center]) - np.array([x_center_next, y_center_next])))

                    for j in range(num_dots):
                        alpha = (j + 1) / num_dots

                        dot_x = int(alpha * x_center_next + (1 - alpha) * x_center)

                        dot_y = int(alpha * y_center_next + (1 - alpha) * y_center)

                        cv2.circle(overlay_frame, (dot_x, dot_y), radius=1, color=color, thickness=-1)

        st.image(overlay_frame, caption='Trajectories Overlay on First Frame', use_column_width=True)


    elif option == "Show Paths by Region":

        # Load first frame of the video
        video_path = os.path.join(os.path.dirname(__file__), '18.03.2024_3 - 002.mp4')
        video_capture = cv2.VideoCapture(video_path)
        success, frame = video_capture.read()
        if success:
            first_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        # Display region selection options
        st.subheader("Select Region")

        region_options = ["Region 1", "Region 2", "Region 3"]
        selected_region = st.selectbox("Select Region", region_options)

        # Define region coordinates (assuming equal division)
        frame_height, frame_width, _ = first_frame.shape
        region_height = frame_height // 3
        region_width = frame_width

        if selected_region == "Region 1":
            region = (0, 0, region_width, region_height)
        elif selected_region == "Region 2":
            region = (0, region_height, region_width, 2 * region_height)
        else:  # Region 3
            region = (0, 2 * region_height, region_width, frame_height)

        # Display trajectories overlay for the selected region
        st.subheader(f"Trajectories Overlay for {selected_region}")

        person_tracks_folder = os.path.join(os.path.dirname(__file__), 'person_tracks')
        person_tracks = load_person_tracks(person_tracks_folder)

        overlay_frame = first_frame.copy()

        num_people_in_region = 0
        people_in_region = set()

        for person_id, tracks in person_tracks.items():
            color = tuple(np.random.randint(0, 255, size=(3,)).tolist())  # Convert array to tuple
            for track in tracks:
                for i in range(len(track) - 1):
                    x1, y1, x2, y2 = track[i]
                    if region[0] <= (x1 + x2) // 2 <= region[2] and region[1] <= (y1 + y2) // 2 <= region[3]:
                        people_in_region.add(person_id)
                        x1_next, y1_next, x2_next, y2_next = track[i + 1]
                        x_center, y_center = (x1 + x2) // 2, (y1 + y2) // 2
                        x_center_next, y_center_next = (x1_next + x2_next) // 2, (y1_next + y2_next) // 2
                        cv2.line(overlay_frame, (int(x_center), int(y_center)),
                                 (int(x_center_next), int(y_center_next)),
                                 color, 2)
                        num_dots = int(
                            np.linalg.norm(np.array([x_center, y_center]) - np.array([x_center_next, y_center_next])))
                        for j in range(num_dots):
                            alpha = (j + 1) / num_dots
                            dot_x = int(alpha * x_center_next + (1 - alpha) * x_center)
                            dot_y = int(alpha * y_center_next + (1 - alpha) * y_center)
                            cv2.circle(overlay_frame, (dot_x, dot_y), radius=1, color=color, thickness=-1)

        num_people_in_region = len(people_in_region)
        st.image(overlay_frame, caption=f'Trajectories Overlay for {selected_region}', use_column_width=True)

        # Display number of people detected in the selected region
        st.write(f'Number of People in {selected_region}: {num_people_in_region}')


if __name__ == "__main__":
    main()
