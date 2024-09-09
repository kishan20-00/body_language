import "./App.css";
import './css/elegant-icons.css';
import './css/font-awesome.min.css';
import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Camera from "./components/Camera";
import CameraObject from "./components/CameraObject";
import ImageView from "./components/ImageView";
import Main from "./components/Main";
import Object from "./components/Object";
import Register from "./components/Register";
import User from "./components/User";
import Login from "./components/Login";
import Map from "./components/Map";
import Nav from "./components/nav";
import Footer from "./components/footer";
import ButterToast, { POS_RIGHT, POS_TOP } from "butter-toast";
import { height } from "@mui/system";
import PersonIdentify from "./components/PersonIdentify";
import VideoUpload from "./components/AnomalyDetect";
import VideoProcessing from "./components/FaceRecognition";

function App() {
  return (
    <Router>
      <div
        className="App center-div-custom"
        style={{
          backgroundImage: "url(/bg.png)",
          backgroundRepeat: "repeat",
          backgroundSize: "cover",
          height: "100%",
        }}
      >
        <Nav />
        <div className="app-main-div">
          <Switch>
            <Route path="/main" component={Main} />
            <Route path="/object" component={Object} />
            <Route path="/cameraobject" component={CameraObject} />
            <Route path="/camera" component={Camera} />
            <Route path="/login" component={Login} />
            <Route path="/user" component={User} />
            <Route path="/image" component={ImageView} />
            <Route path="/map" component={Map} />
            <Route path="/register" component={Register} />
            <Route path="/identify" component={PersonIdentify} />
            <Route path="/anomaly" component={VideoUpload} />
            <Route path="/facereco" component={VideoProcessing} />
            <Route path="/" component={User} /> {/* Default Route */}
          </Switch>
        </div>
        <ButterToast position={{ vertical: POS_TOP, horizontal: POS_RIGHT }} />
        <Footer />
      </div>
    </Router>
  );
}

export default App;
