import React, { useState } from 'react';
import axios from 'axios';
import './PathTracking.css'; // Import the CSS file for styling

const PathTrack = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [videoURL, setVideoURL] = useState('');
  const [loading, setLoading] = useState(false);

  // Handle file change
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      alert("Please select a video file.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/upload_video', formData, {
        responseType: 'blob',
      });

      // Create a URL for the processed video file
      const videoBlob = new Blob([response.data], { type: 'video/mp4' });
      const videoUrl = URL.createObjectURL(videoBlob);
      setVideoURL(videoUrl);
    } catch (error) {
      console.error('Error uploading video:', error);
      alert('Failed to process the video.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h1>Path Tracking</h1>
      <div className="upload-section">
        <form onSubmit={handleSubmit}>
          <input type="file" accept="video/*" onChange={handleFileChange} className="file-input" />
          <button type="submit" disabled={loading} className="upload-button">
            {loading ? 'Processing...' : 'Upload Video'}
          </button>
        </form>
        {videoURL && (
          <div className="video-section">
            <h3>Processed Video:</h3>
            <video controls src={videoURL} className="video-player" />
            <a href={videoURL} download="processed_video.mp4" className="download-link">
              Download Processed Video
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default PathTrack;
