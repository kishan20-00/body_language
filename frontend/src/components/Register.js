import React from 'react';
import '../App.css';
import swal from 'sweetalert';
import axios from 'axios';

const initialState = {
    id: "",
    fname: "",
    fnameError: "",
    lname: "",
    lnameError: "",
    address: "",
    addressError: "",
    email: "",
    emailError: "",
    phone: "",
    phoneError: "",
    dob: "",
    dobError: "",
    password: "",
    passwordError: "",
    cPassword: "",
    cPasswordError: ""
}

class Register extends React.Component {

    constructor(props) {
        super(props);
        this.state = initialState;
    }

    componentDidMount() {
        if(localStorage.getItem('usertype')==='admin'){
            window.location.href = "/admin";
        }else if(localStorage.getItem('usertype')==='seller'){
            window.location.href = "/seller";
        }else if(localStorage.getItem('usertype')==='user'){
            window.location.href = "/user";
        }
    }

    handleChange = e => {
        const isCheckbox = e.target.type === "checkbox";
        this.setState({
            [e.target.name]: isCheckbox
                ? e.target.checked
                : e.target.value
        });
    }

    onClear(){
        this.setState(initialState);
    }

    validation = async() => {

        let phoneError = "";
        let fnameError = "";
        let lnameError = "";
        let addressError = "";
        let emailError = "";
        let dobError = "";
        let passwordError = "";
        let cPasswordError = "";

        if(!this.state.fname){
            fnameError="First Name Required!"
        }

        if(!this.state.lname){
            lnameError="Last Name Required!"
        }

        if(!this.state.phone){
            phoneError="Phone Number Required!"
        }else if(this.state.phone.length!==10){
          phoneError="Phone Number 10 Digit!"
        }

        if(!this.state.address){
            addressError="Address Required!"
        }

        if(!this.state.email){
            emailError="Email Required!"
        }

        if(!this.state.dob){
            dobError="Date Of Birth Required!"
        }

        if(!this.state.password){
            passwordError="Password Required!"
        }

        if(!this.state.cPassword){
            cPasswordError="Confirm Password Required!"
        }

        if(this.state.cPassword!==this.state.password){
          cPasswordError="Password & Confirm Password Not Match!"
      }

        if( fnameError|| lnameError || phoneError || addressError || emailError || passwordError || dobError|| cPasswordError){
            
            await this.setState({ fnameError , lnameError , phoneError , addressError , emailError , dobError , passwordError , cPasswordError });
            
            return false;

        }else{

            await this.setState({ fnameError , lnameError , phoneError , addressError , emailError , dobError , passwordError , cPasswordError });
            return true;
            
        }

    }

    SubmitForm = async(e) => {
        e.preventDefault();
        if(await this.validation()){
          console.log(this.state);
          const url = 'http://localhost:3500/user/';
          const data = JSON.stringify({ fname: this.state.fname , lname: this.state.lname , phone: this.state.phone , address: this.state.address , email: this.state.email , dob: this.state.dob ,  password: this.state.password });
          console.log(data);
          await axios.post(url,data,{
              headers: {'Content-Type': 'application/json'}
          })
          .then(res => {
              console.log(res.data);
              this.setState(initialState)
              swal("Success!", "Add Successful!", "success")
          })
        }
    }

    render (){
        return (
            <div class="container">
            <div className="col-lg-12">
            <br/><br/>
            <div class="justify-content-center">
                    <h1>Register</h1>
                    <div class="x_scroll">
                    <hr/>
                        <form autoComplete="off" onSubmit={this.SubmitForm}>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">First Name</label>
                            <div class="col-md-6">
                                <input type="text" class="form-control" name="fname" value={this.state.fname} onChange={this.handleChange} />
                                <div style={{color : "red"}}>{this.state.fnameError}</div>
                            </div>
                        </div>
                        <br/>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">Last Name</label>
                            <div class="col-md-6">
                                <input type="text" class="form-control" name="lname" value={this.state.lname} onChange={this.handleChange} />
                                <div style={{color : "red"}}>{this.state.lnameError}</div>
                            </div>
                        </div>
                        <br/>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">Phone Number</label>
                            <div class="col-md-6">
                                <input type="number" class="form-control" name="phone" value={this.state.phone} onChange={this.handleChange} />
                                <div style={{color : "red"}}>{this.state.phoneError}</div>
                            </div>
                        </div>
                        <br/>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">Date Of Birth</label>
                            <div class="col-md-6">
                                <input type="date" class="form-control" name="dob" value={this.state.dob} onChange={this.handleChange} />
                                <div style={{color : "red"}}>{this.state.dobError}</div>
                            </div>
                        </div>
                        <br/>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">Address</label>
                            <div class="col-md-6">
                                <input type="text" class="form-control" name="address" value={this.state.address} onChange={this.handleChange} />
                                <div style={{color : "red"}}>{this.state.addressError}</div>
                            </div>
                        </div>
                        <br/>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">Email</label>
                            <div class="col-md-6">
                                <input type="email" class="form-control" name="email" min="0" max="100" value={this.state.email} onChange={this.handleChange} />
                                <div style={{color : "red"}}>{this.state.emailError}</div>
                            </div>
                        </div>
                        <br/>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">Password</label>
                            <div class="col-md-6">
                                <input type="password" class="form-control" name="password" min="0" max="100" value={this.state.password} onChange={this.handleChange} />
                                <div style={{color : "red"}}>{this.state.passwordError}</div>
                            </div>
                        </div>
                        <br/>
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label text-md-right font-weight-bold">Confirm Password</label>
                            <div class="col-md-6">
                                <input type="password" class="form-control" name="cPassword" min="0" max="100" value={this.state.cPassword} onChange={this.handleChange} />
                                <div style={{color : "red"}}>{this.state.cPasswordError}</div>
                            </div>
                        </div>
                        <br/>   
                        <div class="col-md-4 offset-md-4">
                            <input type="submit" class="btn btn-primary" value="Submit" />
                            <input type="button" class="btn btn-danger" value="Clear" onClick={() => this.onClear()} />
                        </div>
                        <br/><br/>   
                    </form>
                    </div>
                </div>
                </div>
            </div>
        );
    }
}

export default Register;
