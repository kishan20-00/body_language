import React from 'react';
import '../App.css';

class User extends React.Component {

    constructor(props) {
        super(props);
    }

    render (){
        return (
            <div class="container">
                <img class="home_image" src={ './hero.png' }/>
            <div className="col-lg-12">
            <br/>
                <div class="home_Title">
                    <h5>Surveillance System </h5>
                    <a class="btn btn-success col-md-12" href="/main" >Path Detect Using Video</a>
                    <br/><br/>
                    <a class="btn btn-success col-md-12" href="/camera" >Path Detect Using Camera</a>
                    <br/><br/>
                    <a class="btn btn-success col-md-12" href="/object" >Object Move Detect Using Video</a>
                    <br/><br/>
                    <a class="btn btn-success col-md-12" href="/cameraobject" >Object Move Detect Using Camera</a>
                    <br/><br/>
                    <a class="btn btn-success col-md-12" href="/identify" >Person Identification</a>
                    <br/><br/>
                    <a class="btn btn-success col-md-12" href="/anomaly" >Anomaly Detection</a>
                    <br/><br/>
                    <a class="btn btn-success col-md-12" href="/facereco" >Face Recognition</a>
                </div>
            <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
            </div>
            </div>
        );
    }
}

export default User;
