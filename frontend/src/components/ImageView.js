import React from 'react';
import '../App.css';
import axios from "axios";
import LocalIP from "./LocalIP";
import swal from 'sweetalert';

const initialState = {
    image: "",
    imageError: "",
    video: "",
    videoError: "",
    videoData:"",
    videoRef:null,
    selectedVideo:"",
    intervalId: "",
    frameData:"",
    webcamRef: null
}

class ImageView extends React.Component {

    constructor(props) {
        super(props);
        this.state = initialState;
    }

    
    onChangeHandler=event=>{
        this.setState({
            selectedFile: event.target.files[0],
            loaded: 0,
        }, () => {
            const data = new FormData() 
            data.append('file', this.state.selectedFile)
            axios.post("http://localhost:3500/Main/", data, { 
            }).then(res => { 
                this.setState({image:res.data.filename})
            })
        })
    }

    validation = async() => {

        let imageError = "";

        if(!this.state.image){
            imageError="Image Required!"
        }


        if( imageError ){
            
            await this.setState({ imageError });
            
            return false;

        }else{

            await this.setState({ imageError });
            return true;
            
        }

    }

    uploadImage = async () => {
        if(await this.validation()){
            const data_url = await this.state.image
            const url = "http://" + LocalIP + ":8888/main";
            const data = JSON.stringify({ url: data_url });
            console.log(data);
            await axios
            .post(url, data, {
                headers: { "Content-Type": "application/json" },
            })
            .then(async(res) => {
                console.log(res.data);
                this.setState({frameData:true,frame:data_url})
            });
        }
      };

    render (){
        return (
            <div class="container">
            <div className="col-lg-12">
            <br/><br/>
            <div class="justify-content-center">
                    <h1>Image testing</h1>
                    <div class="x_scroll">
                    <hr/>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">Image</label>
                            <div class="col-md-6">
                                <input type="file" class="form-control" name="file"  onChange={this.onChangeHandler} />
                                {
                                    (this.state.image!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image } width="1280" height="720" />):(<div></div>)
                                }
                                <div style={{color : "red"}}>{this.state.imageError}</div>
                            </div>
                        </div>
                        <br/>
                        <div class="col-md-4 offset-md-4">
                            <input type="submit" class="btn btn-primary" value="Submit" onClick={this.uploadImage} />
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

export default ImageView;
