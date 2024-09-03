import requests
import os

# Define the server URL
base_url = "http://127.0.0.1:5000"  # Make sure this matches your Flask server URL

# Define the path to the video file you want to upload for testing
video_file_path = "D:/Python/anomaly/My Research/videos/aa.mp4"  # Replace with the path to your test video

# Upload the video to the Flask app
upload_url = f"{base_url}/upload"
with open(video_file_path, 'rb') as f:
    files = {'file': (os.path.basename(video_file_path), f)}
    try:
        response = requests.post(upload_url, files=files)
        response.raise_for_status()  # Check for HTTP request errors
    except requests.exceptions.RequestException as e:
        print(f"Error during file upload: {e}")
        exit(1)

# Check if the video processing was successful
if response.status_code == 200:
    response_data = response.json()
    print("Upload response:", response_data)
    if "filename" in response_data:
        # Extract the processed video filename
        processed_filename = response_data["filename"]
        
        # Construct the download URL
        download_url = f"{base_url}/download/{processed_filename}"
        
        # Download the processed video
        try:
            download_response = requests.get(download_url)
            download_response.raise_for_status()  # Check for HTTP request errors
            
            # Save the downloaded video to a file
            output_path = os.path.join("D:/Python/anomaly/My Research/videos", processed_filename)  # Replace with your desired save path
            with open(output_path, 'wb') as output_file:
                output_file.write(download_response.content)
            print(f"Processed video downloaded successfully: {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error during file download: {e}")
    else:
        print("Error: 'filename' not found in the response.")
else:
    print("Error during video processing:", response.text)
