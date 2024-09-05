import React from 'react';
import { Link } from 'react-router-dom';
import { FaUserCheck, FaExclamationCircle, FaRoute } from 'react-icons/fa';
import { MdFace } from 'react-icons/md';
import './Home.css'; // Import custom styles for Home page

const Home = () => {
  return (
    <div className="home-container">
      <h1>Welcome to Surveillance System Dashboard</h1>

      <div className="card-grid">
        {/* Face Recognition Card */}
        <div className="card">
          <MdFace className="card-icon" size={50} />
          <h3>Face Recognition</h3>
          <p>Identify people using facial recognition technology.</p>
          <Link to="/videoprocess" className="card-link">Go to Face Recognition</Link>
        </div>

        {/* Person Identification Card */}
        <div className="card">
          <FaUserCheck className="card-icon" size={50} />
          <h3>Person Identification</h3>
          <p>Track and identify individuals in video footage.</p>
          <Link to="/identify" className="card-link">Go to Person Identification</Link>
        </div>

        {/* Anomaly Detection Card */}
        <div className="card">
          <FaExclamationCircle className="card-icon" size={50} />
          <h3>Anomaly Detection</h3>
          <p>Detect unusual activities in video streams.</p>
          <Link to="/anomaly" className="card-link">Go to Anomaly Detection</Link>
        </div>

        {/* Path Tracking Card */}
        <div className="card">
          <FaRoute className="card-icon" size={50} />
          <h3>Path Tracking</h3>
          <p>Track movement paths in videos for further insights.</p>
          <Link to="/pathtrack" className="card-link">Go to Path Tracking</Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
