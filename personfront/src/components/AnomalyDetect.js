import React, { useState } from "react";
import axios from "axios";
import "./VideoInputPage.css";

function VideoInputPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [downloadLink, setDownloadLink] = useState("");
  const [videoUrl, setVideoUrl] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setUploadStatus("Uploading...");

    try {
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setUploadStatus("Upload successful!");
      setDownloadLink(response.data.filename);
      setVideoUrl(`http://localhost:5000/download/${response.data.filename}`);
    } catch (error) {
      setUploadStatus("Upload failed!");
      console.error("Error uploading file:", error);
    }
  };

  const handleDownload = () => {
    if (!downloadLink) {
      alert("No video to download!");
      return;
    }

    // Trigger the download
    const link = document.createElement("a");
    link.href = videoUrl;
    link.setAttribute("download", downloadLink);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link); // Clean up
  };

  return (
    <div className="video-input-page">
      <h1>Video Uploader</h1>
      <input type="file" onChange={handleFileChange} className="file-input" />
      <button onClick={handleUpload} className="upload-button">Upload Video</button>
      <p className="upload-status">{uploadStatus}</p>

      {videoUrl && (
        <div className="video-container">
          <h2>Processed Video</h2>
          <video width="600" controls>
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}

      {downloadLink && (
        <div className="download-container">
          <button onClick={handleDownload} className="download-button">Download Processed Video</button>
        </div>
      )}
    </div>
  );
}

export default VideoInputPage;
