import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PersonIdentify from './components/PersonIdentify';
import VideoInputPage from './components/AnomalyDetect'; // Import the component
import Home from './components/Home';
import VideoProcessing from './components/FaceRecognition';

const App = () => {
  return (
    <BrowserRouter>
    <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/identify" element={<PersonIdentify />} />
    <Route path="/anomaly" element={<VideoInputPage />} />
    <Route path="/videoprocess" element={<VideoProcessing />} />
    </Routes>
    </BrowserRouter>
  );
};

export default App;
