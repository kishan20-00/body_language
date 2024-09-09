import React, { useState } from 'react';
import axios from 'axios';
import '../css/VideoProcessing.css';  // Import the CSS file

function VideoProcessing() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setDownloadUrl('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a video file first.");
      return;
    }

    const formData = new FormData();
    formData.append('video', selectedFile);

    setProcessing(true);

    try {
      const response = await axios.post('http://127.0.0.1:5002/upload', formData, {
        responseType: 'blob' // Important for downloading the file
      });

      // Create a URL for the processed video blob
      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
    } catch (error) {
      console.error("There was an error processing the video!", error);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="video-processing-container">
      <h1>Face Recognition & Gait Analysis</h1>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={!selectedFile || processing}>
        {processing ? 'Processing...' : 'Upload and Process'}
      </button>
      {downloadUrl && (
        <div>
          <h3>Download Processed Video</h3>
          <a href={downloadUrl} download="processed_face_reco.mp4">
            Download Video
          </a>
        </div>
      )}
    </div>
  );
}

export default VideoProcessing;
