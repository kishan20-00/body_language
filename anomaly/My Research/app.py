import streamlit as st
from moviepy.editor import *


def convert_video(input_path, output_path):
    # Load the video
    video_clip = VideoFileClip(input_path)

    # Convert the video to H.264 codec and AAC audio codec
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

def main():
    st.title("Image and Video Viewer")

    # Dropdown for selecting content type
    content_type = st.selectbox("Select Content Type", ["Image", "Video"])

    if content_type == "Image":
        # Dropdown for selecting image category
        #category = st.selectbox("Select Image Category", ["Normal", "Anomalous"])

        #if category == "Normal":
            #st.image("C:/Users/thaha/OneDrive/Desktop/My Research/My Research/output/normal.png", caption="Normal Image")
        #elif category == "Anomalous":
        st.image("D:/Python/anomaly/My Research/runs/detect/train/val_batch2_pred.jpg", caption="Predicted Image")

    elif content_type == "Video":
        # Convert the video
        convert_video("D:/Python/anomaly/My Research/videos/aa.mp4_out.mp4", "D:/Python/anomaly/My Research/videos/converted_video.mp4")

        # Display the converted video
        st.video("D:/Python/anomaly/My Research/videos/converted_video.mp4")
        # Dropdown for selecting video category
        #category = st.selectbox("Select Video Category", ["Normal", "Anomalous"])

        #if category == "Normal":
        #st.video("C:/Users/thaha/OneDrive/Desktop/My Research/My Research/videos/aa.mp4_out.mp4")
        #elif category == "Anomalous":
           # st.video("anomalous_video.mp4", caption="Anomalous Video")

if __name__ == "__main__":
    main()
