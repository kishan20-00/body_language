import requests

# Replace with the URL of your Flask API
url = 'http://localhost:5000/upload'

# Path to the video you want to upload
video_path = 'path/to/your/video.mp4'

# Open the video file in binary mode
with open(video_path, 'rb') as video_file:
    # Send a POST request to the Flask API
    response = requests.post(url, files={'file': video_file})

# Check if the request was successful
if response.status_code == 200:
    # Save the processed video
    output_video_path = 'output_video.mp4'
    with open(output_video_path, 'wb') as output_file:
        output_file.write(response.content)
    print(f'Processed video saved as {output_video_path}')
else:
    print(f'Failed to process video. Status code: {response.status_code}')
    print(f'Response: {response.text}')
