import React from 'react';
import '../App.css';
import Webcam from "react-webcam";
import axios from "axios";
import LocalIP from "./LocalIP";
import swal from 'sweetalert';
import html2canvas from 'html2canvas';

const initialState = {
    video: "",
    object_points:[],
    default_object_count:0,
    videoError: "",
    videoData:"",
    videoRef:null,
    selectedVideo:"",
    intervalId: "",
    frameData:"",
    webcamRef: null
}

class Object extends React.Component {

    constructor(props) {
        super(props);
        this.state = initialState;
    }

    componentDidMount() {
        if (!("Notification" in window)) {
            swal("Error!", "Browser does not support desktop notification!", "error")
        } else {
            Notification.requestPermission()
        }
    }

    handleFileChange = (event) => {
        const selectedFile = URL.createObjectURL(event.target.files[0]);
        console.log(selectedFile)
        this.setState({videoData:selectedFile})
        console.log()
    };

    showNotification(msg) {
        var options = {
          body: 'Protest Sys',
          icon: 'https://www.vkf-renzel.com/out/pictures/generated/product/1/356_356_75/r12044336-01/general-warning-sign-10836-1.jpg?    auto=compress&cs=tinysrgb&dpr=1&w=500',
          dir: 'ltr',
        };
    
        new Notification(msg, options);
    }

    startFun =async()=>{
        await this.setState({selectedVideo:true})
        console.log(this.state.videoRef.play())
        if(this.state.videoRef!=null){
            console.log(this.state.videoRef.play())
            this.captureImage()
        }
    }

    captureImage = () => {
        const divToCapture = document.getElementById('image_div');
    
        if (divToCapture) {
          html2canvas(divToCapture).then(canvas => {
            const imgData = canvas.toDataURL('image/png');
            this.uploadImage(imgData)
            console.log(imgData)
          });
        }
      };

    uploadImage = async (image_uri) => {
        const data = JSON.stringify({ image: image_uri});
        await axios
          .post("http://" + LocalIP + ":3500/Main/upload_base64", data, {
            timeout: 4000,
            headers: { "Content-Type": "application/json" },
          })
          .then(async(res)=> {
            const data_url = await res.data;
            const url = "http://" + LocalIP + ":8888/object";
            const data = JSON.stringify({ url: data_url , object_points:this.state.object_points});
            console.log(data);
            await axios
              .post(url, data, {
                headers: { "Content-Type": "application/json" },
              })
              .then(async(res) => {
                console.log(res.data);
                if(this.state.default_object_count==0&&res.data.object_points.length!=0){
                    this.state.default_object_count=res.data.object_points.length
                }
                this.setState({frameData:true,frame:data_url,object_points:res.data.object_points})
                this.captureImage()
                if(this.state.object_points.length!=this.state.default_object_count){
                    this.showNotification("objects move")
                }
              });
          });
      };

    render (){
        return (
            <div class="container">
            <div className="col-lg-12">
            <br/><br/>
            <div class="justify-content-center">
                    <h1>Upload Video</h1>
                    <div class="x_scroll">
                        <br/>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">Video</label>
                            <div class="col-md-6">
                                <input type="file" class="form-control" name="video" value={this.state.video} accept="video/*" onChange={this.handleFileChange} />
                                <div style={{color : "red"}}>{this.state.videoError}</div>
                            </div>
                        </div>
                        <br/>
                        <div class="col-md-4 offset-md-4">
                            <input type="submit" class="btn btn-primary" value="Submit" onClick={this.startFun} />
                        </div>
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

export default Object;
