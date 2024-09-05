import React, { useState } from 'react';
import axios from 'axios';
import './VideoProcessing.css'; // Import the CSS file

const VideoProcessing = () => {
  const [selectedFileFace, setSelectedFileFace] = useState(null);
  const [selectedFileGait, setSelectedFileGait] = useState(null);
  const [videoURLFace, setVideoURLFace] = useState('');
  const [videoURLGait, setVideoURLGait] = useState('');
  const [loadingFace, setLoadingFace] = useState(false);
  const [loadingGait, setLoadingGait] = useState(false);

  // Handle file change for Face Recognition
  const handleFileChangeFace = (event) => {
    setSelectedFileFace(event.target.files[0]);
  };

  // Handle file change for Gait Analysis
  const handleFileChangeGait = (event) => {
    setSelectedFileGait(event.target.files[0]);
  };

  // Handle form submission for Face Recognition
  const handleSubmitFace = async (event) => {
    event.preventDefault();

    if (!selectedFileFace) {
      alert("Please select a video file for Face Recognition.");
      return;
    }

    setLoadingFace(true);

    const formData = new FormData();
    formData.append('video', selectedFileFace);

    try {
      const response = await axios.post('http://localhost:5001/process_video', formData, {
        responseType: 'blob'
      });

      const videoBlob = new Blob([response.data], { type: 'video/avi' });
      const videoUrl = URL.createObjectURL(videoBlob);
      setVideoURLFace(videoUrl);
    } catch (error) {
      console.error('Error uploading video for Face Recognition:', error);
      alert('Failed to process video for Face Recognition.');
    } finally {
      setLoadingFace(false);
    }
  };

  // Handle form submission for Gait Analysis
  const handleSubmitGait = async (event) => {
    event.preventDefault();

    if (!selectedFileGait) {
      alert("Please select a video file for Gait Analysis.");
      return;
    }

    setLoadingGait(true);

    const formData = new FormData();
    formData.append('video', selectedFileGait);

    try {
      const response = await axios.post('http://localhost:5002/process_video', formData, {
        responseType: 'blob'
      });

      const videoBlob = new Blob([response.data], { type: 'video/avi' });
      const videoUrl = URL.createObjectURL(videoBlob);
      setVideoURLGait(videoUrl);
    } catch (error) {
      console.error('Error uploading video for Gait Analysis:', error);
      alert('Failed to process video for Gait Analysis.');
    } finally {
      setLoadingGait(false);
    }
  };

  return (
    <div className="container">
      <h1>Video Processing</h1>
      
      {/* Face Recognition Section */}
      <div className="section">
        <h2>Face Recognition</h2>
        <form onSubmit={handleSubmitFace}>
          <input type="file" accept="video/*" onChange={handleFileChangeFace} className="file-input" />
          <button type="submit" disabled={loadingFace} className="submit-button">
            {loadingFace ? 'Processing...' : 'Upload for Face Recognition'}
          </button>
        </form>
        {videoURLFace && (
          <div className="video-section">
            <h3>Processed Video:</h3>
            <video controls src={videoURLFace} className="video-player" />
            <a href={videoURLFace} download="processed_face_video.avi" className="download-link">
              Download Processed Face Recognition Video
            </a>
          </div>
        )}
      </div>

      {/* Gait Analysis Section */}
      <div className="section">
        <h2>Gait Analysis</h2>
        <form onSubmit={handleSubmitGait}>
          <input type="file" accept="video/*" onChange={handleFileChangeGait} className="file-input" />
          <button type="submit" disabled={loadingGait} className="submit-button">
            {loadingGait ? 'Processing...' : 'Upload for Gait Analysis'}
          </button>
        </form>
        {videoURLGait && (
          <div className="video-section">
            <h3>Processed Video:</h3>
            <video controls src={videoURLGait} className="video-player" />
            <a href={videoURLGait} download="processed_gait_video.avi" className="download-link">
              Download Processed Gait Analysis Video
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoProcessing;
