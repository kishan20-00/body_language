import requests

# Replace this URL with your actual endpoint
url = 'http://127.0.0.1:5000/upload_video'  # Localhost example, change as needed
video_path = '/path/to/your/video/file.mp4'  # Replace with the path to your video file

# Open the video file in binary mode
with open(video_path, 'rb') as video_file:
    # Prepare the files dictionary for the request
    files = {'video': video_file}
    
    # Send the POST request to the server
    response = requests.post(url, files=files)

# Print the server's response
print(response.json())
