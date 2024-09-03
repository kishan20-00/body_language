import requests

def upload_video(file_path, url='http://localhost:5000/upload'):
    """
    Uploads a video file to the Flask server and downloads the processed video.
    
    :param file_path: Path to the video file to upload
    :param url: URL of the Flask endpoint
    """
    # Open the video file in binary mode
    with open(file_path, 'rb') as file:
        # Prepare the file to be sent as part of a POST request
        files = {'file': file}
        
        # Send a POST request to the Flask endpoint
        response = requests.post(url, files=files)
        
        # Check if the request was successful
        if response.status_code == 200:
            output_file_path = 'output_video.mp4'
            # Write the response content (processed video) to a file
            with open(output_file_path, 'wb') as output_file:
                output_file.write(response.content)
            print(f'Processed video saved to {output_file_path}')
        else:
            print(f'Error: {response.status_code}, {response.text}')

# Path to the video file to test
video_file_path = 'path_to_your_video_file.mp4'

# Call the function to upload and download the processed video
upload_video(video_file_path)
