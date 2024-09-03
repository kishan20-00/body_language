import requests

# URL of the Flask endpoint to process the video
url = 'http://127.0.0.1:5000/process_video'

# Path to the input video file you want to upload
input_video_path = 'uploaded_video.mp4'

# Open the file in binary mode and prepare it for upload
with open(input_video_path, 'rb') as file:
    files = {'file': file}
    # Send the POST request with the file to the Flask app
    response = requests.post(url, files=files)

# Check if the request was successful
if response.status_code == 200:
    # Save the received output video to a file
    with open('processed_output_video.mp4', 'wb') as output_file:
        output_file.write(response.content)
    print('Processed video saved as processed_output_video.mp4')
else:
    print(f'Failed to process video. Status code: {response.status_code}')
