import requests

url = 'http://127.0.0.1:5002/process_video'
video_path = '/path/to/video/file.mp4'

with open(video_path, 'rb') as video_file:
    response = requests.post(url, files={'video': video_file})

with open('processed_video.avi', 'wb') as output_file:
    output_file.write(response.content)
