import React, { useState } from 'react';
import axios from 'axios';

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

      // Create a URL for the video file
      const videoBlob = new Blob([response.data], { type: 'video/mp4' });
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

      // Create a URL for the video file
      const videoBlob = new Blob([response.data], { type: 'video/mp4' });
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
    <div>
      <h1>Video Processing</h1>
      
      {/* Face Recognition Section */}
      <div>
        <h2>Face Recognition</h2>
        <form onSubmit={handleSubmitFace}>
          <input type="file" accept="video/*" onChange={handleFileChangeFace} />
          <button type="submit" disabled={loadingFace}>
            {loadingFace ? 'Processing...' : 'Upload and Process'}
          </button>
        </form>
        {videoURLFace && (
          <div>
            <h3>Processed Video (Face Recognition):</h3>
            <video controls src={videoURLFace} width="600"></video>
            <a href={videoURLFace} download="processed_video_face.mp4">
              <button>Download Video</button>
            </a>
          </div>
        )}
      </div>

      {/* Gait Analysis Section */}
      <div>
        <h2>Gait Analysis</h2>
        <form onSubmit={handleSubmitGait}>
          <input type="file" accept="video/*" onChange={handleFileChangeGait} />
          <button type="submit" disabled={loadingGait}>
            {loadingGait ? 'Processing...' : 'Upload and Process'}
          </button>
        </form>
        {videoURLGait && (
          <div>
            <h3>Processed Video (Gait Analysis):</h3>
            <video controls src={videoURLGait} width="600"></video>
            <a href={videoURLGait} download="processed_video_gait.mp4">
              <button>Download Video</button>
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoProcessing;
