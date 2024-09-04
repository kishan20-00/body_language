import requests

# Define the URL of your Flask endpoint
url = 'http://localhost:5001/process_video'

# Path to your input video file
input_video_path = 'path_to_your_video.mp4'

# Path to save the output video
output_video_path = 'processed_video.mp4'

# Open the video file in binary mode
with open(input_video_path, 'rb') as video_file:
    # Prepare the files parameter for the POST request
    files = {'video': video_file}
    
    # Send the POST request
    response = requests.post(url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the response content (processed video) to a file
        with open(output_video_path, 'wb') as output_file:
            output_file.write(response.content)
        print(f'Processed video saved to {output_video_path}')
    else:
        print(f'Error: {response.status_code} - {response.text}')
