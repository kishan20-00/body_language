import React, { useState } from 'react';
import axios from 'axios';
import '../css/VideoInputPage.css';

function VideoUpload() {
    const [videoFile, setVideoFile] = useState(null);
    const [downloadLink, setDownloadLink] = useState(null);
    const [loading, setLoading] = useState(false); // Loading state

    const handleVideoUpload = (event) => {
        setVideoFile(event.target.files[0]);
    };

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append('video', videoFile);

        setLoading(true); // Set loading to true when the request starts

        try {
            const response = await axios.post('http://localhost:5001/process_video', formData, {
                responseType: 'blob', // Receive the video file as a blob
            });

            // Create a download link for the video blob
            const downloadUrl = URL.createObjectURL(new Blob([response.data], { type: 'video/mp4' }));
            setDownloadLink(downloadUrl);
        } catch (error) {
            console.error('Error uploading video', error);
        } finally {
            setLoading(false); // Set loading to false when the request is completed
        }
    };

    return (
        <div className="video-upload-container">
            <h1>Anomaly Detection</h1>
            <input type="file" onChange={handleVideoUpload} accept="video/mp4" className="file-input" />
            <button onClick={handleSubmit} className="upload-button" disabled={loading}>
                {loading ? 'Processing...' : 'Upload and Process'} {/* Display loading text */}
            </button>
            {loading && <p className="loading-text">Your video is being processed. Please wait...</p>}
            {downloadLink && (
                <div className="download-section">
                    <h2>Download Processed Video</h2>
                    <a href={downloadLink} download="processed_video.mp4" className="download-link">Download Video</a>
                </div>
            )}
        </div>
    );
}

export default VideoUpload;
