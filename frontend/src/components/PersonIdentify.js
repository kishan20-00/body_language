import React, { useState } from 'react';
import axios from 'axios';
import JSZip from 'jszip'; // Import JSZip to handle zip file extraction
import '../css/PersonIdentify.css';

function PersonIdentify() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [outputVideoUrl, setOutputVideoUrl] = useState(null);
  const [processedVideoUrl, setProcessedVideoUrl] = useState(null);
  const [uploading, setUploading] = useState(false);

  // Handle file selection
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Handle file upload and video processing
  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a video file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setUploading(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/process_video', formData, {
        responseType: 'blob', // Important to get the response as a blob
      });

      // Load the response as a zip file
      const zip = await JSZip.loadAsync(response.data);

      // Extract and create URLs for both videos
      const outputVideoBlob = await zip.file('output_video.mp4').async('blob');
      const processedVideoBlob = await zip.file('processed_output_video.mp4').async('blob');

      const outputVideoUrl = URL.createObjectURL(outputVideoBlob);
      const processedVideoUrl = URL.createObjectURL(processedVideoBlob);

      setOutputVideoUrl(outputVideoUrl);
      setProcessedVideoUrl(processedVideoUrl);
      setUploading(false);
    } catch (error) {
      console.error('Error uploading and processing video', error);
      alert('Error uploading and processing video');
      setUploading(false);
    }
  };

  return (
    <div className="person-identify-page">
      <h1>Person Identification</h1>
      
      {/* File input for selecting video */}
      <input type="file" onChange={handleFileChange} accept="video/*" className="file-input" />
      
      {/* Button for uploading and processing */}
      <button onClick={handleUpload} disabled={uploading} className="upload-button">
        {uploading ? 'Processing...' : 'Upload and Process Video'}
      </button>

      {/* Display the output video if available */}
      {outputVideoUrl && (
        <div className="video-container">
          <h2>Output Video</h2>
          <video src={outputVideoUrl} controls width="600" />
        </div>
      )}

      {/* Display the processed video if available */}
      {processedVideoUrl && (
        <div className="video-container">
          <h2>Processed Video</h2>
          <video src={processedVideoUrl} controls width="600" />
        </div>
      )}
    </div>
  );
}

export default PersonIdentify;
