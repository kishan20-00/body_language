import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="App">
      <Navbar />
      <div className="container">
        <h1>BodyLanguage</h1>
        <div className="cards">
          <Card title="Anomaly Detection" link="/anomaly" icon="📄" />
          <Card title="Person Identification" link="/identify" icon="📊" />
          <Card title="Face Recognition" link="/videoprocess" icon="📘" />
          <Card title="Path Tracking" link="/page4" icon="🔧" />
        </div>
      </div>
    </div>
  );
};

const Navbar = () => {
  return (
    <nav className="navbar">
      <h2>BodyLanguage</h2>
    </nav>
  );
};

const Card = ({ title, link, icon }) => {
  return (
    <Link to={link} className="card">
      <div className="card-icon">{icon}</div>
      <h3>{title}</h3>
    </Link>
  );
};

export default Home;
