import React from 'react';
import '../App.css';
import Webcam from "react-webcam";
import axios from "axios";
import LocalIP from "./LocalIP";
import swal from 'sweetalert';

const initialState = {
    video: "",
    center_points:[],
    videoError: "",
    videoData:"",
    videoRef:null,
    selectedVideo:"",
    intervalId: "",
    frameData:"",
    webcamRef: null
}

class Camera extends React.Component {

    constructor(props) {
        super(props);
        this.state = initialState;
    }

    componentDidMount() {
        const timer = setTimeout(() => {
            if(this.state.webcamRef!==null){
                const imageSrc = this.state.webcamRef.getScreenshot()
                this.uploadImage(imageSrc)
            }
          }, 3000);
    }

    uploadImage = async (image_uri) => {
        const data = JSON.stringify({ image: image_uri});
        await axios
          .post("http://" + LocalIP + ":3500/Main/upload_base64", data, {
            timeout: 4000,
            headers: { "Content-Type": "application/json" },
          })
          .then(async(res)=> {
            const data_url = await res.data;
            const url = "http://" + LocalIP + ":8888/main";
            const data = JSON.stringify({ url: data_url , center_points:this.state.center_points});
            console.log(data);
            await axios
              .post(url, data, {
                headers: { "Content-Type": "application/json" },
              })
              .then(async(res) => {
                console.log(res.data);
                this.setState({frameData:true,frame:data_url,center_points:res.data.center_points})
                const imageSrc = this.state.webcamRef.getScreenshot()
                this.uploadImage(imageSrc)
              });
          });
      };

    render (){
        return (
            <div class="container">
            <div className="col-lg-12">
            <br/><br/>
            <div class="justify-content-center">
                    <h1>Camera testing</h1>
                    <div class="x_scroll">
                    <hr/>
                        <Webcam
                            class="img-thumbnail"
                            ref={(res)=>this.state.webcamRef=res}
                            audio={false}
                            height={720}
                            screenshotFormat="image/jpeg"
                            width={1280}
                        />
                        <br/>
                    <hr/>
                        <div class="form-group row">
                            <div id='image_div'>
                            {this.state.selectedVideo &&
                                <video id="videoPlayer" src={this.state.videoData} ref={(res)=>this.state.videoRef=res} controls width="1280" height="720"/>
                            }
                            </div>
                            {this.state.frameData &&
                                <img src={"http://localhost:3500/output/"+this.state.frame} />
                            }
                            <br/>
                        </div>
                    <hr/>
                    </div>
                </div>
                </div>
            </div>
        );
    }
}

export default Camera;
