import React from 'react';
import '../App.css';
import axios from "axios";
import LocalIP from "./LocalIP";
import swal from 'sweetalert';
import { Grid } from '@mui/material';

const initialState = {
    overall: "",
    image1: "",
    frame1: "",
    image2: "",
    frame2: "",
    image3: "",
    frame3: "",
    image4: "",
    frame4: "",
    image5: "",
    frame5: "",
    image6: "",
    frame6: "",
    image7: "",
    frame7: "",
    image8: "",
    frame8: "",
    image9: "",
    frame9: "",
    frameData1:"",
    frameData2:"",
    frameData3:"",
    frameData4:"",
    frameData5:"",
    frameData6:"",
    frameData7:"",
    frameData8:"",
    frameData9:"",
    value1:"",
    value2:"",
    value3:"",
    value4:"",
    value5:"",
    value6:"",
    value7:"",
    value8:"",
    value9:"",
    video: "",
    videoError: "",
    videoData:"",
    videoRef:null,
    selectedVideo:"",
    intervalId: "",
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
                if(event.target.name=="file1"){
                    this.setState({image1:res.data.filename})
                }else if(event.target.name=="file2"){
                    this.setState({image2:res.data.filename})
                }else if(event.target.name=="file3"){
                    this.setState({image3:res.data.filename})
                }else if(event.target.name=="file4"){
                    this.setState({image4:res.data.filename})
                }else if(event.target.name=="file5"){
                    this.setState({image5:res.data.filename})
                }else if(event.target.name=="file6"){
                    this.setState({image6:res.data.filename})
                }else if(event.target.name=="file7"){
                    this.setState({image7:res.data.filename})
                }else if(event.target.name=="file8"){
                    this.setState({image8:res.data.filename})
                }else if(event.target.name=="file9"){
                    this.setState({image9:res.data.filename})
                }
            })
        })
    }

    validation = async() => {

        if( this.state.image1=="" || this.state.image2=="" || this.state.image3=="" || this.state.image4=="" || this.state.image5=="" || this.state.image6=="" || this.state.image7=="" || this.state.image8=="" || this.state.image9=="" ){
            
            swal("Error!", "Upload All Images!", "error")
            
            return false;

        }else{

            return true;
            
        }

    }

    uploadImage = async () => {
        if(await this.validation()){
            var total=0
            const data_url1 = await this.state.image1
            const url = "http://" + LocalIP + ":8888/main";
            const data = JSON.stringify({ url: data_url1 });
            console.log(data);
            await axios
            .post(url, data, {
                headers: { "Content-Type": "application/json" },
            })
            .then(async(res) => {
                console.log(res.data);
                total=total+(res.data.percentage_value*1)
                this.setState({frameData1:true,frame1:data_url1,value1:res.data.percentage_value})
                    
                const data_url2 = await this.state.image2
                const data = JSON.stringify({ url: data_url2 });
                console.log(data);
                await axios
                .post(url, data, {
                    headers: { "Content-Type": "application/json" },
                })
                .then(async(res) => {
                    console.log(res.data);
                    total=total+(res.data.percentage_value*1)
                    this.setState({frameData2:true,frame2:data_url2,value2:res.data.percentage_value})
                    const data_url3 = await this.state.image3
                    const data = JSON.stringify({ url: data_url3 });
                    console.log(data);
                    await axios
                    .post(url, data, {
                        headers: { "Content-Type": "application/json" },
                    })
                    .then(async(res) => {
                        console.log(res.data);
                        total=total+(res.data.percentage_value*1)
                        this.setState({frameData3:true,frame3:data_url3,value3:res.data.percentage_value})
                        const data_url4 = await this.state.image4
                        const data = JSON.stringify({ url: data_url4 });
                        console.log(data);
                        await axios
                        .post(url, data, {
                            headers: { "Content-Type": "application/json" },
                        })
                        .then(async(res) => {
                            console.log(res.data);
                            total=total+(res.data.percentage_value*1)
                            this.setState({frameData4:true,frame4:data_url4,value4:res.data.percentage_value})
                            const data_url5 = await this.state.image5
                            const data = JSON.stringify({ url: data_url5 });
                            console.log(data);
                            await axios
                            .post(url, data, {
                                headers: { "Content-Type": "application/json" },
                            })
                            .then(async(res) => {
                                console.log(res.data);
                                total=total+(res.data.percentage_value*1)
                                this.setState({frameData5:true,frame5:data_url5,value5:res.data.percentage_value})
                                const data_url6 = await this.state.image6
                                const data = JSON.stringify({ url: data_url6 });
                                console.log(data);
                                await axios
                                .post(url, data, {
                                    headers: { "Content-Type": "application/json" },
                                })
                                .then(async(res) => {
                                    console.log(res.data);
                                    total=total+(res.data.percentage_value*1)
                                    this.setState({frameData6:true,frame6:data_url6,value6:res.data.percentage_value})
                                    const data_url7 = await this.state.image7
                                    const data = JSON.stringify({ url: data_url7 });
                                    console.log(data);
                                    await axios
                                    .post(url, data, {
                                        headers: { "Content-Type": "application/json" },
                                    })
                                    .then(async(res) => {
                                        console.log(res.data);
                                        total=total+(res.data.percentage_value*1)
                                        this.setState({frameData7:true,frame7:data_url7,value7:res.data.percentage_value})
                                        const data_url8 = await this.state.image8
                                        const data = JSON.stringify({ url: data_url8 });
                                        console.log(data);
                                        await axios
                                        .post(url, data, {
                                            headers: { "Content-Type": "application/json" },
                                        })
                                        .then(async(res) => {
                                            console.log(res.data);
                                            total=total+(res.data.percentage_value*1)
                                            this.setState({frameData8:true,frame8:data_url8,value8:res.data.percentage_value})
                                            const data_url9 = await this.state.image9
                                            const data = JSON.stringify({ url: data_url9 });
                                            console.log(data);
                                            await axios
                                            .post(url, data, {
                                                headers: { "Content-Type": "application/json" },
                                            })
                                            .then(async(res) => {
                                                console.log(res.data);
                                                total=total+(res.data.percentage_value*9)
                                                this.setState({frameData9:true,frame9:data_url9,value9:res.data.percentage_value,overall:"overall map percentage : "+(total/9)})
                                            });
                                        });
                                    });
                                });
                            });
                        });
                    });
                });
            });
        }
      };

    render (){
        return (
            <div class="container">
            <div className="col-lg-12">
            <br/><br/>
            <div class="justify-content-center">
                    <h1>Map Testing Using Grid Image</h1>
                    <div class="x_scroll">
                    <hr/>
                        
                        <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
                            <Grid item xs={2} sm={4} md={4} >
                                <div class="card">
                                {
                                    (this.state.image1!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image1 } width="1280" height="720" />):(
                                        <input type="file" class="form-control" name="file1"  onChange={this.onChangeHandler} />)
                                }
                                </div>
                            </Grid>
                            <Grid item xs={2} sm={4} md={4} >
                                <div class="card">
                                {
                                    (this.state.image2!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image2 } width="1280" height="720" />):(
                                        <input type="file" class="form-control" name="file2"  onChange={this.onChangeHandler} />)
                                }
                                </div>
                            </Grid>
                            <Grid item xs={2} sm={4} md={4} >
                                <div class="card">
                                {
                                    (this.state.image3!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image3 } width="1280" height="720" />):(
                                        <input type="file" class="form-control" name="file3"  onChange={this.onChangeHandler} />)
                                }
                                </div>
                            </Grid>
                            <Grid item xs={2} sm={4} md={4} >
                                <div class="card">
                                {
                                    (this.state.image4!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image4 } width="1280" height="720" />):(
                                        <input type="file" class="form-control" name="file4"  onChange={this.onChangeHandler} />)
                                }
                                </div>
                            </Grid>
                            <Grid item xs={2} sm={4} md={4} >
                                <div class="card">
                                {
                                    (this.state.image5!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image5 } width="1280" height="720" />):(
                                        <input type="file" class="form-control" name="file5"  onChange={this.onChangeHandler} />)
                                }
                                </div>
                            </Grid>
                            <Grid item xs={2} sm={4} md={4} >
                                <div class="card">
                                {
                                    (this.state.image6!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image6 } width="1280" height="720" />):(
                                        <input type="file" class="form-control" name="file6"  onChange={this.onChangeHandler} />)
                                }
                                </div>
                            </Grid>
                            <Grid item xs={2} sm={4} md={4} >
                                <div class="card">
                                {
                                    (this.state.image7!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image7 } width="1280" height="720" />):(
                                        <input type="file" class="form-control" name="file7"  onChange={this.onChangeHandler} />)
                                }
                                </div>
                            </Grid>
                            <Grid item xs={2} sm={4} md={4} >
                                <div class="card">
                                {
                                    (this.state.image8!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image8 } width="1280" height="720" />):(
                                        <input type="file" class="form-control" name="file8"  onChange={this.onChangeHandler} />)
                                }
                                </div>
                            </Grid>
                            <Grid item xs={2} sm={4} md={4} >
                                <div class="card">
                                {
                                    (this.state.image9!=="")?(<img class="img-thumbnail" src={ "http://localhost:3500/upload/" + this.state.image9 } width="1280" height="720" />):(
                                        <input type="file" class="form-control" name="file9"  onChange={this.onChangeHandler} />)
                                }
                                </div>
                            </Grid>
                        </Grid>
                        <br/>
                        <div class="col-md-4 offset-md-4">
                            <input type="submit" class="btn btn-primary" value="Submit" onClick={this.uploadImage} />
                        </div>
                    <hr/>
                    <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
                            {this.state.frameData1 &&
                                <Grid item xs={2} sm={4} md={4} >
                                    <div class="card">
                                        <img src={"http://localhost:3500/output/"+this.state.frame1} />
                                    </div>
                                        <h5>{this.state.value1}</h5>
                                </Grid>
                            }
                            {this.state.frameData2 &&
                                <Grid item xs={2} sm={4} md={4} >
                                    <div class="card">
                                        <img src={"http://localhost:3500/output/"+this.state.frame2} />
                                    </div>
                                        <h5>{this.state.value2}</h5>
                                </Grid>
                            }
                            {this.state.frameData3 &&
                                <Grid item xs={2} sm={4} md={4} >
                                    <div class="card">
                                        <img src={"http://localhost:3500/output/"+this.state.frame3} />
                                    </div>
                                        <h5>{this.state.value3}</h5>
                                </Grid>
                            }
                            {this.state.frameData4 &&
                                <Grid item xs={2} sm={4} md={4} >
                                    <div class="card">
                                        <img src={"http://localhost:3500/output/"+this.state.frame4} />
                                    </div>
                                        <h5>{this.state.value4}</h5>
                                </Grid>
                            }
                            {this.state.frameData5 &&
                                <Grid item xs={2} sm={4} md={4} >
                                    <div class="card">
                                        <img src={"http://localhost:3500/output/"+this.state.frame5} />
                                    </div>
                                        <h5>{this.state.value5}</h5>
                                </Grid>
                            }
                            {this.state.frameData6 &&
                                <Grid item xs={2} sm={4} md={4} >
                                    <div class="card">
                                        <img src={"http://localhost:3500/output/"+this.state.frame6} />
                                    </div>
                                        <h5>{this.state.value6}</h5>
                                </Grid>
                            }
                            {this.state.frameData7 &&
                                <Grid item xs={2} sm={4} md={4} >
                                    <div class="card">
                                        <img src={"http://localhost:3500/output/"+this.state.frame7} />
                                    </div>
                                        <h5>{this.state.value7}</h5>
                                </Grid>
                            }
                            {this.state.frameData8 &&
                                <Grid item xs={2} sm={4} md={4} >
                                    <div class="card">
                                        <img src={"http://localhost:3500/output/"+this.state.frame8} />
                                    </div>
                                        <h5>{this.state.value8}</h5>
                                </Grid>
                            }
                            {this.state.frameData9 &&
                                <Grid item xs={2} sm={4} md={4} >
                                    <div class="card">
                                        <img src={"http://localhost:3500/output/"+this.state.frame9} />
                                    </div>
                                        <h5>{this.state.value9}</h5>
                                </Grid>
                            }
                        </Grid>
                    <hr/>
                    <h1>{this.state.overall}</h1>
                    </div>
                </div>
                </div>
            </div>
        );
    }
}

export default ImageView;
